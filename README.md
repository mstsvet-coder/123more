# PXD045741 Sage shard pilot scaffold

This repository is a lightweight GitHub Actions scaffold for a one-file Sage parser/search-intake pilot for the RAW PXD045741 / OB3b-MmoD proteomics project.

It does not contain RAW files, full mzML files, FASTA databases, peptide tables, PSM tables, FDR tables, or biological interpretation outputs.

## Current intended route

1. Provide a small `mzML.gz` search-projection shard as repository data or artifact.
2. Download or provide the checksum-locked OB3b target FASTA plus cRAP contaminants.
3. Install `sage-proteomics` in the runner.
4. Generate `sage_config.json`.
5. Run one-file Sage pilot only.
6. Validate `results.sage.tsv` schema and q-value columns before any claim is made.

## Required local data not committed here

Place these files before running the workflow, or adapt the workflow to fetch them from a private artifact store:

```text
data/fasta/B2117_TARGET_PLUS_CRAP_GPM_CONTAMINANTS_V024.fasta
data/projection/MSB10955Pool_30MinDIA041023GPF_01.search_projection_shard_v26_1000spectra.mzML.gz
```

Expected FASTA checks:

```yaml
combined_fasta_records: 4681
combined_fasta_md5: db508667b8691260997c7bdef610e98c
combined_fasta_sha256: 6d82c064edbcdbf9ed148b3d00181995b45c68e489d6c5fbe3e0403c034aafc4
```

## Claim boundary

Generated mzML is raw spectral layer only. It is not peptide, PSM, FDR, or protein evidence and must not be interpreted as a biological or protein-level claim.
