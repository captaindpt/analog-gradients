#!/usr/bin/env python3
"""Generate softmax input vectors and reference outputs."""

import argparse
import csv
import json
import math
import random
from pathlib import Path
from typing import List


def softmax(xs: List[float], temperature: float) -> List[float]:
    if temperature <= 0:
        raise ValueError("temperature must be > 0")
    m = max(xs)
    exps = [math.exp((x - m) / temperature) for x in xs]
    s = sum(exps)
    if s == 0:
        return [0.0 for _ in xs]
    return [e / s for e in exps]


def quantize(vals: List[float], bits: int) -> List[float]:
    if bits <= 0:
        return vals
    levels = (1 << bits) - 1
    return [round(v * levels) / levels for v in vals]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate softmax vector CSV.")
    parser.add_argument("--n", type=int, default=4, help="softmax dimension")
    parser.add_argument("--mode", choices=["grid", "random"], default="random")
    parser.add_argument("--min", dest="min_val", type=float, default=-1.0)
    parser.add_argument("--max", dest="max_val", type=float, default=1.0)
    parser.add_argument("--step", type=float, default=0.5, help="grid step size")
    parser.add_argument("--samples", type=int, default=64, help="random samples")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--quantize-bits", type=int, default=8)
    parser.add_argument("--out", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.n <= 0:
        raise SystemExit("n must be >= 1")
    if args.max_val <= args.min_val:
        raise SystemExit("max must be greater than min")

    if args.out is None:
        out_path = Path("competition/data/nonlinearity") / f"softmax_vectors_n{args.n}.csv"
    else:
        out_path = args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    vectors: List[List[float]] = []
    if args.mode == "grid":
        vals = []
        v = args.min_val
        while v <= args.max_val + 1e-12:
            vals.append(round(v, 12))
            v += args.step
        total = len(vals) ** args.n
        if total > 50000:
            raise SystemExit(
                f"grid would create {total} vectors; reduce range/step or use random mode"
            )
        # Cartesian product
        vectors = [[]]
        for _ in range(args.n):
            vectors = [v + [x] for v in vectors for x in vals]
    else:
        rng = random.Random(args.seed)
        for _ in range(args.samples):
            vectors.append([rng.uniform(args.min_val, args.max_val) for _ in range(args.n)])

    fieldnames = ["vec_id"]
    fieldnames += [f"in{i}" for i in range(args.n)]
    fieldnames += [f"soft{i}" for i in range(args.n)]
    if args.quantize_bits and args.quantize_bits > 0:
        fieldnames += [f"soft_q{args.quantize_bits}_{i}" for i in range(args.n)]

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for idx, vec in enumerate(vectors):
            sm = softmax(vec, args.temperature)
            row = {"vec_id": idx}
            for i, v in enumerate(vec):
                row[f"in{i}"] = f"{v:.9f}"
            for i, v in enumerate(sm):
                row[f"soft{i}"] = f"{v:.9f}"
            if args.quantize_bits and args.quantize_bits > 0:
                q = quantize(sm, args.quantize_bits)
                for i, v in enumerate(q):
                    row[f"soft_q{args.quantize_bits}_{i}"] = f"{v:.9f}"
            writer.writerow(row)

    meta = {
        "n": args.n,
        "mode": args.mode,
        "min": args.min_val,
        "max": args.max_val,
        "step": args.step,
        "samples": args.samples,
        "seed": args.seed,
        "temperature": args.temperature,
        "quantize_bits": args.quantize_bits,
        "vectors": len(vectors),
        "csv": str(out_path),
    }
    meta_path = out_path.with_suffix(".json")
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"Wrote {len(vectors)} vectors to {out_path}")
    print(f"Metadata: {meta_path}")


if __name__ == "__main__":
    main()
