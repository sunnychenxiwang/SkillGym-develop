"""Expectation tests for duplicate compound identification task.

These tests verify that the task execution produces correct outputs by:
1. Loading input SDF files and extracting PUBCHEM_COMPOUND_CID tags
2. Standardizing molecules using Datamol and computing canonical SMILES
3. Computing Morgan fingerprints (radius=2, nBits=2048) for Tanimoto similarity
4. Asserting JSON output matches these computed values exactly
5. Enforcing exact expected values from task requirements
"""

import json
import os
from pathlib import Path

import datamol as dm
import pytest
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import AllChem


OUTPUT_FILE = "/root/duplicate_identity_report.json"
INPUT_DIR = "/root"

INPUT_FILES = {
    "SDF": os.path.join(INPUT_DIR, "SDF"),
    "SDF_2": os.path.join(INPUT_DIR, "SDF_2"),
    "benzene.sdf": os.path.join(INPUT_DIR, "benzene.sdf"),
}

# Expected exact values from task requirements
EXPECTED_DUPLICATE_FILENAMES = {"SDF", "benzene.sdf"}
EXPECTED_UNIQUE_FILENAME = "SDF_2"
EXPECTED_DUPLICATE_CID = 241
EXPECTED_UNIQUE_CID = 2244
EXPECTED_TANIMOTO = 0.1


def load_sdf_molecule_with_validation(filepath: str) -> Chem.Mol:
    """Load molecule from SDF file with explicit validation.

    Validates that:
    - The file contains exactly one molecule
    - The molecule is not None (successfully parsed)
    - The PUBCHEM_COMPOUND_CID property exists
    """
    supplier = Chem.SDMolSupplier(filepath, sanitize=True, removeHs=False)
    molecules = list(supplier)

    assert len(molecules) == 1, (
        f"SDF file {filepath} should contain exactly one molecule, "
        f"but found {len(molecules)}"
    )

    mol = molecules[0]
    assert mol is not None, (
        f"Failed to parse molecule from {filepath} - molecule is None"
    )

    assert mol.HasProp("PUBCHEM_COMPOUND_CID"), (
        f"Molecule from {filepath} is missing required PUBCHEM_COMPOUND_CID property"
    )

    return mol


def get_pubchem_cid(mol: Chem.Mol) -> int:
    """Extract PUBCHEM_COMPOUND_CID from molecule properties."""
    cid = mol.GetProp("PUBCHEM_COMPOUND_CID")
    return int(cid)


def standardize_and_get_canonical_smiles_datamol(mol: Chem.Mol) -> str:
    """Standardize molecule using Datamol and return canonical SMILES.

    Uses datamol.standardize_mol() for standardization and
    datamol.to_smiles(canonical=True) for canonical SMILES generation,
    as required by the task specification.
    """
    standardized_mol = dm.standardize_mol(mol)
    canonical_smiles = dm.to_smiles(standardized_mol, canonical=True)
    return canonical_smiles


def compute_morgan_fingerprint(mol: Chem.Mol, radius: int = 2, n_bits: int = 2048):
    """Compute Morgan fingerprint with specified parameters.

    Uses Datamol-standardized molecule for consistency.
    """
    standardized_mol = dm.standardize_mol(mol)
    return AllChem.GetMorganFingerprintAsBitVect(standardized_mol, radius, nBits=n_bits)


def compute_tanimoto(fp1, fp2) -> float:
    """Compute Tanimoto similarity between two fingerprints."""
    return DataStructs.TanimotoSimilarity(fp1, fp2)


@pytest.fixture(scope="module")
def validated_input_files():
    """Validate all input SDF files before loading.

    Ensures each file:
    - Contains exactly one molecule
    - Has a valid molecule (not None)
    - Has the PUBCHEM_COMPOUND_CID property
    """
    for name, filepath in INPUT_FILES.items():
        assert os.path.exists(filepath), (
            f"Input file {name} not found at {filepath}"
        )
        supplier = Chem.SDMolSupplier(filepath, sanitize=True, removeHs=False)
        molecules = list(supplier)

        assert len(molecules) == 1, (
            f"Input file {name} ({filepath}) should contain exactly one molecule, "
            f"found {len(molecules)}"
        )
        assert molecules[0] is not None, (
            f"Input file {name} ({filepath}) contains an unparseable molecule"
        )
        assert molecules[0].HasProp("PUBCHEM_COMPOUND_CID"), (
            f"Input file {name} ({filepath}) is missing PUBCHEM_COMPOUND_CID property"
        )
    return True


