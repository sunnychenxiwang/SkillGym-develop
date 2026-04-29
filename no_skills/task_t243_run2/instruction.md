Load **all three** provided SDF files (`/root/SDF`, `/root/SDF_2`, `/root/benzene.sdf`) as molecules, standardize them (sanitize + standardize), and then determine **which two files represent the same compound** by verifying **both** of the following agree after standardization:

1) identical **canonical SMILES** (RDKit/Datamol canonicalization), and  
2) identical **PubChem CID** extracted from the SDF property field `PUBCHEM_COMPOUND_CID`.

Then, compute the **Morgan fingerprint (radius=2, 2048 bits)** Tanimoto similarity between the *unique* compound and the *duplicate* compound (use the standardized molecules), and save a single JSON report to:

`/root/duplicate_identity_report.json`

with exactly this schema:

```json
{
  "duplicate_pair": {
    "file_a": "SDF",
    "file_b": "benzene.sdf",
    "pubchem_cid": 241,
    "canonical_smiles": "..."
  },
  "unique_file": {
    "file": "SDF_2",
    "pubchem_cid": 2244,
    "canonical_smiles": "..."
  },
  "tanimoto_unique_vs_duplicate": 0.0
}
```

Requirements:
- `file_a`, `file_b`, and `unique_file.file` must be the **base filenames** exactly as shown above.
- `pubchem_cid` values must be **integers** taken from the SDF tags (not inferred).
- `canonical_smiles` must be the **post-standardization** canonical SMILES.
- `tanimoto_unique_vs_duplicate` must be a **float** computed from Morgan fingerprints as specified.
- The JSON must be deterministic (stable ordering/formatting is fine) and writing the file is mandatory.