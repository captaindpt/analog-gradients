#!/usr/bin/env python3
"""Generate 4x4 binary matmul transistor checkpoint assets."""

import argparse
import json
import random
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parent.parent
NETLIST_DIR = REPO_DIR / "netlists"
OCEAN_DIR = REPO_DIR / "ocean"

DEFAULT_A = [
    [1, 0, 1, 1],
    [0, 1, 1, 0],
    [1, 1, 0, 1],
    [1, 0, 0, 1],
]
DEFAULT_B = [
    [1, 1, 0, 1],
    [0, 1, 1, 0],
    [1, 0, 1, 1],
    [0, 1, 1, 1],
]
N = 4
A = [row[:] for row in DEFAULT_A]
B = [row[:] for row in DEFAULT_B]
Y = []


def expected_matrix():
    y = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            y[i][j] = sum(A[i][k] * B[k][j] for k in range(N))
    return y


def matrix_line(mat):
    return "[{}]".format(" ".join("[{}]".format(" ".join(str(v) for v in row)) for row in mat))


def matrix_list(mat):
    return "[{}]".format(",".join("[{}]".format(",".join(str(v) for v in row)) for row in mat))


def active_products(mat):
    return sum(sum(row) for row in mat)


def configure_matrices(density, seed):
    global A, B, Y
    if density is None:
        A = [row[:] for row in DEFAULT_A]
        B = [row[:] for row in DEFAULT_B]
    else:
        rng = random.Random(seed)
        A = [[1 if rng.random() < density else 0 for _ in range(N)] for _ in range(N)]
        B = [[1 if rng.random() < density else 0 for _ in range(N)] for _ in range(N)]
    Y = expected_matrix()


def chunks(items, n):
    for i in range(0, len(items), n):
        yield items[i : i + n]


def bit_params(prefix):
    names = []
    for i in range(N):
        for j in range(N):
            names.append("{}{}{}".format(prefix, i, j))
    return names


def render_param_defs():
    bits = bit_params("a") + bit_params("b")
    parts = ["{}={}".format(name, value_for(name)) for name in bits]
    return ["parameters " + " ".join(parts)]


def value_for(name):
    mat = A if name.startswith("a") else B
    i = int(name[1])
    j = int(name[2])
    return mat[i][j]


def render_voltage_param_defs():
    parts = []
    for name in bit_params("a") + bit_params("b"):
        parts.append("{}_v={}*vdd_val".format(name, name))
    return ["parameters " + " ".join(parts)]


def render_sources():
    lines = []
    for name in bit_params("a") + bit_params("b"):
        up = name.upper()
        lines.append(
            "V_{} ({}_in 0) vsource type=pulse val0=0 val1={}_v delay=10n rise=100p fall=100p width=20n period=200n".format(
                up, name, name
            )
        )
    return lines