@pytest.fixture(scope="module")
def input_molecules(validated_input_files):
    """Load all input molecules and extract their properties using Datamol standardization."""
    data = {}
    for name, filepath in INPUT_FILES.items():
        mol = load_sdf_molecule_with_validation(filepath)
        cid = get_pubchem_cid(mol)
        canonical_smiles = standardize_and_get_canonical_smiles_datamol(mol)
        fp = compute_morgan_fingerprint(mol, radius=2, n_bits=2048)
        data[name] = {
            "mol": mol,
            "pubchem_cid": cid,
            "canonical_smiles": canonical_smiles,
            "fingerprint": fp,
        }
    return data


@pytest.fixture(scope="module")
def output_data():
    """Load the JSON output file."""
    with open(OUTPUT_FILE) as f:
        return json.load(f)


@pytest.fixture(scope="module")
def expected_duplicates(input_molecules):
    """Determine expected duplicate pair based on matching CID and canonical SMILES."""
    files = list(INPUT_FILES.keys())
    duplicates = []
    for i, f1 in enumerate(files):
        for f2 in files[i + 1:]:
            if (input_molecules[f1]["pubchem_cid"] == input_molecules[f2]["pubchem_cid"] and
                input_molecules[f1]["canonical_smiles"] == input_molecules[f2]["canonical_smiles"]):
                duplicates.append((f1, f2))
    assert len(duplicates) == 1, f"Expected exactly one duplicate pair, found {len(duplicates)}"
    return duplicates[0]


@pytest.fixture(scope="module")
def expected_unique(input_molecules, expected_duplicates):
    """Determine expected unique file (the one not in the duplicate pair)."""
    all_files = set(INPUT_FILES.keys())
    duplicate_files = set(expected_duplicates)
    unique_files = all_files - duplicate_files
    assert len(unique_files) == 1, f"Expected exactly one unique file, found {len(unique_files)}"
    return unique_files.pop()


class TestInputFileValidation:
    """Tests for validating input SDF files meet requirements."""

    def test_all_input_files_exist(self):
        """Verify all expected input files exist."""
        for name, filepath in INPUT_FILES.items():
            assert os.path.exists(filepath), (
                f"Required input file '{name}' not found at {filepath}"
            )

    def test_each_sdf_contains_exactly_one_molecule(self):
        """Verify each SDF file contains exactly one molecule."""
        for name, filepath in INPUT_FILES.items():
            supplier = Chem.SDMolSupplier(filepath, sanitize=True, removeHs=False)
            molecules = [m for m in supplier]
            assert len(molecules) == 1, (
                f"Input file '{name}' should contain exactly one molecule, "
                f"but found {len(molecules)}"
            )

    def test_each_molecule_is_parseable(self):
        """Verify each SDF file contains a valid, parseable molecule."""
        for name, filepath in INPUT_FILES.items():
            supplier = Chem.SDMolSupplier(filepath, sanitize=True, removeHs=False)
            mol = next(iter(supplier))
            assert mol is not None, (
                f"Input file '{name}' contains a molecule that failed to parse"
            )

    def test_each_molecule_has_pubchem_cid_property(self):
        """Verify each molecule has the PUBCHEM_COMPOUND_CID property."""
        for name, filepath in INPUT_FILES.items():
            supplier = Chem.SDMolSupplier(filepath, sanitize=True, removeHs=False)
            mol = next(iter(supplier))
            assert mol.HasProp("PUBCHEM_COMPOUND_CID"), (
                f"Input file '{name}' is missing required PUBCHEM_COMPOUND_CID property"
            )


