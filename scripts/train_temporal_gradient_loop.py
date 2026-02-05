#!/usr/bin/env python3
"""Finite-difference training loop for clockless temporal gradients.

This script optimizes physical circuit parameters against first-spike timing
objectives using transistor simulations (Spectre + OCEAN).
"""

import argparse
import csv
import json
import math
import re
import shutil
import subprocess
from pathlib import Path
from statistics import mean
from typing import Dict, List, Optional, Sequence, Tuple


class ParamSpec(object):
    def __init__(self, name, scale, min_x, max_x, delta_x, lr, max_step_x):
        self.name = name
        self.scale = scale
        self.min_x = min_x
        self.max_x = max_x
        self.delta_x = delta_x
        self.lr = lr
        self.max_step_x = max_step_x


class TraceEval(object):
    def __init__(
        self,
        delay_ns,
        status,
        first_spikes_ns,
        spike_counts,
        energy_pj,
        target_spikes_ns,
        timing_loss,
        count_penalty,
        order_penalty,
        energy_penalty,
        total_loss,
        eval_dir,
    ):
        self.delay_ns = delay_ns
        self.status = status
        self.first_spikes_ns = first_spikes_ns
        self.spike_counts = spike_counts
        self.energy_pj = energy_pj
        self.target_spikes_ns = target_spikes_ns
        self.timing_loss = timing_loss
        self.count_penalty = count_penalty
        self.order_penalty = order_penalty
        self.energy_penalty = energy_penalty
        self.total_loss = total_loss
        self.eval_dir = eval_dir


class EvalResult(object):
    def __init__(
        self,
        params,
        phase,
        loss,
        timing_loss_mean,
        count_penalty_mean,
        order_penalty_mean,
        energy_penalty_mean,
        energy_pj_mean,
        first_spike_means_ns,
        trace_results,
    ):
        self.params = params
        self.phase = phase
        self.loss = loss
        self.timing_loss_mean = timing_loss_mean
        self.count_penalty_mean = count_penalty_mean
        self.order_penalty_mean = order_penalty_mean
        self.energy_penalty_mean = energy_penalty_mean
        self.energy_pj_mean = energy_pj_mean
        self.first_spike_means_ns = first_spike_means_ns
        self.trace_results = trace_results


def parse_float_list(raw: str, label: str) -> List[float]:
    vals: List[float] = []
    for tok in raw.split(","):
        tok = tok.strip()
        if not tok:
            continue
        vals.append(float(tok))
    if not vals:
        raise SystemExit(f"No values provided for {label}.")
    return vals


def parse_int_list(raw: str, label: str) -> List[int]:
    vals: List[int] = []
    for tok in raw.split(","):
        tok = tok.strip()
        if not tok:
            continue
        vals.append(int(tok))
    if not vals:
        raise SystemExit(f"No values provided for {label}.")
    return vals


def parse_optional_float_list(raw: str) -> List[float]:
    if raw.strip() == "":
        return []
    vals: List[float] = []
    for tok in raw.split(","):
        tok = tok.strip()
        if not tok:
            continue
        vals.append(float(tok))
    return vals


def delay_key(delay_ns: float) -> str:
    return "{:.9f}".format(delay_ns)


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def update_param_line(param_line: str, key: str, value: str) -> str:
    pat = rf"\b{re.escape(key)}=[^ ]+"
    if re.search(pat, param_line):
        return re.sub(pat, f"{key}={value}", param_line)
    return f"{param_line} {key}={value}"


def build_temp_netlist(
    src_text: str,
    params: Dict[str, float],
    pre_delay_ns: float,
) -> str:
    text = src_text

    m = re.search(r"^parameters\s+.+$", text, flags=re.MULTILINE)
    if not m:
        raise SystemExit("Could not find parameters line in source netlist.")
    param_line = m.group(0)
    param_line = update_param_line(param_line, "r_fb", f"{params['r_fb']:.6f}")
    param_line = update_param_line(param_line, "rleak", f"{params['rleak']:.6f}")
    param_line = update_param_line(param_line, "iin_amp", f"{params['iin_amp']:.6f}")
    param_line = update_param_line(param_line, "pre_delay", f"{pre_delay_ns:.6f}n")
    text = text[: m.start()] + param_line + text[m.end() :]

    # Make the drive amplitude trainable and the pulse delay trace-configurable.
    text = re.sub(
        r"(V_PRE0\s*\(pre0 0\)\s*vsource\s*type=pulse[\s\S]*?\bval1=)[^\s\\]+",
        r"\1iin_amp",
        text,
        count=1,
    )
    text = re.sub(
        r"(V_PRE0\s*\(pre0 0\)\s*vsource\s*type=pulse[\s\S]*?\bdelay=)[^\s\\]+",
        r"\1pre_delay",
        text,
        count=1,
    )

    # Ensure supply current is saved for energy integration.
    sm = re.search(r"^save\s+.+$", text, flags=re.MULTILINE)
    if not sm:
        raise SystemExit("Could not find save line in source netlist.")
    save_line = sm.group(0)
    if "V_VDD:p" not in save_line:
        save_line = save_line + " V_VDD:p"
        text = text[: sm.start()] + save_line + text[sm.end() :]

    return text


