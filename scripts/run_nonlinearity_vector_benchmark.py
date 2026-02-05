#!/usr/bin/env python3
"""Run per-vector nonlinearity benchmark on a Spectre netlist."""

import argparse
import csv
import json
import re
import shutil
import subprocess
from pathlib import Path
from statistics import mean
from typing import Dict, List, Optional, Sequence, Tuple


def parse_list(raw: str) -> List[str]:
    return [tok.strip() for tok in raw.split(",") if tok.strip()]


def parse_kv_list(raw: str) -> Dict[str, float]:
    if not raw:
        return {}
    out: Dict[str, float] = {}
    for tok in raw.split(","):
        tok = tok.strip()
        if not tok:
            continue
        if "=" not in tok:
            raise SystemExit(f"Invalid extra param '{tok}', expected key=value.")
        k, v = tok.split("=", 1)
        out[k.strip()] = float(v.strip())
    return out


def update_param_line(param_line: str, key: str, value: str) -> str:
    pat = rf"\b{re.escape(key)}=[^ ]+"
    if re.search(pat, param_line):
        return re.sub(pat, f"{key}={value}", param_line)
    return f"{param_line} {key}={value}"


def ensure_save_nodes(netlist: str, nodes: Sequence[str]) -> str:
    m = re.search(r"^save\s+.+$", netlist, flags=re.MULTILINE)
    if not m:
        raise SystemExit("Missing save line in netlist.")
    save_line = m.group(0)
    for node in nodes:
        if node not in save_line:
            save_line = save_line + f" {node}"
    return netlist[: m.start()] + save_line + netlist[m.end() :]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run_cmd(cmd: Sequence[str], cwd: Path, stdout: Optional[Path] = None) -> int:
    if stdout is None:
        proc = subprocess.run(cmd, cwd=cwd)
        return proc.returncode
    with stdout.open("w", encoding="utf-8") as f:
        proc = subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT)
    return proc.returncode


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