def render_digital_netlist():
    lines = []
    lines.append("// matmul4x4_binary_digital.scs - Binary 4x4 matmul transistor checkpoint (digital path)")
    lines.append("// Multiply: AND. Accumulate: 4-input popcount -> 3-bit output per cell.")
    lines.append("")
    lines.append("simulator lang=spectre")
    lines.append("")
    lines.append("parameters vdd_val=1.8")
    lines.extend(render_param_defs())
    lines.extend(render_voltage_param_defs())
    lines.append("")
    lines.append("model nch mos1 type=n vto=0.4 kp=120u")
    lines.append("model pch mos1 type=p vto=-0.4 kp=40u")
    lines.append("")
    lines.append("V_VDD (vdd 0) vsource dc=vdd_val")
    lines.append("")
    lines.append("// Input event at 10ns. Zero-valued bits keep val1=0.")
    lines.extend(render_sources())
    lines.append("")
    lines.append("subckt nand2 (a b out vdd)")
    lines.append("    MP0 (out a vdd vdd) pch w=2u l=1u")
    lines.append("    MP1 (out b vdd vdd) pch w=2u l=1u")
    lines.append("    MN0 (out a mid 0) nch w=2u l=1u")
    lines.append("    MN1 (mid b 0 0) nch w=2u l=1u")
    lines.append("ends nand2")
    lines.append("")
    lines.append("subckt inverter (in out vdd)")
    lines.append("    MP0 (out in vdd vdd) pch w=2u l=1u")
    lines.append("    MN0 (out in 0 0) nch w=1u l=1u")
    lines.append("ends inverter")
    lines.append("")
    lines.append("subckt and2 (a b out vdd)")
    lines.append("    XN (a b n_int vdd) nand2")
    lines.append("    XI (n_int out vdd) inverter")
    lines.append("ends and2")
    lines.append("")
    lines.append("subckt xor2 (a b out vdd)")
    lines.append("    X1 (a b n1 vdd) nand2")
    lines.append("    X2 (a n1 n2 vdd) nand2")
    lines.append("    X3 (b n1 n3 vdd) nand2")
    lines.append("    X4 (n2 n3 out vdd) nand2")
    lines.append("ends xor2")
    lines.append("")
    lines.append("subckt half_adder (a b sum carry vdd)")
    lines.append("    XS (a b sum vdd) xor2")
    lines.append("    XC (a b carry vdd) and2")
    lines.append("ends half_adder")
    lines.append("")
    lines.append("subckt full_adder (a b cin sum cout vdd)")
    lines.append("    X0 (a b s0 vdd) xor2")
    lines.append("    X1 (s0 cin sum vdd) xor2")
    lines.append("    X2 (a b c0 vdd) and2")
    lines.append("    X3 (s0 cin c1 vdd) and2")
    lines.append("    X4 (c0 c1 cout vdd) xor2")
    lines.append("ends full_adder")
    lines.append("")
    lines.append("// Partial products + 4-input popcount per output.")
    for i in range(N):
        for j in range(N):
            lines.append("// y{}{} = sum_k(a{}k * bk{})".format(i, j, i, j))
            for k in range(N):
                lines.append(
                    "X_P{}_{}_{} (a{}{}_in b{}{}_in p_{}_{}_{} vdd) and2".format(
                        i, j, k, i, k, k, j, i, j, k
                    )
                )
            lines.append(
                "X_Y{}_{}_HA01 (p_{}_{}_0 p_{}_{}_1 y{}_{}_s01 y{}_{}_c01 vdd) half_adder".format(
                    i, j, i, j, i, j, i, j, i, j
                )
            )
            lines.append(
                "X_Y{}_{}_HA23 (p_{}_{}_2 p_{}_{}_3 y{}_{}_s23 y{}_{}_c23 vdd) half_adder".format(
                    i, j, i, j, i, j, i, j, i, j
                )
            )
            lines.append(
                "X_Y{}_{}_HA0 (y{}_{}_s01 y{}_{}_s23 y{}{}_b0 y{}_{}_c0 vdd) half_adder".format(
                    i, j, i, j, i, j, i, j, i, j
                )
            )
            lines.append(
                "X_Y{}_{}_FA1 (y{}_{}_c01 y{}_{}_c23 y{}_{}_c0 y{}{}_b1 y{}{}_b2 vdd) full_adder".format(
                    i, j, i, j, i, j, i, j, i, j, i, j
                )
            )
            lines.append("")

    lines.append("tran_test tran stop=120n")
    save_nodes = []
    for i in range(N):
        for j in range(N):
            for k in range(N):
                save_nodes.append("p_{}_{}_{}".format(i, j, k))
    for i in range(N):
        for j in range(N):
            save_nodes.append("y{}{}_b0".format(i, j))
            save_nodes.append("y{}{}_b1".format(i, j))
            save_nodes.append("y{}{}_b2".format(i, j))
    save_nodes.append("V_VDD:p")
    lines.append("save " + " ".join(save_nodes))
    lines.append("")
    (NETLIST_DIR / "matmul4x4_binary_digital.scs").write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_digital_ocean():
    lines = []
    lines.append("; test_matmul4x4_binary_digital.ocn")
    lines.append("; Verify 4x4 binary matmul digital transistor checkpoint.")
    lines.append("")
    lines.append('out = outfile("results/matmul4x4_binary_digital_test.txt" "w")')
    lines.append('fprintf(out "=== Binary 4x4 Matmul (Digital Baseline) Verification ===\\n")')
    lines.append('fprintf(out "Transistor checkpoint: AND partial products + popcount adders\\n")')
    lines.append('fprintf(out "Date: %s\\n\\n" getCurrentTime())')
    lines.append("")
    lines.append("simulator('spectre)")
    lines.append('openResults("results/matmul4x4_binary_digital/matmul4x4_binary_digital.raw")')
    lines.append('selectResult("tran_test-tran")')
    lines.append("")
    lines.append("procedure(firstCross(sig th dt tstart tstop)")
    lines.append("  let((ts prev curr frac tcross found)")
    lines.append("    tcross = nil")
    lines.append("    found = nil")
    lines.append("    ts = tstart")
    lines.append("    prev = value(sig ts)")
    lines.append("    ts = ts + dt")
    lines.append("    while(ts < tstop && !found")
    lines.append("      curr = value(sig ts)")
    lines.append("      if(prev < th && curr > th then")
    lines.append("        frac = (th - prev) / (curr - prev)")
    lines.append("        if(frac < 0 then frac = 0)")
    lines.append("        if(frac > 1 then frac = 1)")
    lines.append("        tcross = (ts - dt) + frac * dt")
    lines.append("        found = t")
    lines.append("      )")
    lines.append("      prev = curr")
    lines.append("      ts = ts + dt")
    lines.append("    )")
    lines.append("    tcross")
    lines.append("  )")
    lines.append(")")
    lines.append("")
    lines.append("procedure(bitAt(sig tsample vth_low vth_high)")
    lines.append("  let((vv)")
    lines.append("    vv = value(sig tsample)")
    lines.append("    if(vv < vth_low then")
    lines.append("      0")
    lines.append("    else")
    lines.append("      if(vv > vth_high then 1 else -1)")
    lines.append("    )")
    lines.append("  )")
    lines.append(")")
    lines.append("")

    wave_names = []
    for i in range(N):
        for j in range(N):
            for b in range(3):
                wn = "vy{}{}_b{}".format(i, j, b)
                sn = '"y{}{}_b{}"'.format(i, j, b)
                lines.append("{} = v({})".format(wn, sn))
                wave_names.append(wn)
    lines.append('idd = getData("V_VDD:p")')
    lines.append("")

    cond = " && ".join(wave_names + ["idd"])
    lines.append("if({} then".format(cond))
    lines.append("    pass = t")
    lines.append("    dt = 50p")
    lines.append("    t_in = 10n")
    lines.append("    t_sample = 25n")
    lines.append("    vdd = 1.8")
    lines.append("    vth_low = 0.2 * vdd")
    lines.append("    vth_high = 0.8 * vdd")
    lines.append("")

    for i in range(N):
        for j in range(N):
            for b in range(3):
                lines.append(
                    "    y{}{}_b{} = bitAt(vy{}{}_b{} t_sample vth_low vth_high)".format(
                        i, j, b, i, j, b
                    )
                )
    lines.append("")
    undef_checks = []
    for i in range(N):
        for j in range(N):
            for b in range(3):
                undef_checks.append("y{}{}_b{} < 0".format(i, j, b))
    lines.append("    if({} then".format(" || ".join(undef_checks)))
    lines.append('        fprintf(out "FAIL: one or more output bits are undefined at sample time\\n")')
    lines.append("        pass = nil")
    lines.append("    )")
    lines.append("")

    for i in range(N):
        for j in range(N):
            lines.append(
                "    y{}{} = y{}{}_b0 + 2*y{}{}_b1 + 4*y{}{}_b2".format(
                    i, j, i, j, i, j, i, j
                )
            )
    lines.append("")

    crossing_vars = []
    for i in range(N):
        for j in range(N):
            val = Y[i][j]
            bits = [(val >> 0) & 1, (val >> 1) & 1, (val >> 2) & 1]
            for b in range(3):
                if bits[b]:
                    cv = "t_y{}{}_b{}".format(i, j, b)
                    lines.append(
                        "    {} = firstCross(vy{}{}_b{} vth_high dt 1n 120n)".format(
                            cv, i, j, b
                        )
                    )
                    crossing_vars.append(cv)
    lines.append("")
    if crossing_vars:
        lines.append("    latest_valid_t = nil")
        lines.append("    foreach(tt list({})".format(" ".join(crossing_vars)))
        lines.append("      if(tt then")
        lines.append("        if(latest_valid_t then")
        lines.append("          if(tt > latest_valid_t then latest_valid_t = tt)")
        lines.append("        else")
        lines.append("          latest_valid_t = tt")
        lines.append("        )")
        lines.append("      else")
        lines.append("        pass = nil")
        lines.append('        fprintf(out "FAIL: missing expected rising edge in output bits\\n")')
        lines.append("      )")
        lines.append("    )")
    else:
        lines.append("    latest_valid_t = t_in")
    lines.append("")
    lines.append("    if(latest_valid_t then")
    lines.append("      latency_ns = (latest_valid_t - t_in) * 1e9")
    lines.append("    else")
    lines.append("      latency_ns = -1.0")
    lines.append("      pass = nil")
    lines.append("    )")
    lines.append("")

    lines.append("    t0 = 0n")
    lines.append("    t1 = 120n")
    lines.append("    energy = 0")
    lines.append("    ts = t0")
    lines.append("    prev_i = value(idd ts)")
    lines.append("    prev_t = ts")
    lines.append("    ts = ts + dt")
    lines.append("    while(ts <= t1")
    lines.append("      curr_i = value(idd ts)")
    lines.append("      p0 = -prev_i * vdd")
    lines.append("      p1 = -curr_i * vdd")
    lines.append("      energy = energy + 0.5 * (p0 + p1) * (ts - prev_t)")
    lines.append("      prev_i = curr_i")
    lines.append("      prev_t = ts")
    lines.append("      ts = ts + dt")
    lines.append("    )")
    lines.append("    e_per_op = energy / 112")
    lines.append("")
    lines.append('    fprintf(out "Stimulus matrices:\\n")')
    lines.append('    fprintf(out "  A = {}\\n")'.format(matrix_line(A)))
    lines.append('    fprintf(out "  B = {}\\n\\n")'.format(matrix_line(B)))
    lines.append('    fprintf(out "Expected output Y = {}\\n\\n")'.format(matrix_line(Y)))
    lines.append("")
    lines.append('    fprintf(out "Decoded output matrix:\\n")')
    for i in range(N):
        lines.append(
            '    fprintf(out "  row{}: %d %d %d %d\\n" y{}0 y{}1 y{}2 y{}3)'.format(
                i, i, i, i, i
            )
        )
    flat_vars = []
    for i in range(N):
        for j in range(N):
            flat_vars.append("y{}{}".format(i, j))
    lines.append(
        '    fprintf(out "\\nDecoded output vector: {}\\n\\n" {})'.format(
            " ".join(["%d"] * (N * N)),
            " ".join(flat_vars),
        )
    )
    lines.append('    fprintf(out "Latency to full output-valid: %.3f ns\\n" latency_ns)')
    lines.append('    fprintf(out "Total energy (0-120ns): %.6e J\\n" energy)')
    lines.append('    fprintf(out "Energy per operation (112 ops): %.6e J/op\\n\\n" e_per_op)')
    lines.append("")
    eq_checks = []
    for i in range(N):
        for j in range(N):
            eq_checks.append("y{}{} == {}".format(i, j, Y[i][j]))
    lines.append("    if({} then".format(" && ".join(eq_checks)))
    lines.append('      fprintf(out "OK: decoded outputs match expected 4x4 matrix\\n")')
    lines.append("    else")
    lines.append('      fprintf(out "FAIL: decoded outputs do not match expected 4x4 matrix\\n")')
    lines.append("      pass = nil")
    lines.append("    )")
    lines.append("")
    lines.append("    fprintf(out \"\\n\")")
    lines.append("    if(pass then")
    lines.append('      fprintf(out "=== PASS: Binary 4x4 digital matmul checkpoint verified ===\\n")')
    lines.append("    else")
    lines.append('      fprintf(out "=== FAIL: Binary 4x4 digital matmul checkpoint failed ===\\n")')
    lines.append("    )")
    lines.append("else")
    lines.append('    fprintf(out "ERROR: Could not read waveform data\\n")')
    lines.append(")")
    lines.append("")
    lines.append("close(out)")
    lines.append('printf("Done. Results in: ~/analog-gradients/results/matmul4x4_binary_digital_test.txt\\n")')
    lines.append("exit()")
    lines.append("")
    (OCEAN_DIR / "test_matmul4x4_binary_digital.ocn").write_text("\n".join(lines), encoding="utf-8")