def build_metrics_ocn(raw_dir: Path, out_file: Path, tstop_ns: float) -> str:
    return f"""; auto-generated metrics extraction for temporal gradient training
out = outfile(\"{out_file.as_posix()}\" \"w\")

simulator('spectre)
openResults(\"{raw_dir.as_posix()}\")
selectResult(\"tran_test-tran\")

procedure(countRising(sig th dt tstart tstop)
  let((cnt ts prev curr)
    cnt = 0
    ts = tstart
    prev = value(sig ts)
    ts = ts + dt
    while(ts < tstop
      curr = value(sig ts)
      if(prev < th && curr > th then
        cnt = cnt + 1
      )
      prev = curr
      ts = ts + dt
    )
    cnt
  )
)

procedure(firstCross(sig th dt tstart tstop)
  let((ts prev curr frac tcross found)
    tcross = nil
    found = nil
    ts = tstart
    prev = value(sig ts)
    ts = ts + dt
    while(ts < tstop && !found
      curr = value(sig ts)
      if(prev < th && curr > th then
        frac = (th - prev) / (curr - prev)
        if(frac < 0 then frac = 0)
        if(frac > 1 then frac = 1)
        tcross = (ts - dt) + frac * dt
        found = t
      )
      prev = curr
      ts = ts + dt
    )
    tcross
  )
)

vspk0 = v(\"spike0\")
vspk1 = v(\"spike1\")
vspk2 = v(\"spike2\")
vspk3 = v(\"spike3\")
idd = getData(\"V_VDD:p\")

if(vspk0 && vspk1 && vspk2 && vspk3 && idd then
  dt = 100p
  t0 = 1n
  t1 = {tstop_ns}n

  s0min = ymin(vspk0)
  s1min = ymin(vspk1)
  s2min = ymin(vspk2)
  s3min = ymin(vspk3)
  s0max = ymax(vspk0)
  s1max = ymax(vspk1)
  s2max = ymax(vspk2)
  s3max = ymax(vspk3)

  th0 = (s0max + s0min) / 2
  th1 = (s1max + s1min) / 2
  th2 = (s2max + s2min) / 2
  th3 = (s3max + s3min) / 2

  c0 = countRising(vspk0 th0 dt t0 t1)
  c1 = countRising(vspk1 th1 dt t0 t1)
  c2 = countRising(vspk2 th2 dt t0 t1)
  c3 = countRising(vspk3 th3 dt t0 t1)

  f0 = firstCross(vspk0 th0 dt t0 t1)
  f1 = firstCross(vspk1 th1 dt t0 t1)
  f2 = firstCross(vspk2 th2 dt t0 t1)
  f3 = firstCross(vspk3 th3 dt t0 t1)

  energy = 0
  ts = 0n
  prev_i = value(idd ts)
  prev_t = ts
  ts = ts + dt
  while(ts <= {tstop_ns}n
    curr_i = value(idd ts)
    p0 = -prev_i * 1.8
    p1 = -curr_i * 1.8
    energy = energy + 0.5 * (p0 + p1) * (ts - prev_t)
    prev_i = curr_i
    prev_t = ts
    ts = ts + dt
  )

  fprintf(out \"status=OK\\n\")
  fprintf(out \"spike0_count=%d\\n\" c0)
  fprintf(out \"spike1_count=%d\\n\" c1)
  fprintf(out \"spike2_count=%d\\n\" c2)
  fprintf(out \"spike3_count=%d\\n\" c3)

  if(f0 then fprintf(out \"spike0_first_ns=%.9f\\n\" f0*1e9) else fprintf(out \"spike0_first_ns=-1\\n\"))
  if(f1 then fprintf(out \"spike1_first_ns=%.9f\\n\" f1*1e9) else fprintf(out \"spike1_first_ns=-1\\n\"))
  if(f2 then fprintf(out \"spike2_first_ns=%.9f\\n\" f2*1e9) else fprintf(out \"spike2_first_ns=-1\\n\"))
  if(f3 then fprintf(out \"spike3_first_ns=%.9f\\n\" f3*1e9) else fprintf(out \"spike3_first_ns=-1\\n\"))

  fprintf(out \"energy_j=%.12e\\n\" energy)
else
  fprintf(out \"status=ERROR\\n\")
)

close(out)
exit()
"""


def parse_metrics(path: Path) -> Dict[str, str]:
    out: Dict[str, str] = {}
    if not path.exists():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def run_cmd(cmd: Sequence[str], cwd: Path, stdout: Optional[Path] = None) -> int:
    if stdout is None:
        proc = subprocess.run(cmd, cwd=cwd)
        return proc.returncode
    with stdout.open("w", encoding="utf-8") as f:
        proc = subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT)
    return proc.returncode


def evaluate_trace(
    source_netlist_text: str,
    params: Dict[str, float],
    pre_delay_ns: float,
    target_spikes_ns: List[float],
    expected_counts: List[int],
    eval_dir: Path,
    tstop_ns: float,
    missing_penalty_ns2: float,
    count_penalty_weight: float,
    order_penalty: float,
    order_margin_ns: float,
    energy_weight: float,
    energy_ref_pj: float,
) -> TraceEval:
    eval_dir.mkdir(parents=True, exist_ok=True)

    netlist_path = eval_dir / "neuro_tile4_coupled_train.scs"
    raw_dir = eval_dir / "neuro_tile4_coupled.raw"
    spectre_log = eval_dir / "spectre.log"
    spectre_stdout_log = eval_dir / "spectre_stdout.log"
    ocean_log = eval_dir / "ocean.log"
    metrics_path = eval_dir / "metrics.txt"
    ocn_path = eval_dir / "extract_metrics.ocn"

    netlist_text = build_temp_netlist(source_netlist_text, params, pre_delay_ns)
    write_text(netlist_path, netlist_text)

    rc = run_cmd(
        [
            "spectre",
            str(netlist_path.name),
            "-raw",
            str(raw_dir.name),
            "+log",
            str(spectre_log.name),
        ],
        cwd=eval_dir,
        stdout=spectre_stdout_log,
    )

    if rc != 0:
        return TraceEval(
            delay_ns=pre_delay_ns,
            status="SPECTRE_FAIL",
            first_spikes_ns=[-1.0, -1.0, -1.0, -1.0],
            spike_counts=[0, 0, 0, 0],
            energy_pj=1e9,
            target_spikes_ns=target_spikes_ns,
            timing_loss=missing_penalty_ns2,
            count_penalty=4.0 * count_penalty_weight,
            order_penalty=0.0,
            energy_penalty=energy_weight * (1e9 / max(energy_ref_pj, 1e-9)),
            total_loss=missing_penalty_ns2 + 4.0 * count_penalty_weight + energy_weight * (1e9 / max(energy_ref_pj, 1e-9)),
            eval_dir=eval_dir,
        )

    if "completes with 0 errors" not in spectre_log.read_text(encoding="utf-8", errors="ignore"):
        return TraceEval(
            delay_ns=pre_delay_ns,
            status="SPECTRE_LOG_FAIL",
            first_spikes_ns=[-1.0, -1.0, -1.0, -1.0],
            spike_counts=[0, 0, 0, 0],
            energy_pj=1e9,
            target_spikes_ns=target_spikes_ns,
            timing_loss=missing_penalty_ns2,
            count_penalty=4.0 * count_penalty_weight,
            order_penalty=0.0,
            energy_penalty=energy_weight * (1e9 / max(energy_ref_pj, 1e-9)),
            total_loss=missing_penalty_ns2 + 4.0 * count_penalty_weight + energy_weight * (1e9 / max(energy_ref_pj, 1e-9)),
            eval_dir=eval_dir,
        )

    write_text(ocn_path, build_metrics_ocn(raw_dir=raw_dir, out_file=metrics_path, tstop_ns=tstop_ns))
    rc_ocean = run_cmd(["bash", "-lc", f"ocean -nograph < '{ocn_path.name}'"], cwd=eval_dir, stdout=ocean_log)
    metrics = parse_metrics(metrics_path)

    if rc_ocean != 0 or metrics.get("status") != "OK":
        return TraceEval(
            delay_ns=pre_delay_ns,
            status="OCEAN_FAIL",
            first_spikes_ns=[-1.0, -1.0, -1.0, -1.0],
            spike_counts=[0, 0, 0, 0],
            energy_pj=1e9,
            target_spikes_ns=target_spikes_ns,
            timing_loss=missing_penalty_ns2,
            count_penalty=4.0 * count_penalty_weight,
            order_penalty=0.0,
            energy_penalty=energy_weight * (1e9 / max(energy_ref_pj, 1e-9)),
            total_loss=missing_penalty_ns2 + 4.0 * count_penalty_weight + energy_weight * (1e9 / max(energy_ref_pj, 1e-9)),
            eval_dir=eval_dir,
        )

    first = [
        float(metrics.get("spike0_first_ns", "-1")),
        float(metrics.get("spike1_first_ns", "-1")),
        float(metrics.get("spike2_first_ns", "-1")),
        float(metrics.get("spike3_first_ns", "-1")),
    ]
    counts = [
        int(float(metrics.get("spike0_count", "0"))),
        int(float(metrics.get("spike1_count", "0"))),
        int(float(metrics.get("spike2_count", "0"))),
        int(float(metrics.get("spike3_count", "0"))),
    ]
    energy_j = float(metrics.get("energy_j", "1e9"))
    energy_pj = energy_j * 1e12

    timing_terms: List[float] = []
    for i in range(4):
        if first[i] < 0.0:
            timing_terms.append(missing_penalty_ns2)
        else:
            err = first[i] - target_spikes_ns[i]
            timing_terms.append(err * err)
    timing_loss = mean(timing_terms)

    cpen = 0.0
    for i, c in enumerate(counts):
        exp_c = expected_counts[i] if i < len(expected_counts) else expected_counts[-1]
        cpen += count_penalty_weight * abs(float(c - exp_c))

    open_spikes = [t for t in first if t >= 0.0]
    open_idx = [i for i, t in enumerate(first) if t >= 0.0]
    open_map = dict(zip(open_idx, open_spikes))
    open_pen = 0.0
    for i in range(3):
        if i in open_map and (i + 1) in open_map:
            violation = (open_map[i] + order_margin_ns) - open_map[i + 1]
            if violation > 0.0:
                open_pen += order_penalty * violation * violation

    epen = energy_weight * (max(0.0, energy_pj) / max(energy_ref_pj, 1e-9))
    total = timing_loss + cpen + open_pen + epen

    return TraceEval(
        delay_ns=pre_delay_ns,
        status="OK",
        first_spikes_ns=first,
        spike_counts=counts,
        energy_pj=energy_pj,
        target_spikes_ns=target_spikes_ns,
        timing_loss=timing_loss,
        count_penalty=cpen,
        order_penalty=open_pen,
        energy_penalty=epen,
        total_loss=total,
        eval_dir=eval_dir,
    )