def build_metrics_ocn(
    raw_dir: Path,
    out_file: Path,
    output_nodes: Sequence[str],
    target_vals: Optional[Sequence[float]],
    tstop_ns: float,
    t_eval_ns: float,
    t_start_ns: float,
    energy_dt_ps: float,
    vdd_node: str,
    vdd_source: str,
    output_scale: float,
    output_offset: float,
    output_invert: bool,
    latency_tol: Optional[float],
    latency_hold_ns: float,
) -> str:
    node_lines = "\n".join([f'vraw{i} = v("{n}")' for i, n in enumerate(output_nodes)])
    out_lines = []
    for i, _ in enumerate(output_nodes):
        out_lines.append(f'  fprintf(out "raw{i}=%.9f\\n" value(vraw{i} t_eval))')
        out_lines.append(f'  fprintf(out "out{i}=%.9f\\n" value(vout{i} t_eval))')
    target_lines = ""
    latency_proc = ""
    latency_lines = ""
    if target_vals is not None and latency_tol is not None:
        target_lines = "\n".join([f"  targ{i} = {v:.9f}" for i, v in enumerate(target_vals)])
        latency_proc = f"""
procedure(firstWithin(sig targ tol dt tstart tstop hold_ns)
  let((ts prev curr hold_steps ok tcross)
    tcross = -1
    hold_steps = max(1 round(hold_ns / dt))
    ts = tstart
    prev = value(sig ts)
    ts = ts + dt
    while(ts < tstop && tcross < 0
      curr = value(sig ts)
      if(abs(curr - targ) <= tol then
        ok = 1
        let((i tcheck vcheck)
          i = 0
          tcheck = ts
          while(i < hold_steps
            vcheck = value(sig tcheck)
            if(abs(vcheck - targ) > tol then ok = 0)
            tcheck = tcheck + dt
            i = i + 1
          )
        )
        if(ok == 1 then tcross = ts)
      )
      prev = curr
      ts = ts + dt
    )
    tcross
  )
)
"""
        latency_lines = "\n".join(
            [
                f'  lat{i} = firstWithin(vout{i} targ{i} {latency_tol} dt t_start t_stop {latency_hold_ns}n)'
                for i, _ in enumerate(output_nodes)
            ]
            + [f'  fprintf(out "lat{i}_ns=%.9f\\n" lat{i}*1e9)' for i, _ in enumerate(output_nodes)]
        )

    transform_lines = ["  scale = {}".format(output_scale), "  offset = {}".format(output_offset)]
    if output_invert:
        transform_lines += [f"  vout{i} = scale * (offset - vraw{i})" for i in range(len(output_nodes))]
    else:
        transform_lines += [f"  vout{i} = scale * (vraw{i} - offset)" for i in range(len(output_nodes))]

    return f"""; auto-generated nonlinearity metrics extraction
out = outfile("{out_file.as_posix()}" "w")

simulator('spectre)
openResults("{raw_dir.as_posix()}")
selectResult("tran_test-tran")

{node_lines}
idd = getData("{vdd_source}:p")
vvdd = v("{vdd_node}")

if({ " && ".join([f"vraw{i}" for i in range(len(output_nodes))] + ["idd", "vvdd"]) } then
  dt = {energy_dt_ps}p
  t_start = {t_start_ns}n
  t_stop = {tstop_ns}n
  t_eval = {t_eval_ns}n

{target_lines}
{latency_proc}
{chr(10).join(transform_lines)}

  energy = 0
  ts = t_start
  prev_i = value(idd ts)
  prev_v = value(vvdd ts)
  prev_t = ts
  ts = ts + dt
  while(ts <= t_stop
    curr_i = value(idd ts)
    curr_v = value(vvdd ts)
    p0 = -prev_i * prev_v
    p1 = -curr_i * curr_v
    energy = energy + 0.5 * (p0 + p1) * (ts - prev_t)
    prev_i = curr_i
    prev_v = curr_v
    prev_t = ts
    ts = ts + dt
  )

  fprintf(out "status=OK\\n")
{chr(10).join(out_lines)}
{latency_lines}
  fprintf(out "energy_j=%.12e\\n" energy)
else
  fprintf(out "status=ERROR\\n")
)

close(out)
exit()
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Run nonlinearity vector benchmark.")
    parser.add_argument("--netlist", type=Path, required=True)
    parser.add_argument("--vectors-csv", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--input-params", type=str, required=True)
    parser.add_argument("--output-nodes", type=str, required=True)
    parser.add_argument("--input-cols", type=str, default="")
    parser.add_argument("--target-cols", type=str, default="")
    parser.add_argument("--tstop-ns", type=float, default=50.0)
    parser.add_argument("--eval-time-ns", type=float, default=50.0)
    parser.add_argument("--tstart-ns", type=float, default=0.0)
    parser.add_argument("--energy-dt-ps", type=float, default=100.0)
    parser.add_argument("--vdd-node", type=str, default="vdd")
    parser.add_argument("--vdd-source", type=str, default="V_VDD")
    parser.add_argument("--vdd-val", type=float, default=None)
    parser.add_argument("--extra-params", type=str, default="")
    parser.add_argument("--output-scale", type=float, default=1.0)
    parser.add_argument("--output-offset", type=float, default=0.0)
    parser.add_argument("--output-invert", action="store_true")
    parser.add_argument("--accuracy-tol", type=float, default=0.02)
    parser.add_argument("--latency-tol", type=float, default=None)
    parser.add_argument("--latency-hold-ns", type=float, default=0.0)
    parser.add_argument("--latency-max-ns", type=float, default=None)
    parser.add_argument("--model-class", choices=["toy", "pdk"], default="toy")
    args = parser.parse_args()

    if shutil.which("spectre") is None or shutil.which("ocean") is None:
        raise SystemExit("spectre/ocean not found. Run `source setup_cadence.sh` first.")

    input_params = parse_list(args.input_params)
    output_nodes = parse_list(args.output_nodes)
    if not input_params or not output_nodes:
        raise SystemExit("input-params and output-nodes are required")

    input_cols = parse_list(args.input_cols) if args.input_cols else [f"in{i}" for i in range(len(input_params))]
    target_cols = parse_list(args.target_cols) if args.target_cols else [f"soft{i}" for i in range(len(output_nodes))]
    extra_params = parse_kv_list(args.extra_params)

    if len(input_cols) != len(input_params):
        raise SystemExit("input-cols and input-params must have same length")
    if target_cols and len(target_cols) != len(output_nodes):
        raise SystemExit("target-cols must match output-nodes length")

    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    netlist_text = args.netlist.read_text(encoding="utf-8")
    m = re.search(r"^parameters\\s+.+$", netlist_text, flags=re.MULTILINE)
    if not m:
        raise SystemExit("Netlist missing parameters line.")

    netlist_text = ensure_save_nodes(
        netlist_text,
        list(output_nodes) + [args.vdd_node, f"{args.vdd_source}:p"],
    )

    results_csv = out_dir / "nonlinearity_results.csv"
    summary_md = out_dir / "nonlinearity_summary.md"
    run_meta = out_dir / "run_metadata.json"

    vectors = []
    with args.vectors_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vectors.append(row)
    if not vectors:
        raise SystemExit("vectors csv is empty")

    rows: List[Dict[str, str]] = []
    errors: List[float] = []
    energies: List[float] = []
    latencies: List[float] = []
    pass_count = 0

    for idx, vec in enumerate(vectors):
        vec_id = vec.get("vec_id", str(idx))
        params_line = m.group(0)
        for col, param in zip(input_cols, input_params):
            if col not in vec:
                raise SystemExit(f"Missing column {col} in vectors CSV")
            params_line = update_param_line(params_line, param, f"{float(vec[col]):.9f}")
        if args.vdd_val is not None:
            params_line = update_param_line(params_line, "vdd_val", f"{args.vdd_val:.6f}")
        for k, v in extra_params.items():
            params_line = update_param_line(params_line, k, f"{v:.9f}")
        vec_netlist = netlist_text[: m.start()] + params_line + netlist_text[m.end() :]

        vec_dir = out_dir / f"vec_{vec_id}"
        vec_dir.mkdir(parents=True, exist_ok=True)
        netlist_path = vec_dir / args.netlist.name
        write_text(netlist_path, vec_netlist)

        raw_dir = vec_dir / f"{args.netlist.stem}.raw"
        spectre_log = vec_dir / "spectre.log"
        spectre_stdout = vec_dir / "spectre_stdout.log"
        ocean_log = vec_dir / "ocean.log"
        metrics_path = vec_dir / "metrics.txt"
        ocn_path = vec_dir / "extract_metrics.ocn"

        rc = run_cmd(
            ["spectre", netlist_path.name, "-raw", raw_dir.name, "+log", spectre_log.name],
            cwd=vec_dir,
            stdout=spectre_stdout,
        )
        status = "PASS"
        if rc != 0:
            status = "SPECTRE_FAIL"
        elif "completes with 0 errors" not in spectre_log.read_text(encoding="utf-8", errors="ignore"):
            status = "SPECTRE_LOG_FAIL"

        target_vals = None
        if target_cols:
            target_vals = [float(vec[c]) for c in target_cols]
        ocn_text = build_metrics_ocn(
            raw_dir=raw_dir,
            out_file=metrics_path,
            output_nodes=output_nodes,
            target_vals=target_vals,
            tstop_ns=args.tstop_ns,
            t_eval_ns=args.eval_time_ns,
            t_start_ns=args.tstart_ns,
            energy_dt_ps=args.energy_dt_ps,
            vdd_node=args.vdd_node,
            vdd_source=args.vdd_source,
            output_scale=args.output_scale,
            output_offset=args.output_offset,
            output_invert=args.output_invert,
            latency_tol=args.latency_tol,
            latency_hold_ns=args.latency_hold_ns,
        )
        write_text(ocn_path, ocn_text)

        if status == "PASS":
            rc_ocean = run_cmd(["bash", "-lc", f"ocean -nograph < '{ocn_path.name}'"], cwd=vec_dir, stdout=ocean_log)
            metrics = parse_metrics(metrics_path)
            if rc_ocean != 0 or metrics.get("status") != "OK":
                status = "OCEAN_FAIL"
        else:
            metrics = {}

        outputs: List[float] = []
        for i in range(len(output_nodes)):
            outputs.append(float(metrics.get(f"out{i}", "nan")))
        energy_j = float(metrics.get("energy_j", "nan"))
        energy_pj = energy_j * 1e12 if energy_j == energy_j else float("nan")

        vec_error = float("nan")
        lats: List[float] = []
        if target_vals is not None and all(o == o for o in outputs):
            errs = [abs(o - t) for o, t in zip(outputs, target_vals)]
            vec_error = max(errs) if errs else float("nan")
        if args.latency_tol is not None:
            for i in range(len(output_nodes)):
                lat_ns = float(metrics.get(f"lat{i}_ns", "-1"))
                lats.append(lat_ns)

        pass_flag = status == "PASS"
        if pass_flag and vec_error == vec_error and vec_error > args.accuracy_tol:
            pass_flag = False
            status = "ACCURACY_FAIL"
        if pass_flag and args.latency_max_ns is not None and lats:
            max_lat = max(lats)
            if max_lat < 0 or max_lat > args.latency_max_ns:
                pass_flag = False
                status = "LATENCY_FAIL"

        row = {
            "vec_id": vec_id,
            "status": status,
            "energy_pj": f"{energy_pj:.6f}" if energy_pj == energy_pj else "",
            "l_inf_error": f"{vec_error:.9f}" if vec_error == vec_error else "",
        }
        for col in input_cols:
            row[col] = vec[col]
        for i, out in enumerate(outputs):
            row[f"out{i}"] = f"{out:.9f}" if out == out else ""
            raw = metrics.get(f"raw{i}")
            if raw is not None:
                try:
                    row[f"raw{i}"] = f"{float(raw):.9f}"
                except ValueError:
                    row[f"raw{i}"] = raw
        if target_vals is not None:
            for i, t in enumerate(target_vals):
                row[f"target{i}"] = f"{t:.9f}"
        if lats:
            for i, lat in enumerate(lats):
                row[f"lat{i}_ns"] = f"{lat:.9f}"
        rows.append(row)

        if pass_flag:
            pass_count += 1
        if energy_pj == energy_pj:
            energies.append(energy_pj)
        if vec_error == vec_error:
            errors.append(vec_error)
        if lats:
            for lat in lats:
                if lat >= 0:
                    latencies.append(lat)

    fieldnames = list(rows[0].keys()) if rows else []
    with results_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    summary = [
        "# Nonlinearity Benchmark Summary",
        "",
        f"- netlist: `{args.netlist}`",
        f"- vectors: `{args.vectors_csv}`",
        f"- model class: `{args.model_class}`",
        f"- vectors: `{len(rows)}`",
        f"- pass: `{pass_count}/{len(rows)}`",
        f"- energy mean (pJ): `{mean(energies):.6f}`" if energies else "- energy mean (pJ): `n/a`",
        f"- l_inf mean: `{mean(errors):.6f}`" if errors else "- l_inf mean: `n/a`",
        f"- latency mean (ns): `{mean(latencies):.6f}`" if latencies else "- latency mean (ns): `n/a`",
    ]
    summary_md.write_text("\n".join(summary) + "\n", encoding="utf-8")

    run_meta.write_text(
        json.dumps(
            {
                "netlist": str(args.netlist),
                "vectors": str(args.vectors_csv),
                "input_params": input_params,
                "output_nodes": output_nodes,
                "input_cols": input_cols,
                "target_cols": target_cols,
                "tstop_ns": args.tstop_ns,
                "eval_time_ns": args.eval_time_ns,
                "energy_dt_ps": args.energy_dt_ps,
                "vdd_node": args.vdd_node,
                "vdd_source": args.vdd_source,
                "extra_params": extra_params,
                "output_scale": args.output_scale,
                "output_offset": args.output_offset,
                "output_invert": args.output_invert,
                "accuracy_tol": args.accuracy_tol,
                "latency_tol": args.latency_tol,
                "latency_hold_ns": args.latency_hold_ns,
                "latency_max_ns": args.latency_max_ns,
                "model_class": args.model_class,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Wrote {results_csv}")
    print(f"Wrote {summary_md}")
    print(f"Wrote {run_meta}")


if __name__ == "__main__":
    main()
