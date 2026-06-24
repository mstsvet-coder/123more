#!/usr/bin/env python3
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

EXPECTED_FASTA_MD5 = "db508667b8691260997c7bdef610e98c"
EXPECTED_FASTA_SHA256 = "6d82c064edbcdbf9ed148b3d00181995b45c68e489d6c5fbe3e0403c034aafc4"


def digest(path: Path):
    md5 = hashlib.md5()
    sha = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            md5.update(chunk)
            sha.update(chunk)
    return md5.hexdigest(), sha.hexdigest()


def count_fasta(path: Path):
    n = 0
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith(">"):
                n += 1
    return n


def check_mzml_gz(path: Path):
    spectra = 0
    bda = 0
    ms_level = 0
    with gzip.open(path, "rb") as fh:
        for event, elem in ET.iterparse(fh, events=("end",)):
            tag = elem.tag.split("}")[-1]
            if tag == "spectrum":
                spectra += 1
                elem.clear()
            elif tag == "binaryDataArray":
                bda += 1
                elem.clear()
            elif tag == "cvParam" and elem.attrib.get("accession") == "MS:1000511":
                ms_level += 1
                elem.clear()
    return {"spectra": spectra, "binaryDataArray": bda, "ms_level_cv": ms_level}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--fasta", required=True, type=Path)
    p.add_argument("--mzml", required=True, type=Path)
    p.add_argument("--json-out", required=True, type=Path)
    a = p.parse_args()
    rep = {"status": "partial", "validation": "fail", "error_code": "missing_required_input"}
    if not a.fasta.exists() or not a.mzml.exists():
        rep["fasta_exists"] = a.fasta.exists()
        rep["mzml_exists"] = a.mzml.exists()
    else:
        md5, sha = digest(a.fasta)
        m = check_mzml_gz(a.mzml)
        rep.update({
            "fasta_exists": True,
            "mzml_exists": True,
            "fasta_md5": md5,
            "fasta_sha256": sha,
            "fasta_records": count_fasta(a.fasta),
            "mzml_gz": m,
            "fasta_md5_expected_match": md5 == EXPECTED_FASTA_MD5,
            "fasta_sha256_expected_match": sha == EXPECTED_FASTA_SHA256,
        })
        if rep["fasta_md5_expected_match"] and m["spectra"] > 0 and m["binaryDataArray"] == 2 * m["spectra"]:
            rep.update({"status": "ok", "validation": "pass", "error_code": None})
        else:
            rep["error_code"] = "verification_failed"
    a.json_out.parent.mkdir(parents=True, exist_ok=True)
    a.json_out.write_text(json.dumps(rep, indent=2) + "\n")
    print(json.dumps(rep, indent=2))
    return 0 if rep["validation"] == "pass" else 2

if __name__ == "__main__":
    raise SystemExit(main())