def evaluate_params(
    source_netlist_text: str,
    params: Dict[str, float],
    phase: str,
    out_root: Path,
    trace_delays_ns: Sequence[float],
    trace_target_map: Dict[str, List[float]],
    trace_expected_counts_map: Dict[str, List[int]],
    tstop_ns: float,
    missing_penalty_ns2: float,
    count_penalty_weight: float,
    order_penalty: float,
    order_margin_ns: float,
    energy_weight: float,
    energy_ref_pj: float,
) -> EvalResult:
    phase_dir = out_root / phase
    traces: List[TraceEval] = []

    for idx, delay_ns in enumerate(trace_delays_ns):
        dkey = delay_key(delay_ns)
        if dkey not in trace_target_map:
            raise SystemExit("Missing target map for delay {}".format(delay_ns))
        target = trace_target_map[dkey]
        expected_counts = trace_expected_counts_map.get(dkey, [1, 1, 1, 1])
        tr = evaluate_trace(
            source_netlist_text=source_netlist_text,
            params=params,
            pre_delay_ns=delay_ns,
            target_spikes_ns=target,
            expected_counts=expected_counts,
            eval_dir=phase_dir / f"trace_{idx:02d}_{delay_ns:.3f}ns",
            tstop_ns=tstop_ns,
            missing_penalty_ns2=missing_penalty_ns2,
            count_penalty_weight=count_penalty_weight,
            order_penalty=order_penalty,
            order_margin_ns=order_margin_ns,
            energy_weight=energy_weight,
            energy_ref_pj=energy_ref_pj,
        )
        traces.append(tr)

    loss = mean(t.total_loss for t in traces)
    tmean = mean(t.timing_loss for t in traces)
    cmean = mean(t.count_penalty for t in traces)
    omean = mean(t.order_penalty for t in traces)
    emean = mean(t.energy_penalty for t in traces)
    energy_mean = mean(t.energy_pj for t in traces)

    first_means = []
    for ch in range(4):
        vals = [t.first_spikes_ns[ch] for t in traces if t.first_spikes_ns[ch] >= 0.0]
        first_means.append(mean(vals) if vals else -1.0)

    return EvalResult(
        params=dict(params),
        phase=phase,
        loss=loss,
        timing_loss_mean=tmean,
        count_penalty_mean=cmean,
        order_penalty_mean=omean,
        energy_penalty_mean=emean,
        energy_pj_mean=energy_mean,
        first_spike_means_ns=first_means,
        trace_results=traces,
    )


