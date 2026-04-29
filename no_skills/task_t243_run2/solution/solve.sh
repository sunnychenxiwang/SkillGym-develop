#!/usr/bin/env bash
set -euo pipefail

# Create expectation_tests.py
cat > "/root/expectation_tests.py" <<'PYEOF'
import json
import os

def test_output_json_exists_and_has_keys():
    out_path = "/root/duplicate_identity_report.json"
    assert os.path.exists(out_path)
    with open(out_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "duplicate_pair" in data
    assert "unique_file" in data
    assert "tanimoto_unique_vs_duplicate" in data

    dp = data["duplicate_pair"]
    uf = data["unique_file"]

    assert set(dp.keys()) == {"file_a", "file_b", "pubchem_cid", "canonical_smiles"}
    assert set(uf.keys()) == {"file", "pubchem_cid", "canonical_smiles"}

    assert isinstance(dp["pubchem_cid"], int)
    assert isinstance(uf["pubchem_cid"], int)
    assert isinstance(data["tanimoto_unique_vs_duplicate"], float)
PYEOF

# Create process_sdfs.py (main script that generates required JSON)
cat > "/root/process_sdfs.py" <<'PYEOF'
import json
import os
import datamol as dm
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem

INPUTS = [
    "/root/SDF",
    "/root/SDF_2",
    "/root/benzene.sdf",
]
OUT_PATH = "/root/duplicate_identity_report.json"

def load_first_mol(path: str) -> Chem.Mol:
    suppl = Chem.SDMolSupplier(path, sanitize=True, removeHs=False)
    for m in suppl:
        if m is not None:
            return m
    raise ValueError(f"No valid molecule found in {path}")

def get_cid(m: Chem.Mol) -> int:
    if not m.HasProp("PUBCHEM_COMPOUND_CID"):
        raise KeyError("Missing PUBCHEM_COMPOUND_CID property")
    return int(m.GetProp("PUBCHEM_COMPOUND_CID"))

def morgan_fp(m: Chem.Mol):
    return AllChem.GetMorganFingerprintAsBitVect(m, radius=2, nBits=2048)

def main():
    records = []
    for p in INPUTS:
        m0 = load_first_mol(p)
        # Standardize using datamol as required by the task
        m = dm.standardize_mol(m0)
        canonical_smiles = dm.to_smiles(m, canonical=True)
        rec = {
            "path": p,
            "file": os.path.basename(p),
            "cid": get_cid(m0),  # CID from original molecule properties
            "smiles": canonical_smiles,
            "mol": m,
        }
        records.append(rec)

    # Find duplicate pair: must match BOTH CID and canonical SMILES
    dup_pair = None
    unique = None

    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            if records[i]["cid"] == records[j]["cid"] and records[i]["smiles"] == records[j]["smiles"]:
                dup_pair = (records[i], records[j])
                break
        if dup_pair:
            break

    if not dup_pair:
        raise RuntimeError("No duplicate pair found by CID+canonical SMILES agreement")

    dup_files = {dup_pair[0]["file"], dup_pair[1]["file"]}
    remaining = [r for r in records if r["file"] not in dup_files]
    if len(remaining) != 1:
        raise RuntimeError("Could not uniquely identify the unique file")
    unique = remaining[0]

    # Compute similarity between unique and one of the duplicates
    fp_u = morgan_fp(unique["mol"])
    fp_d = morgan_fp(dup_pair[0]["mol"])
    tanimoto = float(DataStructs.TanimotoSimilarity(fp_u, fp_d))

    report = {
        "duplicate_pair": {
            "file_a": dup_pair[0]["file"],
            "file_b": dup_pair[1]["file"],
            "pubchem_cid": int(dup_pair[0]["cid"]),
            "canonical_smiles": dup_pair[0]["smiles"],
        },
        "unique_file": {
            "file": unique["file"],
            "pubchem_cid": int(unique["cid"]),
            "canonical_smiles": unique["smiles"],
        },
        "tanimoto_unique_vs_duplicate": tanimoto,
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, sort_keys=True, indent=2)
        f.write("\n")

if __name__ == "__main__":
    main()
PYEOF

# Run the main processor to generate the required JSON report
python3 "/root/process_sdfs.py"

# Ensure output exists
test -f "/root/duplicate_identity_report.json"