class TestOutputFileExists:
    """Tests for verifying output file existence and basic structure."""

    def test_output_file_exists(self):
        """Verify output file was created at the expected path."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

    def test_output_file_is_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.getsize(OUTPUT_FILE) > 0, "Output file is empty"


class TestOutputIsValidJson:
    """Tests for verifying JSON validity and structure."""

    def test_output_is_valid_json(self, output_data):
        """Verify output is valid JSON format."""
        assert output_data is not None, "JSON data is None"
        assert isinstance(output_data, dict), "JSON root should be a dictionary"

    def test_required_top_level_keys_exist(self, output_data):
        """Verify all required top-level keys are present."""
        required_keys = {"duplicate_pair", "unique_file", "tanimoto_unique_vs_duplicate"}
        actual_keys = set(output_data.keys())
        missing_keys = required_keys - actual_keys
        assert not missing_keys, f"Missing required top-level keys: {missing_keys}"

    def test_no_extra_top_level_keys(self, output_data):
        """Verify only expected top-level keys are present."""
        expected_keys = {"duplicate_pair", "unique_file", "tanimoto_unique_vs_duplicate"}
        extra_keys = set(output_data.keys()) - expected_keys
        assert not extra_keys, f"Unexpected top-level keys: {extra_keys}"


class TestDuplicatePairStructure:
    """Tests for duplicate_pair section structure and content."""

    def test_duplicate_pair_is_dict(self, output_data):
        """Verify duplicate_pair is a dictionary."""
        assert isinstance(output_data.get("duplicate_pair"), dict), (
            "duplicate_pair should be a dictionary"
        )

    def test_duplicate_pair_required_keys(self, output_data):
        """Verify duplicate_pair has all required keys."""
        required_keys = {"file_a", "file_b", "pubchem_cid", "canonical_smiles"}
        actual_keys = set(output_data["duplicate_pair"].keys())
        missing_keys = required_keys - actual_keys
        assert not missing_keys, f"duplicate_pair missing required keys: {missing_keys}"

    def test_no_extra_duplicate_pair_keys(self, output_data):
        """Verify only expected keys in duplicate_pair."""
        expected_keys = {"file_a", "file_b", "pubchem_cid", "canonical_smiles"}
        extra_keys = set(output_data["duplicate_pair"].keys()) - expected_keys
        assert not extra_keys, f"Unexpected duplicate_pair keys: {extra_keys}"

    def test_duplicate_pair_file_a_is_string(self, output_data):
        """Verify file_a is a string."""
        assert isinstance(output_data["duplicate_pair"]["file_a"], str), (
            "duplicate_pair.file_a should be a string"
        )

    def test_duplicate_pair_file_b_is_string(self, output_data):
        """Verify file_b is a string."""
        assert isinstance(output_data["duplicate_pair"]["file_b"], str), (
            "duplicate_pair.file_b should be a string"
        )

    def test_duplicate_pair_pubchem_cid_is_integer(self, output_data):
        """Verify pubchem_cid is an integer (not float or string)."""
        cid = output_data["duplicate_pair"]["pubchem_cid"]
        assert isinstance(cid, int), (
            f"duplicate_pair.pubchem_cid should be an integer, got {type(cid).__name__}"
        )
        assert not isinstance(cid, bool), "duplicate_pair.pubchem_cid should not be a boolean"

    def test_duplicate_pair_canonical_smiles_is_string(self, output_data):
        """Verify canonical_smiles is a non-empty string."""
        smiles = output_data["duplicate_pair"]["canonical_smiles"]
        assert isinstance(smiles, str), "duplicate_pair.canonical_smiles should be a string"
        assert len(smiles) > 0, "duplicate_pair.canonical_smiles should not be empty"


class TestUniqueFileStructure:
    """Tests for unique_file section structure and content."""

    def test_unique_file_is_dict(self, output_data):
        """Verify unique_file is a dictionary."""
        assert isinstance(output_data.get("unique_file"), dict), (
            "unique_file should be a dictionary"
        )

    def test_unique_file_required_keys(self, output_data):
        """Verify unique_file has all required keys."""
        required_keys = {"file", "pubchem_cid", "canonical_smiles"}
        actual_keys = set(output_data["unique_file"].keys())
        missing_keys = required_keys - actual_keys
        assert not missing_keys, f"unique_file missing required keys: {missing_keys}"

    def test_no_extra_unique_file_keys(self, output_data):
        """Verify only expected keys in unique_file."""
        expected_keys = {"file", "pubchem_cid", "canonical_smiles"}
        extra_keys = set(output_data["unique_file"].keys()) - expected_keys
        assert not extra_keys, f"Unexpected unique_file keys: {extra_keys}"

    def test_unique_file_file_is_string(self, output_data):
        """Verify file field is a string."""
        assert isinstance(output_data["unique_file"]["file"], str), (
            "unique_file.file should be a string"
        )

    def test_unique_file_pubchem_cid_is_integer(self, output_data):
        """Verify pubchem_cid is an integer (not float or string)."""
        cid = output_data["unique_file"]["pubchem_cid"]
        assert isinstance(cid, int), (
            f"unique_file.pubchem_cid should be an integer, got {type(cid).__name__}"
        )
        assert not isinstance(cid, bool), "unique_file.pubchem_cid should not be a boolean"

    def test_unique_file_canonical_smiles_is_string(self, output_data):
        """Verify canonical_smiles is a non-empty string."""
        smiles = output_data["unique_file"]["canonical_smiles"]
        assert isinstance(smiles, str), "unique_file.canonical_smiles should be a string"
        assert len(smiles) > 0, "unique_file.canonical_smiles should not be empty"


class TestExactExpectedFilenames:
    """Tests enforcing the exact required filenames from the task specification."""

    def test_duplicate_pair_contains_exact_expected_files(self, output_data):
        """Verify duplicate pair contains exactly 'SDF' and 'benzene.sdf' (in any order)."""
        output_files = {
            output_data["duplicate_pair"]["file_a"],
            output_data["duplicate_pair"]["file_b"]
        }
        assert output_files == EXPECTED_DUPLICATE_FILENAMES, (
            f"Duplicate pair must contain exactly {EXPECTED_DUPLICATE_FILENAMES}, "
            f"got {output_files}"
        )

    def test_unique_file_is_exactly_sdf_2(self, output_data):
        """Verify unique file is exactly 'SDF_2'."""
        assert output_data["unique_file"]["file"] == EXPECTED_UNIQUE_FILENAME, (
            f"unique_file.file must be '{EXPECTED_UNIQUE_FILENAME}', "
            f"got '{output_data['unique_file']['file']}'"
        )

    def test_filenames_are_base_names(self, output_data):
        """Verify all file references are base filenames (no paths)."""
        file_a = output_data["duplicate_pair"]["file_a"]
        file_b = output_data["duplicate_pair"]["file_b"]
        unique_file = output_data["unique_file"]["file"]

        for fname in [file_a, file_b, unique_file]:
            assert "/" not in fname, f"Filename should be base name, not path: {fname}"
            assert "\\" not in fname, f"Filename should be base name, not path: {fname}"

    def test_all_three_files_represented(self, output_data):
        """Verify all three input files are accounted for in the output."""
        file_a = output_data["duplicate_pair"]["file_a"]
        file_b = output_data["duplicate_pair"]["file_b"]
        unique_file = output_data["unique_file"]["file"]

        all_files = {file_a, file_b, unique_file}
        expected_files = set(INPUT_FILES.keys())

        assert all_files == expected_files, (
            f"Expected files {expected_files}, but got {all_files}"
        )

    def test_duplicate_pair_has_different_files(self, output_data):
        """Verify file_a and file_b are different files."""
        file_a = output_data["duplicate_pair"]["file_a"]
        file_b = output_data["duplicate_pair"]["file_b"]
        assert file_a != file_b, (
            f"Duplicate pair should reference two different files, got '{file_a}' twice"
        )


class TestExactExpectedCidValues:
    """Tests enforcing the exact required PubChem CID values from the task specification."""

    def test_duplicate_pair_cid_is_exactly_241(self, output_data):
        """Verify duplicate pair CID is exactly 241 (benzene)."""
        assert output_data["duplicate_pair"]["pubchem_cid"] == EXPECTED_DUPLICATE_CID, (
            f"duplicate_pair.pubchem_cid must be {EXPECTED_DUPLICATE_CID}, "
            f"got {output_data['duplicate_pair']['pubchem_cid']}"
        )

    def test_unique_file_cid_is_exactly_2244(self, output_data):
        """Verify unique file CID is exactly 2244 (aspirin)."""
        assert output_data["unique_file"]["pubchem_cid"] == EXPECTED_UNIQUE_CID, (
            f"unique_file.pubchem_cid must be {EXPECTED_UNIQUE_CID}, "
            f"got {output_data['unique_file']['pubchem_cid']}"
        )

    def test_duplicate_cid_differs_from_unique_cid(self, output_data):
        """Verify duplicate pair and unique file have different CIDs."""
        dup_cid = output_data["duplicate_pair"]["pubchem_cid"]
        unique_cid = output_data["unique_file"]["pubchem_cid"]
        assert dup_cid != unique_cid, (
            f"Duplicate ({dup_cid}) and unique ({unique_cid}) should have different CIDs"
        )


class TestExactExpectedTanimotoValue:
    """Tests enforcing the exact required Tanimoto value from the task specification."""

    def test_tanimoto_is_exactly_zero(self, output_data):
        """Verify tanimoto_unique_vs_duplicate is exactly 0.0."""
        tanimoto = output_data["tanimoto_unique_vs_duplicate"]
        assert tanimoto == EXPECTED_TANIMOTO, (
            f"tanimoto_unique_vs_duplicate must be {EXPECTED_TANIMOTO}, got {tanimoto}"
        )

    def test_tanimoto_is_numeric(self, output_data):
        """Verify tanimoto_unique_vs_duplicate is a float."""
        tanimoto = output_data.get("tanimoto_unique_vs_duplicate")
        assert isinstance(tanimoto, (int, float)), (
            f"tanimoto_unique_vs_duplicate should be numeric, got {type(tanimoto).__name__}"
        )

    def test_tanimoto_in_valid_range(self, output_data):
        """Verify tanimoto similarity is between 0 and 1 (inclusive)."""
        tanimoto = output_data["tanimoto_unique_vs_duplicate"]
        assert 0.0 <= tanimoto <= 1.0, (
            f"Tanimoto similarity should be in [0, 1], got {tanimoto}"
        )


class TestDuplicateIdentificationByCidAndSmiles:
    """Tests verifying duplicates are identified by matching CID AND canonical SMILES."""

    def test_duplicate_pair_files_match_expected(self, output_data, expected_duplicates):
        """Verify duplicate pair consists of the files with matching CID and SMILES."""
        output_files = {
            output_data["duplicate_pair"]["file_a"],
            output_data["duplicate_pair"]["file_b"]
        }
        expected_files = set(expected_duplicates)
        assert output_files == expected_files, (
            f"Duplicate pair should be {expected_files}, got {output_files}. "
            "Duplicates must have both matching PUBCHEM_COMPOUND_CID and identical "
            "post-standardization canonical SMILES."
        )

    def test_unique_file_matches_expected(self, output_data, expected_unique):
        """Verify unique file is the one not matching others by CID and SMILES."""
        assert output_data["unique_file"]["file"] == expected_unique, (
            f"Unique file should be '{expected_unique}', "
            f"got '{output_data['unique_file']['file']}'"
        )

    def test_duplicate_pair_cid_extracted_from_sdf(self, output_data, input_molecules, expected_duplicates):
        """Verify duplicate pair CID matches the PUBCHEM_COMPOUND_CID tag from input SDFs."""
        expected_cid = input_molecules[expected_duplicates[0]]["pubchem_cid"]
        other_cid = input_molecules[expected_duplicates[1]]["pubchem_cid"]
        assert expected_cid == other_cid, (
            f"Duplicate files should have same CID, got {expected_cid} vs {other_cid}"
        )
        assert output_data["duplicate_pair"]["pubchem_cid"] == expected_cid, (
            f"duplicate_pair.pubchem_cid should be {expected_cid} "
            f"(from SDF PUBCHEM_COMPOUND_CID tag), got {output_data['duplicate_pair']['pubchem_cid']}"
        )

    def test_unique_file_cid_extracted_from_sdf(self, output_data, input_molecules, expected_unique):
        """Verify unique file CID matches the PUBCHEM_COMPOUND_CID tag from input SDF."""
        expected_cid = input_molecules[expected_unique]["pubchem_cid"]
        assert output_data["unique_file"]["pubchem_cid"] == expected_cid, (
            f"unique_file.pubchem_cid should be {expected_cid} "
            f"(from SDF PUBCHEM_COMPOUND_CID tag), got {output_data['unique_file']['pubchem_cid']}"
        )


class TestCanonicalSmilesFromDatamolStandardization:
    """Tests verifying canonical SMILES are computed using Datamol standardization."""

    def test_duplicate_pair_canonical_smiles_matches_datamol(self, output_data, input_molecules, expected_duplicates):
        """Verify duplicate_pair.canonical_smiles matches Datamol-standardized SMILES."""
        smiles_a = input_molecules[expected_duplicates[0]]["canonical_smiles"]
        smiles_b = input_molecules[expected_duplicates[1]]["canonical_smiles"]
        assert smiles_a == smiles_b, (
            f"Duplicate files should have identical Datamol-standardized canonical SMILES: "
            f"'{smiles_a}' vs '{smiles_b}'"
        )
        output_smiles = output_data["duplicate_pair"]["canonical_smiles"]
        assert output_smiles == smiles_a, (
            f"duplicate_pair.canonical_smiles should be '{smiles_a}' "
            f"(Datamol-standardized canonical SMILES), got '{output_smiles}'"
        )

    def test_unique_file_canonical_smiles_matches_datamol(self, output_data, input_molecules, expected_unique):
        """Verify unique_file.canonical_smiles matches Datamol-standardized SMILES."""
        expected_smiles = input_molecules[expected_unique]["canonical_smiles"]
        output_smiles = output_data["unique_file"]["canonical_smiles"]
        assert output_smiles == expected_smiles, (
            f"unique_file.canonical_smiles should be '{expected_smiles}' "
            f"(Datamol-standardized canonical SMILES), got '{output_smiles}'"
        )

    def test_duplicate_and_unique_smiles_different(self, output_data, input_molecules, expected_duplicates, expected_unique):
        """Verify duplicate and unique compounds have different canonical SMILES."""
        dup_smiles = input_molecules[expected_duplicates[0]]["canonical_smiles"]
        unique_smiles = input_molecules[expected_unique]["canonical_smiles"]
        assert dup_smiles != unique_smiles, (
            f"Duplicate pair SMILES '{dup_smiles}' should differ from unique SMILES '{unique_smiles}'"
        )
        assert output_data["duplicate_pair"]["canonical_smiles"] != output_data["unique_file"]["canonical_smiles"], (
            "Output duplicate and unique SMILES should be different"
        )


class TestTanimotoSimilarityComputation:
    """Tests verifying Tanimoto similarity computed with Morgan(radius=2, nBits=2048)."""

    def test_tanimoto_matches_morgan_fingerprint_computation(self, output_data, input_molecules, expected_duplicates, expected_unique):
        """Verify Tanimoto value matches Morgan(radius=2, nBits=2048) fingerprint computation."""
        dup_fp = input_molecules[expected_duplicates[0]]["fingerprint"]
        unique_fp = input_molecules[expected_unique]["fingerprint"]
        expected_tanimoto = compute_tanimoto(dup_fp, unique_fp)
        output_tanimoto = output_data["tanimoto_unique_vs_duplicate"]
        assert abs(output_tanimoto - expected_tanimoto) < 1e-6, (
            f"tanimoto_unique_vs_duplicate should be {expected_tanimoto:.10f} "
            f"(computed with Morgan radius=2, nBits=2048), got {output_tanimoto:.10f}"
        )

    def test_tanimoto_zero_for_benzene_vs_aspirin(self, output_data, input_molecules, expected_duplicates, expected_unique):
        """Verify Tanimoto matches expected value for benzene vs aspirin with Morgan(2, 2048)."""
        dup_fp = input_molecules[expected_duplicates[0]]["fingerprint"]
        unique_fp = input_molecules[expected_unique]["fingerprint"]
        expected_tanimoto = compute_tanimoto(dup_fp, unique_fp)
        output_tanimoto = output_data["tanimoto_unique_vs_duplicate"]

        assert abs(expected_tanimoto - EXPECTED_TANIMOTO) < 1e-6, (
            f"Expected Tanimoto between benzene and aspirin to be {EXPECTED_TANIMOTO} "
            f"but computed {expected_tanimoto}"
        )
        assert abs(output_tanimoto - EXPECTED_TANIMOTO) < 1e-6, (
            f"Expected Tanimoto of {EXPECTED_TANIMOTO}, got {output_tanimoto}"
        )

    def test_tanimoto_less_than_one_for_different_compounds(self, output_data):
        """Verify Tanimoto is < 1.0 since unique and duplicate are different compounds."""
        tanimoto = output_data["tanimoto_unique_vs_duplicate"]
        assert tanimoto < 1.0, (
            f"Tanimoto between different compounds (benzene vs aspirin) should be < 1.0, got {tanimoto}"
        )


class TestJsonStructureComplete:
    """Final validation that JSON structure is complete and correct."""

    def test_json_is_dict_not_list(self, output_data):
        """Verify JSON root is a dictionary, not a list."""
        assert isinstance(output_data, dict), (
            f"JSON root should be dict, got {type(output_data).__name__}"
        )

    def test_complete_structure(self, output_data):
        """Verify complete JSON structure with all required nested fields."""
        assert "duplicate_pair" in output_data
        assert "unique_file" in output_data
        assert "tanimoto_unique_vs_duplicate" in output_data

        dp = output_data["duplicate_pair"]
        assert all(k in dp for k in ["file_a", "file_b", "pubchem_cid", "canonical_smiles"])

        uf = output_data["unique_file"]
        assert all(k in uf for k in ["file", "pubchem_cid", "canonical_smiles"])


class TestDuplicatePairOrderIndependent:
    """Tests ensuring duplicate pair detection is correct regardless of file_a/file_b ordering."""

    def test_duplicate_files_are_correct_set(self, output_data, expected_duplicates):
        """Verify duplicate pair contains correct files regardless of ordering."""
        output_set = {
            output_data["duplicate_pair"]["file_a"],
            output_data["duplicate_pair"]["file_b"]
        }
        expected_set = set(expected_duplicates)
        assert output_set == expected_set, (
            f"Duplicate pair files should be {expected_set} (in any order), got {output_set}"
        )

    def test_single_shared_cid_for_duplicate_pair(self, output_data, input_molecules):
        """Verify both duplicate files share the same CID as reported."""
        file_a = output_data["duplicate_pair"]["file_a"]
        file_b = output_data["duplicate_pair"]["file_b"]
        reported_cid = output_data["duplicate_pair"]["pubchem_cid"]

        cid_a = input_molecules[file_a]["pubchem_cid"]
        cid_b = input_molecules[file_b]["pubchem_cid"]

        assert cid_a == cid_b == reported_cid, (
            f"Both duplicate files should have CID {reported_cid}, "
            f"but file_a ({file_a}) has {cid_a} and file_b ({file_b}) has {cid_b}"
        )

    def test_single_shared_smiles_for_duplicate_pair(self, output_data, input_molecules):
        """Verify both duplicate files share the same canonical SMILES as reported."""
        file_a = output_data["duplicate_pair"]["file_a"]
        file_b = output_data["duplicate_pair"]["file_b"]
        reported_smiles = output_data["duplicate_pair"]["canonical_smiles"]

        smiles_a = input_molecules[file_a]["canonical_smiles"]
        smiles_b = input_molecules[file_b]["canonical_smiles"]

        assert smiles_a == smiles_b == reported_smiles, (
            f"Both duplicate files should have SMILES '{reported_smiles}', "
            f"but file_a ({file_a}) has '{smiles_a}' and file_b ({file_b}) has '{smiles_b}'"
        )