def make_loss_svg(path: Path, records: List[EvalResult]) -> None:
    pts = [r for r in records if r.phase.startswith("iter_") or r.phase == "final"]
    if not pts:
        return
    y_max = max(r.loss for r in pts) * 1.1
    y_max = max(y_max, 1.0)
    w, h = 1100, 620
    left, top, pw, ph = 90, 80, 920, 420

    def x_of(i: int) -> float:
        denom = max(len(pts) - 1, 1)
        return left + i * pw / denom

    def y_of(v: float) -> float:
        return top + ph - (v / y_max) * ph

    body = ['<rect x="0" y="0" width="100%" height="100%" fill="#f7fafc"/>']
    body.append('<text x="24" y="42" font-family="Helvetica,Arial,sans-serif" font-size="30" font-weight="bold" fill="#102033">Temporal Gradient Training Loss</text>')
    body.append(f'<rect x="{left}" y="{top}" width="{pw}" height="{ph}" fill="#ffffff" stroke="#d1d9e6" stroke-width="2"/>')

    for i in range(6):
        yv = y_max * i / 5.0
        y = y_of(yv)
        body.append(f'<line x1="{left}" y1="{y:.2f}" x2="{left+pw}" y2="{y:.2f}" stroke="#e6ecf2" stroke-width="1"/>')
        body.append(f'<text x="16" y="{y+4:.2f}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="#4a5d73">{yv:.2f}</text>')

    ptxt = []
    for i, r in enumerate(pts):
        x = x_of(i)
        y = y_of(r.loss)
        ptxt.append(f"{x:.2f},{y:.2f}")
        body.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="#d62728"/>')
        body.append(f'<text x="{x-12:.2f}" y="{top+ph+24}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="#4a5d73">{i}</text>')

    body.append(f'<polyline points="{" ".join(ptxt)}" fill="none" stroke="#d62728" stroke-width="3"/>')
    body.append(f'<text x="{left+pw+10}" y="{top+ph+24}" font-family="Helvetica,Arial,sans-serif" font-size="12" font-weight="bold" fill="#2c3e50">step</text>')
    body.append(f'<text x="{20}" y="{top+ph+18}" font-family="Helvetica,Arial,sans-serif" font-size="12" font-weight="bold" fill="#2c3e50">loss</text>')

    write_text(
        path,
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n' + "\n".join(body) + "\n</svg>\n",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Finite-difference temporal gradient training loop.")
    parser.add_argument("--netlist-source", type=Path, default=Path("netlists/neuro_tile4_coupled.scs"))
    parser.add_argument("--out-dir", type=Path, required=True)

    parser.add_argument("--target-mode", choices=["absolute", "measured_anchor_shift"], default="absolute")
    parser.add_argument("--target-first-spikes-ns", default="47.5,49.5,51.5,53.5")
    parser.add_argument("--target-shift-ns", default="1.0,1.0,1.0,1.0")
    parser.add_argument("--target-spike-counts", default="15,15,15,15")
    parser.add_argument("--use-anchor-counts", action="store_true")
    parser.add_argument("--trace-delays-ns", default="")
    parser.add_argument("--train-trace-delays-ns", default="5.0,8.0")
    parser.add_argument("--holdout-trace-delays-ns", default="6.5,9.5")
    parser.add_argument("--anchor-probe-split", choices=["train", "all"], default="train")
    parser.add_argument("--base-delay-ns", type=float, default=5.0)
    parser.add_argument("--tstop-ns", type=float, default=300.0)

    parser.add_argument("--iters", type=int, default=4)

    parser.add_argument("--init-r-fb", type=float, default=1000.0)
    parser.add_argument("--init-rleak", type=float, default=8_000_000.0)
    parser.add_argument("--init-iin-amp", type=float, default=1.8)

    parser.add_argument("--r-fb-bounds", default="600,5000")
    parser.add_argument("--rleak-bounds", default="3000000,20000000")
    parser.add_argument("--iin-amp-bounds", default="1.2,1.8")

    parser.add_argument("--delta-r-fb-x", type=float, default=0.05)
    parser.add_argument("--delta-rleak-x", type=float, default=0.25)
    parser.add_argument("--delta-iin-amp-x", type=float, default=0.02)

    parser.add_argument("--lr-r-fb", type=float, default=0.20)
    parser.add_argument("--lr-rleak", type=float, default=0.15)
    parser.add_argument("--lr-iin-amp", type=float, default=0.10)

    parser.add_argument("--max-step-r-fb-x", type=float, default=0.20)
    parser.add_argument("--max-step-rleak-x", type=float, default=0.40)
    parser.add_argument("--max-step-iin-amp-x", type=float, default=0.05)
    parser.add_argument("--grad-norm-eps", type=float, default=25.0)

    parser.add_argument("--missing-penalty-ns2", type=float, default=400.0)
    parser.add_argument("--count-penalty", type=float, default=12.0)
    parser.add_argument("--order-penalty", type=float, default=35.0)
    parser.add_argument("--order-margin-ns", type=float, default=0.20)
    parser.add_argument("--energy-weight", type=float, default=0.03)
    parser.add_argument("--energy-weight-start", type=float, default=None)
    parser.add_argument("--energy-weight-end", type=float, default=None)

    args = parser.parse_args()

    if shutil.which("spectre") is None or shutil.which("ocean") is None:
        raise SystemExit("spectre/ocean not found. Run `source setup_cadence.sh` first.")

    target_base = parse_float_list(args.target_first_spikes_ns, "target-first-spikes-ns")
    if len(target_base) != 4:
        raise SystemExit("target-first-spikes-ns must contain exactly 4 values.")
    target_shift = parse_float_list(args.target_shift_ns, "target-shift-ns")
    if len(target_shift) != 4:
        raise SystemExit("target-shift-ns must contain exactly 4 values.")
    target_counts = parse_int_list(args.target_spike_counts, "target-spike-counts")
    if len(target_counts) != 4:
        raise SystemExit("target-spike-counts must contain exactly 4 values.")
    if args.trace_delays_ns.strip():
        train_trace_delays_ns = parse_float_list(args.trace_delays_ns, "trace-delays-ns")
        holdout_trace_delays_ns = []
    else:
        train_trace_delays_ns = parse_float_list(args.train_trace_delays_ns, "train-trace-delays-ns")
        holdout_trace_delays_ns = parse_optional_float_list(args.holdout_trace_delays_ns)

    if not train_trace_delays_ns:
        raise SystemExit("At least one training trace delay is required.")
    all_trace_delays_ns = sorted(set(train_trace_delays_ns + holdout_trace_delays_ns))
    anchor_probe_delays_ns = train_trace_delays_ns if args.anchor_probe_split == "train" else all_trace_delays_ns

    if (args.energy_weight_start is None) != (args.energy_weight_end is None):
        raise SystemExit("Specify both --energy-weight-start and --energy-weight-end, or neither.")
    if args.energy_weight_start is None:
        energy_weight_start = args.energy_weight
        energy_weight_end = args.energy_weight
    else:
        energy_weight_start = float(args.energy_weight_start)
        energy_weight_end = float(args.energy_weight_end)

    def energy_weight_for_step(step_idx: int, total_steps: int) -> float:
        if total_steps <= 1:
            return energy_weight_end
        alpha = float(step_idx) / float(total_steps - 1)
        return energy_weight_start + (energy_weight_end - energy_weight_start) * alpha

    rfb_bounds = parse_float_list(args.r_fb_bounds, "r-fb-bounds")
    rleak_bounds = parse_float_list(args.rleak_bounds, "rleak-bounds")
    iin_bounds = parse_float_list(args.iin_amp_bounds, "iin-amp-bounds")
    if len(rfb_bounds) != 2 or len(rleak_bounds) != 2 or len(iin_bounds) != 2:
        raise SystemExit("bounds args must have two comma-separated numbers.")

    param_specs = {
        "r_fb": ParamSpec(
            name="r_fb",
            scale=1000.0,
            min_x=min(rfb_bounds) / 1000.0,
            max_x=max(rfb_bounds) / 1000.0,
            delta_x=args.delta_r_fb_x,
            lr=args.lr_r_fb,
            max_step_x=args.max_step_r_fb_x,
        ),
        "rleak": ParamSpec(
            name="rleak",
            scale=1_000_000.0,
            min_x=min(rleak_bounds) / 1_000_000.0,
            max_x=max(rleak_bounds) / 1_000_000.0,
            delta_x=args.delta_rleak_x,
            lr=args.lr_rleak,
            max_step_x=args.max_step_rleak_x,
        ),
        "iin_amp": ParamSpec(
            name="iin_amp",
            scale=1.0,
            min_x=min(iin_bounds),
            max_x=max(iin_bounds),
            delta_x=args.delta_iin_amp_x,
            lr=args.lr_iin_amp,
            max_step_x=args.max_step_iin_amp_x,
        ),
    }

    x = {
        "r_fb": clamp(args.init_r_fb / param_specs["r_fb"].scale, param_specs["r_fb"].min_x, param_specs["r_fb"].max_x),
        "rleak": clamp(args.init_rleak / param_specs["rleak"].scale, param_specs["rleak"].min_x, param_specs["rleak"].max_x),
        "iin_amp": clamp(args.init_iin_amp / param_specs["iin_amp"].scale, param_specs["iin_amp"].min_x, param_specs["iin_amp"].max_x),
    }

    source_netlist_text = args.netlist_source.read_text(encoding="utf-8")

    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    eval_csv_path = out_dir / "temporal_gradient_learning.csv"
    trace_csv_path = out_dir / "temporal_gradient_trace.csv"
    summary_md_path = out_dir / "temporal_gradient_learning_summary.md"
    loss_svg_path = out_dir / "temporal_gradient_learning_loss.svg"

    eval_rows: List[Dict[str, str]] = []
    trace_rows: List[Dict[str, str]] = []
    eval_records: List[EvalResult] = []

    trace_target_map: Dict[str, List[float]] = {}
    trace_expected_counts_map: Dict[str, List[int]] = {}
    for d in all_trace_delays_ns:
        dkey = delay_key(d)
        trace_target_map[dkey] = [t + (d - args.base_delay_ns) for t in target_base]
        trace_expected_counts_map[dkey] = list(target_counts)

    # Probe at initial parameters so target/count defaults can be grounded in this circuit regime.
    anchor_params = {k: x[k] * param_specs[k].scale for k in x}
    anchor_probe = evaluate_params(
        source_netlist_text=source_netlist_text,
        params=anchor_params,
        phase="anchor_probe",
        out_root=out_dir,
        trace_delays_ns=anchor_probe_delays_ns,
        trace_target_map=trace_target_map,
        trace_expected_counts_map=trace_expected_counts_map,
        tstop_ns=args.tstop_ns,
        missing_penalty_ns2=args.missing_penalty_ns2,
        count_penalty_weight=args.count_penalty,
        order_penalty=args.order_penalty,
        order_margin_ns=args.order_margin_ns,
        energy_weight=0.0,
        energy_ref_pj=1.0,
    )

    if args.target_mode == "measured_anchor_shift":
        for tr in anchor_probe.trace_results:
            dkey = delay_key(tr.delay_ns)
            adaptive_target: List[float] = []
            for i in range(4):
                base_t = tr.first_spikes_ns[i]
                if base_t < 0.0:
                    base_t = trace_target_map[dkey][i]
                adaptive_target.append(base_t + target_shift[i])
            trace_target_map[dkey] = adaptive_target
            if args.use_anchor_counts:
                trace_expected_counts_map[dkey] = list(tr.spike_counts)

    # Use anchor energy as normalization reference so energy term has stable scale.
    energy_ref_pj = max(anchor_probe.energy_pj_mean, 1e-6)

    for itr in range(args.iters):
        params = {k: x[k] * param_specs[k].scale for k in x}
        energy_weight_iter = energy_weight_for_step(itr, args.iters)
        base = evaluate_params(
            source_netlist_text=source_netlist_text,
            params=params,
            phase=f"iter_{itr:02d}_train_base",
            out_root=out_dir,
            trace_delays_ns=train_trace_delays_ns,
            trace_target_map=trace_target_map,
            trace_expected_counts_map=trace_expected_counts_map,
            tstop_ns=args.tstop_ns,
            missing_penalty_ns2=args.missing_penalty_ns2,
            count_penalty_weight=args.count_penalty,
            order_penalty=args.order_penalty,
            order_margin_ns=args.order_margin_ns,
            energy_weight=energy_weight_iter,
            energy_ref_pj=energy_ref_pj,
        )
        eval_records.append(base)
        holdout = None
        if holdout_trace_delays_ns:
            holdout = evaluate_params(
                source_netlist_text=source_netlist_text,
                params=params,
                phase=f"iter_{itr:02d}_holdout_base",
                out_root=out_dir,
                trace_delays_ns=holdout_trace_delays_ns,
                trace_target_map=trace_target_map,
                trace_expected_counts_map=trace_expected_counts_map,
                tstop_ns=args.tstop_ns,
                missing_penalty_ns2=args.missing_penalty_ns2,
                count_penalty_weight=args.count_penalty,
                order_penalty=args.order_penalty,
                order_margin_ns=args.order_margin_ns,
                energy_weight=energy_weight_iter,
                energy_ref_pj=energy_ref_pj,
            )

        grads_x: Dict[str, float] = {}
        updates_x: Dict[str, float] = {}

        for name, spec in param_specs.items():
            x_plus = dict(x)
            x_minus = dict(x)
            x_plus[name] = clamp(x_plus[name] + spec.delta_x, spec.min_x, spec.max_x)
            x_minus[name] = clamp(x_minus[name] - spec.delta_x, spec.min_x, spec.max_x)

            params_plus = {k: x_plus[k] * param_specs[k].scale for k in x_plus}
            params_minus = {k: x_minus[k] * param_specs[k].scale for k in x_minus}

            plus = evaluate_params(
                source_netlist_text=source_netlist_text,
                params=params_plus,
                phase=f"iter_{itr:02d}_{name}_plus",
                out_root=out_dir,
                trace_delays_ns=train_trace_delays_ns,
                trace_target_map=trace_target_map,
                trace_expected_counts_map=trace_expected_counts_map,
                tstop_ns=args.tstop_ns,
                missing_penalty_ns2=args.missing_penalty_ns2,
                count_penalty_weight=args.count_penalty,
                order_penalty=args.order_penalty,
                order_margin_ns=args.order_margin_ns,
                energy_weight=energy_weight_iter,
                energy_ref_pj=energy_ref_pj,
            )
            minus = evaluate_params(
                source_netlist_text=source_netlist_text,
                params=params_minus,
                phase=f"iter_{itr:02d}_{name}_minus",
                out_root=out_dir,
                trace_delays_ns=train_trace_delays_ns,
                trace_target_map=trace_target_map,
                trace_expected_counts_map=trace_expected_counts_map,
                tstop_ns=args.tstop_ns,
                missing_penalty_ns2=args.missing_penalty_ns2,
                count_penalty_weight=args.count_penalty,
                order_penalty=args.order_penalty,
                order_margin_ns=args.order_margin_ns,
                energy_weight=energy_weight_iter,
                energy_ref_pj=energy_ref_pj,
            )

            span = x_plus[name] - x_minus[name]
            if span <= 1e-12:
                grad_x = 0.0
            else:
                grad_x = (plus.loss - minus.loss) / span
            step_x = -spec.lr * grad_x / (abs(grad_x) + args.grad_norm_eps)
            step_x = clamp(step_x, -spec.max_step_x, spec.max_step_x)
            grads_x[name] = grad_x
            updates_x[name] = step_x

        for name, spec in param_specs.items():
            x[name] = clamp(x[name] + updates_x[name], spec.min_x, spec.max_x)

        denom = max(base.loss, 1e-12)
        eval_rows.append(
            {
                "iter": str(itr),
                "phase": base.phase,
                "loss": f"{base.loss:.9f}",
                "timing_loss": f"{base.timing_loss_mean:.9f}",
                "count_penalty": f"{base.count_penalty_mean:.9f}",
                "order_penalty": f"{base.order_penalty_mean:.9f}",
                "energy_penalty": f"{base.energy_penalty_mean:.9f}",
                "timing_pct": f"{(100.0 * base.timing_loss_mean / denom):.9f}",
                "count_pct": f"{(100.0 * base.count_penalty_mean / denom):.9f}",
                "order_pct": f"{(100.0 * base.order_penalty_mean / denom):.9f}",
                "energy_pct": f"{(100.0 * base.energy_penalty_mean / denom):.9f}",
                "energy_weight": f"{energy_weight_iter:.9f}",
                "energy_pj": f"{base.energy_pj_mean:.9f}",
                "r_fb": f"{params['r_fb']:.9f}",
                "rleak": f"{params['rleak']:.9f}",
                "iin_amp": f"{params['iin_amp']:.9f}",
                "spike0_ns": f"{base.first_spike_means_ns[0]:.9f}",
                "spike1_ns": f"{base.first_spike_means_ns[1]:.9f}",
                "spike2_ns": f"{base.first_spike_means_ns[2]:.9f}",
                "spike3_ns": f"{base.first_spike_means_ns[3]:.9f}",
                "holdout_loss": "" if holdout is None else f"{holdout.loss:.9f}",
                "holdout_timing_loss": "" if holdout is None else f"{holdout.timing_loss_mean:.9f}",
                "holdout_energy_pj": "" if holdout is None else f"{holdout.energy_pj_mean:.9f}",
                "grad_r_fb_x": f"{grads_x['r_fb']:.9f}",
                "grad_rleak_x": f"{grads_x['rleak']:.9f}",
                "grad_iin_amp_x": f"{grads_x['iin_amp']:.9f}",
                "update_r_fb_x": f"{updates_x['r_fb']:.9f}",
                "update_rleak_x": f"{updates_x['rleak']:.9f}",
                "update_iin_amp_x": f"{updates_x['iin_amp']:.9f}",
            }
        )

        for tr in base.trace_results:
            trace_rows.append(
                {
                    "iter": str(itr),
                    "phase": base.phase,
                    "split": "train",
                    "delay_ns": f"{tr.delay_ns:.9f}",
                    "status": tr.status,
                    "loss": f"{tr.total_loss:.9f}",
                    "timing_loss": f"{tr.timing_loss:.9f}",
                    "count_penalty": f"{tr.count_penalty:.9f}",
                    "order_penalty": f"{tr.order_penalty:.9f}",
                    "energy_penalty": f"{tr.energy_penalty:.9f}",
                    "energy_pj": f"{tr.energy_pj:.9f}",
                    "spike0_first_ns": f"{tr.first_spikes_ns[0]:.9f}",
                    "spike1_first_ns": f"{tr.first_spikes_ns[1]:.9f}",
                    "spike2_first_ns": f"{tr.first_spikes_ns[2]:.9f}",
                    "spike3_first_ns": f"{tr.first_spikes_ns[3]:.9f}",
                    "spike0_target_ns": f"{tr.target_spikes_ns[0]:.9f}",
                    "spike1_target_ns": f"{tr.target_spikes_ns[1]:.9f}",
                    "spike2_target_ns": f"{tr.target_spikes_ns[2]:.9f}",
                    "spike3_target_ns": f"{tr.target_spikes_ns[3]:.9f}",
                    "spike0_count": str(tr.spike_counts[0]),
                    "spike1_count": str(tr.spike_counts[1]),
                    "spike2_count": str(tr.spike_counts[2]),
                    "spike3_count": str(tr.spike_counts[3]),
                    "eval_dir": str(tr.eval_dir),
                }
            )
        if holdout is not None:
            for tr in holdout.trace_results:
                trace_rows.append(
                    {
                        "iter": str(itr),
                        "phase": holdout.phase,
                        "split": "holdout",
                        "delay_ns": f"{tr.delay_ns:.9f}",
                        "status": tr.status,
                        "loss": f"{tr.total_loss:.9f}",
                        "timing_loss": f"{tr.timing_loss:.9f}",
                        "count_penalty": f"{tr.count_penalty:.9f}",
                        "order_penalty": f"{tr.order_penalty:.9f}",
                        "energy_penalty": f"{tr.energy_penalty:.9f}",
                        "energy_pj": f"{tr.energy_pj:.9f}",
                        "spike0_first_ns": f"{tr.first_spikes_ns[0]:.9f}",
                        "spike1_first_ns": f"{tr.first_spikes_ns[1]:.9f}",
                        "spike2_first_ns": f"{tr.first_spikes_ns[2]:.9f}",
                        "spike3_first_ns": f"{tr.first_spikes_ns[3]:.9f}",
                        "spike0_target_ns": f"{tr.target_spikes_ns[0]:.9f}",
                        "spike1_target_ns": f"{tr.target_spikes_ns[1]:.9f}",
                        "spike2_target_ns": f"{tr.target_spikes_ns[2]:.9f}",
                        "spike3_target_ns": f"{tr.target_spikes_ns[3]:.9f}",
                        "spike0_count": str(tr.spike_counts[0]),
                        "spike1_count": str(tr.spike_counts[1]),
                        "spike2_count": str(tr.spike_counts[2]),
                        "spike3_count": str(tr.spike_counts[3]),
                        "eval_dir": str(tr.eval_dir),
                    }
                )

    final_params = {k: x[k] * param_specs[k].scale for k in x}
    final_energy_weight = energy_weight_for_step(args.iters - 1, args.iters)
    final_eval = evaluate_params(
        source_netlist_text=source_netlist_text,
        params=final_params,
        phase="final_train",
        out_root=out_dir,
        trace_delays_ns=train_trace_delays_ns,
        trace_target_map=trace_target_map,
        trace_expected_counts_map=trace_expected_counts_map,
        tstop_ns=args.tstop_ns,
        missing_penalty_ns2=args.missing_penalty_ns2,
        count_penalty_weight=args.count_penalty,
        order_penalty=args.order_penalty,
        order_margin_ns=args.order_margin_ns,
        energy_weight=final_energy_weight,
        energy_ref_pj=energy_ref_pj,
    )
    final_holdout = None
    if holdout_trace_delays_ns:
        final_holdout = evaluate_params(
            source_netlist_text=source_netlist_text,
            params=final_params,
            phase="final_holdout",
            out_root=out_dir,
            trace_delays_ns=holdout_trace_delays_ns,
            trace_target_map=trace_target_map,
            trace_expected_counts_map=trace_expected_counts_map,
            tstop_ns=args.tstop_ns,
            missing_penalty_ns2=args.missing_penalty_ns2,
            count_penalty_weight=args.count_penalty,
            order_penalty=args.order_penalty,
            order_margin_ns=args.order_margin_ns,
            energy_weight=final_energy_weight,
            energy_ref_pj=energy_ref_pj,
        )
    eval_records.append(final_eval)

    denom_final = max(final_eval.loss, 1e-12)
    eval_rows.append(
        {
            "iter": str(args.iters),
            "phase": "final",
            "loss": f"{final_eval.loss:.9f}",
            "timing_loss": f"{final_eval.timing_loss_mean:.9f}",
            "count_penalty": f"{final_eval.count_penalty_mean:.9f}",
            "order_penalty": f"{final_eval.order_penalty_mean:.9f}",
            "energy_penalty": f"{final_eval.energy_penalty_mean:.9f}",
            "timing_pct": f"{(100.0 * final_eval.timing_loss_mean / denom_final):.9f}",
            "count_pct": f"{(100.0 * final_eval.count_penalty_mean / denom_final):.9f}",
            "order_pct": f"{(100.0 * final_eval.order_penalty_mean / denom_final):.9f}",
            "energy_pct": f"{(100.0 * final_eval.energy_penalty_mean / denom_final):.9f}",
            "energy_weight": f"{final_energy_weight:.9f}",
            "energy_pj": f"{final_eval.energy_pj_mean:.9f}",
            "r_fb": f"{final_params['r_fb']:.9f}",
            "rleak": f"{final_params['rleak']:.9f}",
            "iin_amp": f"{final_params['iin_amp']:.9f}",
            "spike0_ns": f"{final_eval.first_spike_means_ns[0]:.9f}",
            "spike1_ns": f"{final_eval.first_spike_means_ns[1]:.9f}",
            "spike2_ns": f"{final_eval.first_spike_means_ns[2]:.9f}",
            "spike3_ns": f"{final_eval.first_spike_means_ns[3]:.9f}",
            "holdout_loss": "" if final_holdout is None else f"{final_holdout.loss:.9f}",
            "holdout_timing_loss": "" if final_holdout is None else f"{final_holdout.timing_loss_mean:.9f}",
            "holdout_energy_pj": "" if final_holdout is None else f"{final_holdout.energy_pj_mean:.9f}",
            "grad_r_fb_x": "",
            "grad_rleak_x": "",
            "grad_iin_amp_x": "",
            "update_r_fb_x": "",
            "update_rleak_x": "",
            "update_iin_amp_x": "",
        }
    )

    for tr in final_eval.trace_results:
        trace_rows.append(
            {
                "iter": str(args.iters),
                "phase": "final",
                "split": "train",
                "delay_ns": f"{tr.delay_ns:.9f}",
                "status": tr.status,
                "loss": f"{tr.total_loss:.9f}",
                "timing_loss": f"{tr.timing_loss:.9f}",
                "count_penalty": f"{tr.count_penalty:.9f}",
                "order_penalty": f"{tr.order_penalty:.9f}",
                "energy_penalty": f"{tr.energy_penalty:.9f}",
                "energy_pj": f"{tr.energy_pj:.9f}",
                "spike0_first_ns": f"{tr.first_spikes_ns[0]:.9f}",
                "spike1_first_ns": f"{tr.first_spikes_ns[1]:.9f}",
                "spike2_first_ns": f"{tr.first_spikes_ns[2]:.9f}",
                "spike3_first_ns": f"{tr.first_spikes_ns[3]:.9f}",
                "spike0_target_ns": f"{tr.target_spikes_ns[0]:.9f}",
                "spike1_target_ns": f"{tr.target_spikes_ns[1]:.9f}",
                "spike2_target_ns": f"{tr.target_spikes_ns[2]:.9f}",
                "spike3_target_ns": f"{tr.target_spikes_ns[3]:.9f}",
                "spike0_count": str(tr.spike_counts[0]),
                "spike1_count": str(tr.spike_counts[1]),
                "spike2_count": str(tr.spike_counts[2]),
                "spike3_count": str(tr.spike_counts[3]),
                "eval_dir": str(tr.eval_dir),
            }
        )
    if final_holdout is not None:
        for tr in final_holdout.trace_results:
            trace_rows.append(
                {
                    "iter": str(args.iters),
                    "phase": "final",
                    "split": "holdout",
                    "delay_ns": f"{tr.delay_ns:.9f}",
                    "status": tr.status,
                    "loss": f"{tr.total_loss:.9f}",
                    "timing_loss": f"{tr.timing_loss:.9f}",
                    "count_penalty": f"{tr.count_penalty:.9f}",
                    "order_penalty": f"{tr.order_penalty:.9f}",
                    "energy_penalty": f"{tr.energy_penalty:.9f}",
                    "energy_pj": f"{tr.energy_pj:.9f}",
                    "spike0_first_ns": f"{tr.first_spikes_ns[0]:.9f}",
                    "spike1_first_ns": f"{tr.first_spikes_ns[1]:.9f}",
                    "spike2_first_ns": f"{tr.first_spikes_ns[2]:.9f}",
                    "spike3_first_ns": f"{tr.first_spikes_ns[3]:.9f}",
                    "spike0_target_ns": f"{tr.target_spikes_ns[0]:.9f}",
                    "spike1_target_ns": f"{tr.target_spikes_ns[1]:.9f}",
                    "spike2_target_ns": f"{tr.target_spikes_ns[2]:.9f}",
                    "spike3_target_ns": f"{tr.target_spikes_ns[3]:.9f}",
                    "spike0_count": str(tr.spike_counts[0]),
                    "spike1_count": str(tr.spike_counts[1]),
                    "spike2_count": str(tr.spike_counts[2]),
                    "spike3_count": str(tr.spike_counts[3]),
                    "eval_dir": str(tr.eval_dir),
                }
            )

    with eval_csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(eval_rows[0].keys()))
        w.writeheader()
        w.writerows(eval_rows)

    with trace_csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(trace_rows[0].keys()))
        w.writeheader()
        w.writerows(trace_rows)

    make_loss_svg(loss_svg_path, eval_records)

    init_row = eval_rows[0]
    final_row = eval_rows[-1]

    def fmt_opt_float(text: str, digits: int = 6) -> str:
        if not text:
            return "n/a"
        return ("{0:." + str(digits) + "f}").format(float(text))

    summary_lines: List[str] = []
    summary_lines.append("# Temporal Gradient Learning Summary")
    summary_lines.append("")
    summary_lines.append("Finite-difference learning on transistor simulations (`neuro_tile4_coupled`).")
    summary_lines.append("")
    summary_lines.append("Claim scope:")
    summary_lines.append("- Classification: **method demo** (internal objective + limited delay-family generalization).")
    summary_lines.append("- Not yet an externally valid benchmark against matched digital training/eval protocol.")
    summary_lines.append("")
    summary_lines.append("Training objective:")
    summary_lines.append("- Match target first-spike times across trace delays.")
    summary_lines.append("- Penalize missing spikes and ordering violations.")
    summary_lines.append("- Add optional energy regularization term.")
    summary_lines.append("")
    summary_lines.append("Configuration:")
    summary_lines.append(f"- iterations: `{args.iters}`")
    summary_lines.append(f"- target mode: `{args.target_mode}`")
    summary_lines.append(f"- train trace delays (ns): `{','.join(f'{x:.3f}' for x in train_trace_delays_ns)}`")
    summary_lines.append(f"- holdout trace delays (ns): `{','.join(f'{x:.3f}' for x in holdout_trace_delays_ns) if holdout_trace_delays_ns else 'none'}`")
    summary_lines.append(f"- base target spikes (ns): `{','.join(f'{x:.3f}' for x in target_base)}`")
    if args.target_mode == "measured_anchor_shift":
        summary_lines.append(f"- target shift (ns): `{','.join(f'{x:.3f}' for x in target_shift)}`")
    else:
        summary_lines.append("- target shift (ns): `n/a (absolute mode)`")
    summary_lines.append(f"- target spike counts: `{','.join(str(x) for x in target_counts)}`")
    summary_lines.append(
        f"- penalties: missing=`{args.missing_penalty_ns2}`, count_weight=`{args.count_penalty}`, "
        f"order_weight=`{args.order_penalty}`, order_margin_ns=`{args.order_margin_ns}`"
    )
    if abs(energy_weight_start - energy_weight_end) < 1e-12:
        summary_lines.append(f"- energy weight schedule: constant `{energy_weight_start:.6f}`")
    else:
        summary_lines.append(
            f"- energy weight schedule: `{energy_weight_start:.6f} -> {energy_weight_end:.6f}`"
        )
    summary_lines.append(f"- anchor probe split: `{args.anchor_probe_split}`")
    summary_lines.append(f"- energy reference (pJ): `{energy_ref_pj:.6f}`")
    summary_lines.append("")
    summary_lines.append("Initial vs final:")
    summary_lines.append("")
    summary_lines.append("| State | train loss | holdout loss | r_fb | rleak | iin_amp | spike0 | spike1 | spike2 | spike3 | energy (pJ) |")
    summary_lines.append("|-------|------------|--------------|------|-------|---------|--------|--------|--------|--------|-------------|")
    summary_lines.append(
        f"| initial | {float(init_row['loss']):.6f} | {fmt_opt_float(init_row.get('holdout_loss', ''), 6)} | {float(init_row['r_fb']):.3f} | {float(init_row['rleak']):.3f} | {float(init_row['iin_amp']):.6f} | "
        f"{float(init_row['spike0_ns']):.3f} | {float(init_row['spike1_ns']):.3f} | {float(init_row['spike2_ns']):.3f} | {float(init_row['spike3_ns']):.3f} | {float(init_row['energy_pj']):.3f} |"
    )
    summary_lines.append(
        f"| final | {float(final_row['loss']):.6f} | {fmt_opt_float(final_row.get('holdout_loss', ''), 6)} | {float(final_row['r_fb']):.3f} | {float(final_row['rleak']):.3f} | {float(final_row['iin_amp']):.6f} | "
        f"{float(final_row['spike0_ns']):.3f} | {float(final_row['spike1_ns']):.3f} | {float(final_row['spike2_ns']):.3f} | {float(final_row['spike3_ns']):.3f} | {float(final_row['energy_pj']):.3f} |"
    )
    summary_lines.append("")
    summary_lines.append("Initial vs final term contribution (% of total loss):")
    summary_lines.append("")
    summary_lines.append("| State | timing % | count % | order % | energy % |")
    summary_lines.append("|-------|----------|---------|---------|----------|")
    summary_lines.append(
        f"| initial | {float(init_row['timing_pct']):.3f} | {float(init_row['count_pct']):.3f} | "
        f"{float(init_row['order_pct']):.3f} | {float(init_row['energy_pct']):.3f} |"
    )
    summary_lines.append(
        f"| final | {float(final_row['timing_pct']):.3f} | {float(final_row['count_pct']):.3f} | "
        f"{float(final_row['order_pct']):.3f} | {float(final_row['energy_pct']):.3f} |"
    )
    summary_lines.append("")
    if final_row.get("holdout_loss"):
        gap = float(final_row["holdout_loss"]) - float(final_row["loss"])
        summary_lines.append(f"- Final generalization gap (holdout-train): `{gap:.6f}`")
        summary_lines.append("")
    summary_lines.append("Per-iteration base points:")
    summary_lines.append("")
    summary_lines.append("| iter | train loss | holdout loss | timing | count_pen | order_pen | energy_pen | timing% | energy% | e_w | grad_r_fb_x | grad_rleak_x | grad_iin_amp_x |")
    summary_lines.append("|------|------------|--------------|--------|-----------|-----------|------------|---------|---------|-----|--------------|----------------|----------------|")
    for r in eval_rows:
        if not r["phase"].endswith("_train_base"):
            continue
        summary_lines.append(
            f"| {r['iter']} | {float(r['loss']):.6f} | {fmt_opt_float(r.get('holdout_loss', ''), 6)} | {float(r['timing_loss']):.6f} | {float(r['count_penalty']):.6f} | "
            f"{float(r['order_penalty']):.6f} | {float(r['energy_penalty']):.6f} | {float(r['timing_pct']):.3f} | {float(r['energy_pct']):.3f} | "
            f"{float(r['energy_weight']):.3f} | {float(r['grad_r_fb_x']):.6f} | {float(r['grad_rleak_x']):.6f} | {float(r['grad_iin_amp_x']):.6f} |"
        )
    summary_lines.append("")
    summary_lines.append("Artifacts:")
    summary_lines.append(f"- Eval CSV: `{eval_csv_path}`")
    summary_lines.append(f"- Trace CSV: `{trace_csv_path}`")
    summary_lines.append(f"- Loss plot: `{loss_svg_path}`")

    write_text(summary_md_path, "\n".join(summary_lines) + "\n")

    run_meta = {
        "netlist_source": str(args.netlist_source),
        "out_dir": str(out_dir),
        "iterations": args.iters,
        "target_mode": args.target_mode,
        "train_trace_delays_ns": train_trace_delays_ns,
        "holdout_trace_delays_ns": holdout_trace_delays_ns,
        "anchor_probe_split": args.anchor_probe_split,
        "anchor_probe_delays_ns": anchor_probe_delays_ns,
        "trace_delays_ns": all_trace_delays_ns,
        "trace_target_map": trace_target_map,
        "trace_expected_counts_map": trace_expected_counts_map,
        "target_base_ns": target_base,
        "target_shift_ns": target_shift,
        "initial_params": {
            "r_fb": args.init_r_fb,
            "rleak": args.init_rleak,
            "iin_amp": args.init_iin_amp,
        },
        "energy_ref_pj": energy_ref_pj,
        "energy_weight_start": energy_weight_start,
        "energy_weight_end": energy_weight_end,
        "final_params": final_params,
        "initial_loss": float(init_row["loss"]),
        "final_loss": float(final_row["loss"]),
    }
    write_text(out_dir / "run_metadata.json", json.dumps(run_meta, indent=2, sort_keys=True) + "\n")

    print("Temporal gradient training complete:")
    print(f"  summary: {summary_md_path}")
    print(f"  eval csv: {eval_csv_path}")
    print(f"  trace csv: {trace_csv_path}")
    print(f"  loss svg: {loss_svg_path}")


if __name__ == "__main__":
    main()