def render_neuro_netlist():
    lines = []
    lines.append("// matmul4x4_binary_neuro.scs - Binary 4x4 matmul transistor checkpoint (neuro path)")
    lines.append("// Partial products via coincidence-like current summation, output via membrane integration.")
    lines.append("")
    lines.append("simulator lang=spectre")
    lines.append("")
    lines.append("parameters vdd_val=1.8 iin_amp=220u cmul=1p rmul=20k csum=700f rsum_leak=15M rsum_in=6k")
    lines.extend(render_param_defs())
    lines.append("")
    lines.append("model nch mos1 type=n vto=0.0 kp=120u")
    lines.append("model pch mos1 type=p vto=0.0 kp=40u")
    lines.append("model nch_cmp mos1 type=n vto=0.5 kp=120u")
    lines.append("model pch_cmp mos1 type=p vto=-0.5 kp=40u")
    lines.append("")
    lines.append("V_VDD (vdd 0) vsource dc=vdd_val")
    lines.append("")
    for i in range(N):
        for j in range(N):
            for k in range(N):
                mem = "mem_p_{}_{}_{}".format(i, j, k)
                lines.append("// p_{}_{}_{} = a{}{} * b{}{}".format(i, j, k, i, k, k, j))
                lines.append(
                    "I_P_{}_{}_{} (vdd {}) isource type=pulse val0=0 val1=(a{}{}*b{}{})*(2*iin_amp) delay=10n rise=100p fall=100p width=2n period=200n".format(
                        i, j, k, mem, i, k, k, j
                    )
                )
                lines.append("C_P_{}_{}_{} ({} 0) capacitor c=cmul".format(i, j, k, mem))
                lines.append("R_P_{}_{}_{} ({} 0) resistor r=rmul".format(i, j, k, mem))
                lines.append(
                    "MP_P_{}_{}_{}_1 (p_{}_{}_{}_n {} vdd vdd) pch_cmp w=2u l=1u".format(
                        i, j, k, i, j, k, mem
                    )
                )
                lines.append(
                    "MN_P_{}_{}_{}_1 (p_{}_{}_{}_n {} 0 0) nch_cmp w=1u l=1u".format(
                        i, j, k, i, j, k, mem
                    )
                )
                lines.append(
                    "MP_P_{}_{}_{}_2 (p_{}_{}_{} p_{}_{}_{}_n vdd vdd) pch w=2u l=1u".format(
                        i, j, k, i, j, k, i, j, k
                    )
                )
                lines.append(
                    "MN_P_{}_{}_{}_2 (p_{}_{}_{} p_{}_{}_{}_n 0 0) nch w=1u l=1u".format(
                        i, j, k, i, j, k, i, j, k
                    )
                )
                lines.append("")

    lines.append("// Output accumulation membranes: yij = sum_k p_ij_k")
    for i in range(N):
        for j in range(N):
            for k in range(N):
                lines.append(
                    "R_P_{}_{}_{}_Y (p_{}_{}_{} y{}{}_mem) resistor r=rsum_in".format(
                        i, j, k, i, j, k, i, j
                    )
                )
            lines.append("C_Y{}{} (y{}{}_mem 0) capacitor c=csum".format(i, j, i, j))
            lines.append("R_Y{}{}_LEAK (y{}{}_mem 0) resistor r=rsum_leak".format(i, j, i, j))
            lines.append("")

    lines.append("tran_test tran stop=120n")
    save_nodes = []
    for i in range(N):
        for j in range(N):
            for k in range(N):
                save_nodes.append("p_{}_{}_{}".format(i, j, k))
    for i in range(N):
        for j in range(N):
            save_nodes.append("y{}{}_mem".format(i, j))
    save_nodes.append("V_VDD:p")
    lines.append("save " + " ".join(save_nodes))
    lines.append("")
    (NETLIST_DIR / "matmul4x4_binary_neuro.scs").write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_neuro_ocean():
    lines = []
    lines.append("; test_matmul4x4_binary_neuro.ocn")
    lines.append("; Verify 4x4 binary matmul neuro transistor checkpoint.")
    lines.append("")
    lines.append('out = outfile("results/matmul4x4_binary_neuro_test.txt" "w")')
    lines.append('fprintf(out "=== Binary 4x4 Matmul (Neuro Path) Verification ===\\n")')
    lines.append('fprintf(out "Transistor checkpoint: coincidence products + membrane accumulation\\n")')
    lines.append('fprintf(out "Date: %s\\n\\n" getCurrentTime())')
    lines.append("")
    lines.append("simulator('spectre)")
    lines.append('openResults("results/matmul4x4_binary_neuro/matmul4x4_binary_neuro.raw")')
    lines.append('selectResult("tran_test-tran")')
    lines.append("")
    lines.append("procedure(countRising(sig th dt tstart tstop)")
    lines.append("  let((cnt ts prev curr)")
    lines.append("    cnt = 0")
    lines.append("    ts = tstart")
    lines.append("    prev = value(sig ts)")
    lines.append("    ts = ts + dt")
    lines.append("    while(ts < tstop")
    lines.append("      curr = value(sig ts)")
    lines.append("      if(prev < th && curr > th then")
    lines.append("        cnt = cnt + 1")
    lines.append("      )")
    lines.append("      prev = curr")
    lines.append("      ts = ts + dt")
    lines.append("    )")
    lines.append("    cnt")
    lines.append("  )")
    lines.append(")")
    lines.append("")
    lines.append("procedure(firstCross(sig th dt tstart tstop)")
    lines.append("  let((ts prev curr frac tcross found)")
    lines.append("    tcross = nil")
    lines.append("    found = nil")
    lines.append("    ts = tstart")
    lines.append("    prev = value(sig ts)")
    lines.append("    ts = ts + dt")
    lines.append("    while(ts < tstop && !found")
    lines.append("      curr = value(sig ts)")
    lines.append("      if(prev < th && curr > th then")
    lines.append("        frac = (th - prev) / (curr - prev)")
    lines.append("        if(frac < 0 then frac = 0)")
    lines.append("        if(frac > 1 then frac = 1)")
    lines.append("        tcross = (ts - dt) + frac * dt")
    lines.append("        found = t")
    lines.append("      )")
    lines.append("      prev = curr")
    lines.append("      ts = ts + dt")
    lines.append("    )")
    lines.append("    tcross")
    lines.append("  )")
    lines.append(")")
    lines.append("")

    p_vars = []
    for i in range(N):
        for j in range(N):
            for k in range(N):
                nm = "vp_{}_{}_{}".format(i, j, k)
                lines.append('{} = v("p_{}_{}_{}")'.format(nm, i, j, k))
                p_vars.append(nm)
    y_vars = []
    for i in range(N):
        for j in range(N):
            nm = "vy{}{}".format(i, j)
            lines.append('{} = v("y{}{}_mem")'.format(nm, i, j))
            y_vars.append(nm)
    lines.append('idd = getData("V_VDD:p")')
    lines.append("")

    cond = " && ".join(p_vars + y_vars + ["idd"])
    lines.append("if({} then".format(cond))
    lines.append("    pass = t")
    lines.append("    dt = 100p")
    lines.append("    t_in = 10n")
    lines.append("    total_partial_spikes = 0")
    lines.append("    latest_active_t = nil")
    lines.append("")

    for i in range(N):
        for j in range(N):
            for k in range(N):
                wv = "vp_{}_{}_{}".format(i, j, k)
                lines.append("    p_{}_{}_{}_min = ymin({})".format(i, j, k, wv))
                lines.append("    p_{}_{}_{}_max = ymax({})".format(i, j, k, wv))
                lines.append("    if(p_{}_{}_{}_max > 0.4 then".format(i, j, k))
                lines.append(
                    "      p_{}_{}_{}_th = (p_{}_{}_{}_max + p_{}_{}_{}_min)/2".format(
                        i, j, k, i, j, k, i, j, k
                    )
                )
                lines.append(
                    "      p_{}_{}_{}_cnt = countRising({} p_{}_{}_{}_th dt 1n 120n)".format(
                        i, j, k, wv, i, j, k
                    )
                )
                lines.append(
                    "      p_{}_{}_{}_t = firstCross({} p_{}_{}_{}_th dt 1n 120n)".format(
                        i, j, k, wv, i, j, k
                    )
                )
                lines.append("    else")
                lines.append("      p_{}_{}_{}_cnt = 0".format(i, j, k))
                lines.append("      p_{}_{}_{}_t = nil".format(i, j, k))
                lines.append("    )")
                lines.append("    total_partial_spikes = total_partial_spikes + p_{}_{}_{}_cnt".format(i, j, k))
                lines.append("    if(p_{}_{}_{}_t then".format(i, j, k))
                lines.append("      if(latest_active_t then")
                lines.append("        if(p_{}_{}_{}_t > latest_active_t then latest_active_t = p_{}_{}_{}_t)".format(i, j, k, i, j, k))
                lines.append("      else")
                lines.append("        latest_active_t = p_{}_{}_{}_t".format(i, j, k))
                lines.append("      )")
                lines.append("    )")
                lines.append("")

    for i in range(N):
        for j in range(N):
            terms = ["p_{}_{}_{}_cnt".format(i, j, k) for k in range(N)]
            lines.append("    y{}{}_est = {}".format(i, j, " + ".join(terms)))
            lines.append("    y{}{}_max = ymax(vy{}{})".format(i, j, i, j))
    lines.append("")
    lines.append("    if(latest_active_t then")
    lines.append("      latency_ns = (latest_active_t - t_in) * 1e9")
    lines.append("    else")
    lines.append("      if(total_partial_spikes == 0 then")
    lines.append("        latency_ns = 0.0")
    lines.append("      else")
    lines.append("        latency_ns = -1.0")
    lines.append("        pass = nil")
    lines.append('        fprintf(out "FAIL: could not determine full-output latency\\n")')
    lines.append("      )")
    lines.append("    )")
    lines.append("")
    lines.append("    t0 = 0n")
    lines.append("    t1 = 120n")
    lines.append("    energy = 0")
    lines.append("    ts = t0")
    lines.append("    prev_i = value(idd ts)")
    lines.append("    prev_t = ts")
    lines.append("    ts = ts + dt")
    lines.append("    while(ts <= t1")
    lines.append("      curr_i = value(idd ts)")
    lines.append("      p0 = -prev_i * 1.8")
    lines.append("      p1 = -curr_i * 1.8")
    lines.append("      energy = energy + 0.5 * (p0 + p1) * (ts - prev_t)")
    lines.append("      prev_i = curr_i")
    lines.append("      prev_t = ts")
    lines.append("      ts = ts + dt")
    lines.append("    )")
    lines.append("    energy_per_op = energy / 112")
    lines.append("    spike_energy_est = total_partial_spikes * 3.27e-12")
    lines.append("")
    lines.append('    fprintf(out "Stimulus matrices:\\n")')
    lines.append('    fprintf(out "  A = {}\\n")'.format(matrix_line(A)))
    lines.append('    fprintf(out "  B = {}\\n\\n")'.format(matrix_line(B)))
    lines.append('    fprintf(out "Expected output Y = {}\\n\\n")'.format(matrix_line(Y)))
    lines.append("")
    lines.append('    fprintf(out "Decoded output from partial products:\\n")')
    for i in range(N):
        lines.append(
            '    fprintf(out "  row{}: %d %d %d %d\\n" y{}0_est y{}1_est y{}2_est y{}3_est)'.format(
                i, i, i, i, i
            )
        )
    flat_est = []
    for i in range(N):
        for j in range(N):
            flat_est.append("y{}{}_est".format(i, j))
    lines.append(
        '    fprintf(out "\\nDecoded output vector: {}\\n\\n" {})'.format(
            " ".join(["%d"] * (N * N)),
            " ".join(flat_est),
        )
    )
    lines.append('    fprintf(out "Total partial spikes: %d\\n" total_partial_spikes)')
    lines.append('    fprintf(out "Latency to full output-valid: %.3f ns\\n" latency_ns)')
    lines.append('    fprintf(out "Total energy (0-120ns): %.6e J\\n" energy)')
    lines.append('    fprintf(out "Energy per operation (112 ops): %.6e J/op\\n" energy_per_op)')
    lines.append('    fprintf(out "Spike-model energy estimate (3.27 pJ/spike): %.6e J\\n\\n" spike_energy_est)')
    lines.append("")
    eq_checks = []
    for i in range(N):
        for j in range(N):
            eq_checks.append("y{}{}_est == {}".format(i, j, Y[i][j]))
    lines.append("    if({} then".format(" && ".join(eq_checks)))
    lines.append('      fprintf(out "OK: decoded outputs match expected 4x4 matrix\\n")')
    lines.append("    else")
    lines.append('      fprintf(out "FAIL: decoded outputs do not match expected 4x4 matrix\\n")')
    lines.append("      pass = nil")
    lines.append("    )")
    lines.append("")
    lines.append("    fprintf(out \"\\n\")")
    lines.append("    if(pass then")
    lines.append('      fprintf(out "=== PASS: Binary 4x4 neuro matmul checkpoint verified ===\\n")')
    lines.append("    else")
    lines.append('      fprintf(out "=== FAIL: Binary 4x4 neuro matmul checkpoint failed ===\\n")')
    lines.append("    )")
    lines.append("else")
    lines.append('    fprintf(out "ERROR: Could not read waveform data\\n")')
    lines.append(")")
    lines.append("")
    lines.append("close(out)")
    lines.append('printf("Done. Results in: ~/analog-gradients/results/matmul4x4_binary_neuro_test.txt\\n")')
    lines.append("exit()")
    lines.append("")
    (OCEAN_DIR / "test_matmul4x4_binary_neuro.ocn").write_text("\n".join(lines), encoding="utf-8")


