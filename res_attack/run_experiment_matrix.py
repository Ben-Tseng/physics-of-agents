"""Run a filtered tranche of an experiment command matrix, stopping on failure."""

from __future__ import annotations

import argparse
import csv
import shlex
import subprocess
from pathlib import Path


def complete(row: dict) -> bool:
    output = Path(row["output_dir"])
    episodes = int(row["episodes"])
    return (output / "manifest.json").exists() and len(list(output.glob("*.json"))) == episodes + 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=Path("res_attack/power_screen_matrix.csv"))
    parser.add_argument("--model")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--label")
    args = parser.parse_args()
    with args.matrix.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if args.model:
        rows = [row for row in rows if row["model"] == args.model]
    if args.seed is not None:
        rows = [row for row in rows if int(row["seed"]) == args.seed]
    if args.label:
        rows = [row for row in rows if row["label"] == args.label]
    if not rows:
        raise SystemExit("no matrix rows matched the filters")

    for index, row in enumerate(rows, 1):
        if complete(row):
            print(f"[matrix {index}/{len(rows)}] complete; skipping {row['output_dir']}", flush=True)
            continue
        print(
            f"[matrix {index}/{len(rows)}] {row['model']} seed={row['seed']} "
            f"cell={row['label']} calls={row['estimated_calls']}",
            flush=True,
        )
        subprocess.run(shlex.split(row["command"]), check=True)
        if not complete(row):
            raise RuntimeError(f"job exited without complete outputs: {row['output_dir']}")
    print(f"completed {len(rows)} selected matrix jobs", flush=True)


if __name__ == "__main__":
    main()
