#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description="Create Sage config for PXD045741 one-file shard pilot.")
    ap.add_argument("--fasta", required=True, type=Path)
    ap.add_argument("--mzml", required=True, type=Path)
    ap.add_argument("--outdir", required=True, type=Path)
    ap.add_argument("--config", required=True, type=Path)
    args = ap.parse_args()

    missing = [str(p) for p in (args.fasta, args.mzml) if not p.exists()]
    if missing:
        raise SystemExit("Missing required input(s): " + ", ".join(missing))

    args.outdir.mkdir(parents=True, exist_ok=True)
    args.config.parent.mkdir(parents=True, exist_ok=True)

    config = {
        "database": {
            "bucket_size": 16384,
            "fragment_min_mz": 150.0,
            "fragment_max_mz": 1500.0,
            "enzyme": {"missed_cleavages": 1, "cleave_at": "KR", "restrict": "P"},
            "static_mods": {"C": 57.0216},
            "decoy_tag": "rev_",
            "generate_decoys": True,
            "fasta": str(args.fasta),
        },
        "deisotope": True,
        "chimera": False,
        "max_fragment_charge": 1,
        "report_psms": 1,
        "precursor_tol": {"ppm": [-50, 50]},
        "fragment_tol": {"ppm": [-10, 10]},
        "isotope_errors": [-1, 3],
        "wide_window": True,
        "predict_rt": False,
        "mzml_paths": [str(args.mzml)],
        "output_directory": str(args.outdir),
        "score_type": "SageHyperScore",
    }

    args.config.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ok", "config": str(args.config), "outdir": str(args.outdir)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
