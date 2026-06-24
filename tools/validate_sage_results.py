#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path

REQUIRED = [
    "psm_id", "peptide", "proteins", "filename", "scannr", "rank", "label",
    "spectrum_q", "peptide_q", "protein_q", "protein_group_q"
]
QCOLS = ["spectrum_q", "peptide_q", "protein_q", "protein_group_q"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--results", required=True, type=Path)
    p.add_argument("--json-out", required=True, type=Path)
    a = p.parse_args()
    out = {"status": "partial", "validation": "fail", "error_code": "missing_required_input", "rows": 0, "missing_columns": REQUIRED, "q_columns_numeric": False}
    if not a.results.exists():
        a.json_out.parent.mkdir(parents=True, exist_ok=True)
        a.json_out.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps(out, indent=2))
        return 2
    with a.results.open(newline="") as fh:
        r = csv.DictReader(fh, delimiter="\t")
        cols = r.fieldnames or []
        out["missing_columns"] = [c for c in REQUIRED if c not in cols]
        okq = True
        n = 0
        for row in r:
            n += 1
            for c in QCOLS:
                try:
                    float(row.get(c, ""))
                except Exception:
                    okq = False
        out["rows"] = n
        out["q_columns_numeric"] = okq and n > 0
    if not out["missing_columns"] and out["q_columns_numeric"]:
        out.update({"status": "ok", "validation": "pass", "error_code": None})
    else:
        out["error_code"] = "verification_failed"
    a.json_out.parent.mkdir(parents=True, exist_ok=True)
    a.json_out.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 0 if out["validation"] == "pass" else 2

if __name__ == "__main__":
    raise SystemExit(main())