def write_metadata(path, density, seed):
    data = {
        "n": N,
        "density": density,
        "seed": seed,
        "A": A,
        "B": B,
        "Y": Y,
        "active_products": active_products(Y),
    }
    Path(path).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def parse_args():
    parser = argparse.ArgumentParser(description="Generate 4x4 binary matmul checkpoint assets.")
    parser.add_argument(
        "--density",
        type=float,
        default=None,
        help="Optional Bernoulli density in [0,1] for random A/B generation.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=1,
        help="Random seed used when --density is provided.",
    )
    parser.add_argument(
        "--metadata-out",
        default=None,
        help="Optional path to write generated A/B/Y metadata JSON.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.density is not None and (args.density < 0.0 or args.density > 1.0):
        raise SystemExit("--density must be in [0,1]")
    configure_matrices(args.density, args.seed)
    render_digital_netlist()
    render_digital_ocean()
    render_neuro_netlist()
    render_neuro_ocean()
    if args.metadata_out:
        write_metadata(args.metadata_out, args.density, args.seed)
    mode = "default-checkpoint" if args.density is None else "random-density"
    print(
        "Generated 4x4 checkpoint assets (mode={}, density={}, seed={}, active_products={}).".format(
            mode,
            "default" if args.density is None else "{:.4f}".format(args.density),
            args.seed,
            active_products(Y),
        )
    )


if __name__ == "__main__":
    main()
