"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for finding the contig with
the highest fraction of unmapped reads in ex1.bam.

Expected output JSON schema:
{
    "flag_unmapped_bit_from_doc": 4,
    "contig": "chr1",
    "mapped_reads": 0,
    "unmapped_reads": 0,
    "unmapped_fraction": 0.0
}
"""

import json
import os
import re
from pathlib import Path

import pysam
import pytest


# Expected output file path
OUTPUT_PATH = "/root/contig_max_unmapped_fraction.json"

# Input file paths
BAM_FILE = "/root/ex1.bam"
LEARNING_FILE = "/root/learning_bam_file"

# Required JSON keys per the task specification
REQUIRED_KEYS = {
    "flag_unmapped_bit_from_doc",
    "contig",
    "mapped_reads",
    "unmapped_reads",
    "unmapped_fraction",
}


def extract_unmap_bit_from_learning_file():
    """Extract the UNMAP flag bit value from learning_bam_file.

    Parses the learning_bam_file to find the documented UNMAP bit value.
    The file contains lines like:
        ##    0x4     4  UNMAP          segment unmapped
    or
        ## 0x4  4   UNMAP

    Returns:
        int: The decimal value of the UNMAP bit (expected to be 4)
    """
    with open(LEARNING_FILE, "r") as f:
        content = f.read()

    # Pattern to match UNMAP flag documentation lines
    # Matches formats like:
    #   ##    0x4     4  UNMAP          segment unmapped
    #   ## 0x4  4   UNMAP
    pattern = r"##\s+0x([0-9a-fA-F]+)\s+(\d+)\s+UNMAP\b"
    matches = re.findall(pattern, content)

    if not matches:
        raise ValueError("Could not find UNMAP flag documentation in learning_bam_file")

    # Extract the decimal value (second capture group)
    # All matches should have the same value; use the first one
    hex_value, decimal_value = matches[0]

    # Verify hex and decimal are consistent
    expected_decimal = int(hex_value, 16)
    actual_decimal = int(decimal_value)

    if expected_decimal != actual_decimal:
        raise ValueError(
            f"Inconsistent UNMAP values in learning_bam_file: "
            f"0x{hex_value} != {decimal_value}"
        )

    return actual_decimal


def compute_bam_stats_with_flag_bit(bam_path, unmapped_bit):
    """Compute per-contig statistics using the specified FLAG bit for unmapped classification.

    This is the reference implementation that explicitly enforces the rule that reads
    with no reference name (None/empty) must not be counted toward any contig's totals.

    Args:
        bam_path: Path to the BAM file
        unmapped_bit: The FLAG bit value to use for unmapped classification

    Returns:
        dict: Per-contig statistics with mapped, unmapped counts and fractions
    """
    stats = {}
    with pysam.AlignmentFile(bam_path, "rb") as bam:
        # Initialize stats for all references in the BAM header
        for ref in bam.references:
            stats[ref] = {"mapped": 0, "unmapped": 0}

        # Count reads using the specified FLAG bit
        # CRITICAL: Only count reads that have a valid (non-None, non-empty) reference_name
        for read in bam.fetch(until_eof=True):
            ref_name = read.reference_name
            # Explicitly skip reads with no reference name - they must not be counted
            if not ref_name:
                continue
            if ref_name not in stats:
                continue
            # Use the extracted FLAG bit to determine unmapped status
            is_unmapped = (read.flag & unmapped_bit) != 0
            if is_unmapped:
                stats[ref_name]["unmapped"] += 1
            else:
                stats[ref_name]["mapped"] += 1

    # Calculate fractions
    for ref in stats:
        total = stats[ref]["mapped"] + stats[ref]["unmapped"]
        if total > 0:
            stats[ref]["fraction"] = stats[ref]["unmapped"] / total
        else:
            stats[ref]["fraction"] = 0.0

    return stats


def count_reads_with_no_reference_name(bam_path):
    """Count reads in the BAM file that have no reference name (None or empty).

    These reads must not be counted toward any contig's mapped/unmapped totals.

    Args:
        bam_path: Path to the BAM file

    Returns:
        int: Number of reads with no reference name
    """
    count = 0
    with pysam.AlignmentFile(bam_path, "rb") as bam:
        for read in bam.fetch(until_eof=True):
            if not read.reference_name:
                count += 1
    return count


def get_expected_contig_with_tiebreaking(stats):
    """Get the contig with maximum unmapped fraction, using lexicographic tie-breaking.

    When multiple contigs have the same maximum fraction, returns the
    lexicographically smallest contig name.

    Args:
        stats: Dict of contig -> {mapped, unmapped, fraction}

    Returns:
        str: The contig name with maximum unmapped fraction
    """
    if not stats:
        return None

    max_fraction = max(s["fraction"] for s in stats.values())

    # Find all contigs with the maximum fraction (ties)
    tied_contigs = [
        contig for contig, s in stats.items()
        if s["fraction"] == max_fraction
    ]

    # Return lexicographically smallest among ties
    return min(tied_contigs)


class TestOutputFileExists:
    """Tests for verifying output file creation."""

    def test_output_file_exists(self):
        """Verify output file was created at the specified path."""
        assert os.path.exists(OUTPUT_PATH), (
            f"Output file not found at {OUTPUT_PATH}. "
            "The task requires writing the result to this exact path."
        )

    def test_output_file_is_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.exists(OUTPUT_PATH), f"Output file not found at {OUTPUT_PATH}"
        file_size = os.path.getsize(OUTPUT_PATH)
        assert file_size > 0, "Output file exists but is empty"

    def test_output_directory_exists(self):
        """Verify output directory exists."""
        output_dir = os.path.dirname(OUTPUT_PATH)
        assert os.path.isdir(output_dir), f"Output directory {output_dir} does not exist"


class TestOutputFormat:
    """Tests for verifying output format validity."""

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        assert os.path.exists(OUTPUT_PATH), f"Output file not found at {OUTPUT_PATH}"
        with open(OUTPUT_PATH) as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                pytest.fail(f"Output file is not valid JSON: {e}")
        assert data is not None, "JSON parsed to None"

    def test_output_is_json_object(self):
        """Verify output is a JSON object (dict), not an array or primitive."""
        assert os.path.exists(OUTPUT_PATH), f"Output file not found at {OUTPUT_PATH}"
        with open(OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data, dict), (
            f"Output should be a JSON object (dict), got {type(data).__name__}"
        )


class TestRequiredFields:
    """Tests for verifying all required fields are present."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_PATH) as f:
            return json.load(f)

    def test_has_flag_unmapped_bit_from_doc(self, output_data):
        """Verify 'flag_unmapped_bit_from_doc' field is present."""
        assert "flag_unmapped_bit_from_doc" in output_data, (
            "Missing required field: 'flag_unmapped_bit_from_doc'"
        )

    def test_has_contig_field(self, output_data):
        """Verify 'contig' field is present."""
        assert "contig" in output_data, "Missing required field: 'contig'"

    def test_has_mapped_reads_field(self, output_data):
        """Verify 'mapped_reads' field is present."""
        assert "mapped_reads" in output_data, "Missing required field: 'mapped_reads'"

    def test_has_unmapped_reads_field(self, output_data):
        """Verify 'unmapped_reads' field is present."""
        assert "unmapped_reads" in output_data, "Missing required field: 'unmapped_reads'"

    def test_has_unmapped_fraction_field(self, output_data):
        """Verify 'unmapped_fraction' field is present."""
        assert "unmapped_fraction" in output_data, "Missing required field: 'unmapped_fraction'"

    def test_has_exactly_five_fields(self, output_data):
        """Verify output has exactly the 5 required fields (no extra fields)."""
        actual_fields = set(output_data.keys())
        assert actual_fields == REQUIRED_KEYS, (
            f"Expected fields {REQUIRED_KEYS}, got {actual_fields}. "
            f"Extra: {actual_fields - REQUIRED_KEYS}, Missing: {REQUIRED_KEYS - actual_fields}"
        )


class TestFieldTypes:
    """Tests for verifying field data types."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_PATH) as f:
            return json.load(f)

    def test_flag_unmapped_bit_is_integer(self, output_data):
        """Verify 'flag_unmapped_bit_from_doc' is an integer."""
        value = output_data.get("flag_unmapped_bit_from_doc")
        assert isinstance(value, int), (
            f"'flag_unmapped_bit_from_doc' should be an integer, got {type(value).__name__}"
        )

    def test_contig_is_string(self, output_data):
        """Verify 'contig' is a string."""
        value = output_data.get("contig")
        assert isinstance(value, str), (
            f"'contig' should be a string, got {type(value).__name__}"
        )

    def test_mapped_reads_is_integer(self, output_data):
        """Verify 'mapped_reads' is an integer."""
        value = output_data.get("mapped_reads")
        assert isinstance(value, int), (
            f"'mapped_reads' should be an integer, got {type(value).__name__}"
        )

    def test_unmapped_reads_is_integer(self, output_data):
        """Verify 'unmapped_reads' is an integer."""
        value = output_data.get("unmapped_reads")
        assert isinstance(value, int), (
            f"'unmapped_reads' should be an integer, got {type(value).__name__}"
        )

    def test_unmapped_fraction_is_float(self, output_data):
        """Verify 'unmapped_fraction' is a float (or int, which JSON allows)."""
        value = output_data.get("unmapped_fraction")
        assert isinstance(value, (int, float)), (
            f"'unmapped_fraction' should be a number, got {type(value).__name__}"
        )


class TestFieldValues:
    """Tests for verifying correct field values."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_PATH) as f:
            return json.load(f)

    @pytest.fixture
    def extracted_unmap_bit(self):
        """Extract the UNMAP bit from learning_bam_file."""
        return extract_unmap_bit_from_learning_file()

    @pytest.fixture
    def bam_stats(self, extracted_unmap_bit):
        """Compute BAM statistics using the extracted FLAG bit."""
        return compute_bam_stats_with_flag_bit(BAM_FILE, extracted_unmap_bit)

    @pytest.fixture
    def bam_contigs(self):
        """Get valid contig names from BAM header."""
        with pysam.AlignmentFile(BAM_FILE, "rb") as bam:
            return set(bam.references)

    def test_contig_is_valid_reference(self, output_data, bam_contigs):
        """Verify 'contig' is one of the valid reference names from ex1.bam header."""
        value = output_data.get("contig")
        assert value in bam_contigs, (
            f"'contig' should be one of {bam_contigs}, got '{value}'"
        )

    def test_mapped_reads_is_non_negative(self, output_data):
        """Verify 'mapped_reads' is non-negative."""
        value = output_data.get("mapped_reads")
        assert value >= 0, f"'mapped_reads' should be non-negative, got {value}"

    def test_unmapped_reads_is_non_negative(self, output_data):
        """Verify 'unmapped_reads' is non-negative."""
        value = output_data.get("unmapped_reads")
        assert value >= 0, f"'unmapped_reads' should be non-negative, got {value}"

    def test_unmapped_fraction_in_valid_range(self, output_data):
        """Verify 'unmapped_fraction' is between 0 and 1."""
        value = output_data.get("unmapped_fraction")
        assert 0 <= value <= 1, (
            f"'unmapped_fraction' should be between 0 and 1, got {value}"
        )


class TestUnmappedFractionCalculation:
    """Tests for verifying correct unmapped fraction calculation."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_PATH) as f:
            return json.load(f)

    @pytest.fixture
    def raw_json_content(self):
        """Load the raw JSON file content as string."""
        with open(OUTPUT_PATH, "r") as f:
            return f.read()

    def test_unmapped_fraction_has_at_most_6_decimal_places(self, raw_json_content):
        """Verify 'unmapped_fraction' has at most 6 decimal places in the JSON representation.

        This test reads the raw JSON text to check the string representation,
        avoiding floating-point comparison issues.
        """
        # Parse the JSON to find the unmapped_fraction value's string representation
        # Look for the pattern "unmapped_fraction": <number>
        pattern = r'"unmapped_fraction"\s*:\s*(-?\d+\.?\d*(?:[eE][+-]?\d+)?)'
        match = re.search(pattern, raw_json_content)

        assert match, "Could not find 'unmapped_fraction' in JSON file"

        value_str = match.group(1)

        # Check if it's an integer (no decimal point) - always valid
        if '.' not in value_str and 'e' not in value_str.lower():
            return  # Integer values are valid

        # For decimal values, check the number of decimal places
        # Handle scientific notation
        if 'e' in value_str.lower():
            # Scientific notation - convert to check effective decimal places
            try:
                value = float(value_str)
                # Format with enough precision to see all digits
                formatted = f"{value:.10f}".rstrip('0').rstrip('.')
                if '.' in formatted:
                    decimal_places = len(formatted.split('.')[1])
                else:
                    decimal_places = 0
            except ValueError:
                pytest.fail(f"Invalid number format: {value_str}")
        else:
            # Regular decimal - count digits after decimal point
            decimal_part = value_str.split('.')[1] if '.' in value_str else ''
            # Trim trailing zeros for the count
            decimal_places = len(decimal_part.rstrip('0'))

        assert decimal_places <= 6, (
            f"'unmapped_fraction' should have at most 6 decimal places, "
            f"but '{value_str}' has {decimal_places} significant decimal digits"
        )

    def test_unmapped_fraction_matches_expected_rounded_value(self, output_data):
        """Verify unmapped_fraction matches the expected rounded calculation.

        Uses absolute tolerance to handle floating-point representation differences.
        """
        mapped = output_data.get("mapped_reads")
        unmapped = output_data.get("unmapped_reads")
        fraction = output_data.get("unmapped_fraction")

        total = mapped + unmapped
        if total > 0:
            expected_fraction = round(unmapped / total, 6)
            # Use absolute tolerance for floating-point comparison
            assert abs(fraction - expected_fraction) < 0.5e-6, (
                f"'unmapped_fraction' should be approximately {expected_fraction} "
                f"({unmapped}/{total} rounded to 6 decimals), got {fraction}"
            )
        else:
            # When total is 0, fraction must be 0.0
            assert fraction == 0.0, (
                f"'unmapped_fraction' should be 0.0 when total reads is 0, got {fraction}"
            )


class TestDataConsistency:
    """Tests for verifying internal data consistency."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_PATH) as f:
            return json.load(f)

    def test_fraction_consistent_with_counts(self, output_data):
        """Verify the fraction is consistent with the read counts.

        When total reads is 0, fraction must be 0.0.
        When total reads > 0, fraction must equal unmapped/total (rounded to 6 decimals).
        """
        mapped = output_data.get("mapped_reads", 0)
        unmapped = output_data.get("unmapped_reads", 0)
        fraction = output_data.get("unmapped_fraction", 0)

        total = mapped + unmapped
        if total > 0:
            expected = round(unmapped / total, 6)
            # Use tolerance for floating-point comparison
            assert abs(fraction - expected) < 0.5e-6, (
                f"Fraction {fraction} does not match calculation "
                f"round({unmapped}/{total}, 6) = {expected}"
            )
        else:
            # When total is 0, fraction must be exactly 0.0
            assert fraction == 0.0, (
                f"When mapped_reads + unmapped_reads = 0, unmapped_fraction must be 0.0, "
                f"got {fraction}"
            )

    def test_contig_name_not_empty(self, output_data):
        """Verify contig name is not an empty string."""
        contig = output_data.get("contig", "")
        assert contig != "", "'contig' should not be an empty string"
        assert contig.strip() == contig, "'contig' should not have leading/trailing whitespace"


class TestLearningFileCompliance:
    """Tests verifying compliance with learning_bam_file requirements."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_PATH) as f:
            return json.load(f)

    @pytest.fixture
    def extracted_unmap_bit(self):
        """Extract the UNMAP bit from learning_bam_file."""
        return extract_unmap_bit_from_learning_file()

    def test_learning_file_contains_unmap_documentation(self):
        """Verify the learning_bam_file contains the UNMAP flag documentation.

        The file should contain a line documenting the UNMAP bit in the format:
            ##    0x4     4  UNMAP          segment unmapped
        """
        with open(LEARNING_FILE, "r") as f:
            content = f.read()

        # Check for the presence of UNMAP flag documentation
        pattern = r"##\s+0x[0-9a-fA-F]+\s+\d+\s+UNMAP\b"
        matches = re.findall(pattern, content)

        assert len(matches) > 0, (
            "learning_bam_file should contain UNMAP flag documentation "
            "in format: '##  0xN  N  UNMAP'"
        )

    def test_flag_bit_matches_extracted_value(self, output_data, extracted_unmap_bit):
        """Verify the output 'flag_unmapped_bit_from_doc' matches the value extracted from learning_bam_file.

        This test reads the learning_bam_file, parses the UNMAP flag documentation,
        extracts the decimal bit value, and verifies the program used this value.
        """
        flag_bit = output_data.get("flag_unmapped_bit_from_doc")
        assert flag_bit == extracted_unmap_bit, (
            f"'flag_unmapped_bit_from_doc' should be {extracted_unmap_bit} "
            f"(extracted from learning_bam_file), got {flag_bit}. "
            f"The learning_bam_file documents UNMAP as 0x{extracted_unmap_bit:x} = {extracted_unmap_bit}"
        )

    def test_flag_bit_is_valid_power_of_2(self, output_data):
        """Verify the FLAG bit is a valid single bit (power of 2).

        SAM FLAG bits are individual bits in a bitfield, so each must be a power of 2.
        """
        flag_bit = output_data.get("flag_unmapped_bit_from_doc")
        # Check if it's a power of 2 (has exactly one bit set)
        assert flag_bit > 0 and (flag_bit & (flag_bit - 1)) == 0, (
            f"'flag_unmapped_bit_from_doc' should be a power of 2 (single bit), "
            f"got {flag_bit} (binary: {bin(flag_bit)})"
        )


class TestInputFilesExist:
    """Tests to verify input files are present and accessible."""

    def test_bam_file_exists(self):
        """Verify the BAM input file exists."""
        assert os.path.exists(BAM_FILE), f"BAM input file not found: {BAM_FILE}"

    def test_learning_file_exists(self):
        """Verify the learning_bam_file input exists."""
        assert os.path.exists(LEARNING_FILE), f"Learning file not found: {LEARNING_FILE}"

    def test_bam_file_is_valid(self):
        """Verify the BAM file can be opened with pysam."""
        try:
            with pysam.AlignmentFile(BAM_FILE, "rb") as bam:
                _ = bam.references
        except Exception as e:
            pytest.fail(f"Failed to open BAM file with pysam: {e}")


class TestReadsWithNoReferenceName:
    """Tests verifying that reads with no reference name are properly excluded.

    Requirement #2 states that reads with no reference_name must not be counted
    toward any contig's mapped_reads or unmapped_reads totals.
    """

    @pytest.fixture
    def extracted_unmap_bit(self):
        """Extract the UNMAP bit from learning_bam_file."""
        return extract_unmap_bit_from_learning_file()

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_PATH) as f:
            return json.load(f)

    @pytest.fixture
    def bam_stats(self, extracted_unmap_bit):
        """Compute BAM statistics using the reference implementation."""
        return compute_bam_stats_with_flag_bit(BAM_FILE, extracted_unmap_bit)

    def test_reads_with_no_reference_excluded_from_totals(self, output_data, bam_stats, extracted_unmap_bit):
        """Verify that reads with reference_name=None are not counted in any contig's totals.

        This test independently counts all reads with valid reference names and compares
        to the reference implementation to ensure reads without reference names are excluded.
        """
        # Count reads with no reference name in the BAM file
        no_ref_count = count_reads_with_no_reference_name(BAM_FILE)

        # Count total reads in the BAM file
        total_reads_in_bam = 0
        with pysam.AlignmentFile(BAM_FILE, "rb") as bam:
            for _ in bam.fetch(until_eof=True):
                total_reads_in_bam += 1

        # Count total reads accounted for in our reference implementation
        total_in_stats = sum(
            s["mapped"] + s["unmapped"] for s in bam_stats.values()
        )

        # The difference should exactly equal the reads with no reference name
        reads_excluded = total_reads_in_bam - total_in_stats
        assert reads_excluded == no_ref_count, (
            f"Reads with no reference name should be excluded from all contig totals. "
            f"BAM has {total_reads_in_bam} total reads, stats account for {total_in_stats}, "
            f"difference is {reads_excluded} but found {no_ref_count} reads with no reference name"
        )

    def test_output_counts_match_reference_excluding_no_ref_reads(self, output_data, bam_stats, extracted_unmap_bit):
        """Verify the output counts match the reference implementation that excludes no-ref reads.

        The reference implementation (compute_bam_stats_with_flag_bit) explicitly excludes
        reads where reference_name is None or empty. This test verifies the program's output
        matches this reference.
        """
        selected_contig = output_data.get("contig")
        reported_mapped = output_data.get("mapped_reads")
        reported_unmapped = output_data.get("unmapped_reads")

        if selected_contig not in bam_stats:
            pytest.fail(f"Selected contig '{selected_contig}' not found in BAM file")

        expected_mapped = bam_stats[selected_contig]["mapped"]
        expected_unmapped = bam_stats[selected_contig]["unmapped"]

        assert reported_mapped == expected_mapped, (
            f"Mapped reads for '{selected_contig}' should be {expected_mapped} "
            f"(using reference implementation that excludes reads with no reference_name), "
            f"got {reported_mapped}"
        )

        assert reported_unmapped == expected_unmapped, (
            f"Unmapped reads for '{selected_contig}' should be {expected_unmapped} "
            f"(using reference implementation that excludes reads with no reference_name), "
            f"got {reported_unmapped}"
        )

    def test_no_ref_reads_not_attributed_to_any_contig(self, extracted_unmap_bit):
        """Verify that reads with no reference name would not be counted toward any contig.

        This test independently examines the BAM file to ensure our reference implementation
        and expected behavior are consistent: reads with reference_name=None should not
        appear in any contig's counts.
        """
        # Get all contigs from the BAM header
        with pysam.AlignmentFile(BAM_FILE, "rb") as bam:
            all_contigs = set(bam.references)

        # Independently count reads per contig, explicitly checking for None reference
        counts_per_contig = {contig: {"mapped": 0, "unmapped": 0} for contig in all_contigs}
        reads_with_no_ref = []

        with pysam.AlignmentFile(BAM_FILE, "rb") as bam:
            for read in bam.fetch(until_eof=True):
                ref_name = read.reference_name
                # Explicitly capture reads with no reference name
                if ref_name is None or ref_name == "":
                    reads_with_no_ref.append({
                        "query_name": read.query_name,
                        "flag": read.flag,
                        "reference_name": ref_name
                    })
                elif ref_name in counts_per_contig:
                    is_unmapped = (read.flag & extracted_unmap_bit) != 0
                    if is_unmapped:
                        counts_per_contig[ref_name]["unmapped"] += 1
                    else:
                        counts_per_contig[ref_name]["mapped"] += 1

        # Verify that our reference implementation matches this independent count
        bam_stats = compute_bam_stats_with_flag_bit(BAM_FILE, extracted_unmap_bit)
        for contig in all_contigs:
            assert bam_stats[contig]["mapped"] == counts_per_contig[contig]["mapped"], (
                f"Reference implementation mismatch for contig '{contig}' mapped reads"
            )
            assert bam_stats[contig]["unmapped"] == counts_per_contig[contig]["unmapped"], (
                f"Reference implementation mismatch for contig '{contig}' unmapped reads"
            )


class TestBAMFileAnalysis:
    """Tests that validate the analysis against the actual BAM file data.

    These tests use the FLAG bit extracted from learning_bam_file to classify
    reads, ensuring the test validates the same interpretation path required
    by the task specification.
    """

    @pytest.fixture
    def extracted_unmap_bit(self):
        """Extract the UNMAP bit from learning_bam_file."""
        return extract_unmap_bit_from_learning_file()

    @pytest.fixture
    def bam_stats(self, extracted_unmap_bit):
        """Compute actual statistics from the BAM file using the extracted FLAG bit.

        Uses (read.flag & unmapped_bit) != 0 to classify reads, matching the
        required interpretation from learning_bam_file documentation.
        """
        return compute_bam_stats_with_flag_bit(BAM_FILE, extracted_unmap_bit)

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_PATH) as f:
            return json.load(f)

    def test_selected_contig_has_max_fraction_with_tiebreaking(self, output_data, bam_stats):
        """Verify the selected contig has the maximum unmapped fraction with proper tie-breaking.

        When multiple contigs have the same maximum fraction, the lexicographically
        smallest contig name should be selected.
        """
        selected_contig = output_data.get("contig")
        expected_contig = get_expected_contig_with_tiebreaking(bam_stats)

        assert selected_contig == expected_contig, (
            f"Selected contig '{selected_contig}' does not match expected '{expected_contig}'. "
            f"Expected contig has max fraction {bam_stats[expected_contig]['fraction']:.6f} "
            f"and is lexicographically smallest among ties. "
            f"All contigs: {[(c, s['fraction']) for c, s in sorted(bam_stats.items())]}"
        )

    def test_counts_match_actual_bam_data_using_flag_bit(self, output_data, bam_stats, extracted_unmap_bit):
        """Verify the mapped/unmapped counts match BAM file data classified by extracted FLAG bit.

        Uses the UNMAP bit extracted from learning_bam_file to classify reads,
        ensuring the output matches the required interpretation.
        """
        selected_contig = output_data.get("contig")
        reported_mapped = output_data.get("mapped_reads")
        reported_unmapped = output_data.get("unmapped_reads")

        if selected_contig not in bam_stats:
            pytest.fail(f"Selected contig '{selected_contig}' not found in BAM file")

        actual_mapped = bam_stats[selected_contig]["mapped"]
        actual_unmapped = bam_stats[selected_contig]["unmapped"]

        assert reported_mapped == actual_mapped, (
            f"Mapped reads mismatch for {selected_contig}: "
            f"reported {reported_mapped}, expected {actual_mapped} "
            f"(using FLAG bit {extracted_unmap_bit} from learning_bam_file)"
        )

        assert reported_unmapped == actual_unmapped, (
            f"Unmapped reads mismatch for {selected_contig}: "
            f"reported {reported_unmapped}, expected {actual_unmapped} "
            f"(using FLAG bit {extracted_unmap_bit} from learning_bam_file)"
        )

    def test_fraction_matches_actual_bam_data(self, output_data, bam_stats):
        """Verify the unmapped fraction matches the computed value from BAM data."""
        selected_contig = output_data.get("contig")
        reported_fraction = output_data.get("unmapped_fraction")

        if selected_contig not in bam_stats:
            pytest.fail(f"Selected contig '{selected_contig}' not found in BAM file")

        expected_fraction = round(bam_stats[selected_contig]["fraction"], 6)

        # Use tolerance for floating-point comparison
        assert abs(reported_fraction - expected_fraction) < 0.5e-6, (
            f"Unmapped fraction mismatch for {selected_contig}: "
            f"reported {reported_fraction}, expected {expected_fraction}"
        )

    def test_all_contigs_considered(self, output_data, bam_stats):
        """Verify the selected contig is among those in the BAM file."""
        selected_contig = output_data.get("contig")
        assert selected_contig in bam_stats, (
            f"Selected contig '{selected_contig}' is not a valid reference in BAM file. "
            f"Valid references: {list(bam_stats.keys())}"
        )

    def test_no_higher_fraction_contig_exists(self, output_data, bam_stats):
        """Verify no other contig has a higher unmapped fraction than the selected one."""
        selected_contig = output_data.get("contig")
        selected_fraction = bam_stats[selected_contig]["fraction"]

        for contig, stats in bam_stats.items():
            assert stats["fraction"] <= selected_fraction, (
                f"Contig '{contig}' has higher fraction ({stats['fraction']:.6f}) "
                f"than selected contig '{selected_contig}' ({selected_fraction:.6f})"
            )

    def test_tiebreaker_is_lexicographic(self, output_data, bam_stats):
        """If there are ties for max fraction, verify the lexicographically smallest was chosen."""
        selected_contig = output_data.get("contig")
        selected_fraction = bam_stats[selected_contig]["fraction"]

        # Find all contigs with the same fraction as selected
        tied_contigs = [
            contig for contig, stats in bam_stats.items()
            if stats["fraction"] == selected_fraction
        ]

        if len(tied_contigs) > 1:
            # Selected should be lexicographically smallest
            expected = min(tied_contigs)
            assert selected_contig == expected, (
                f"Tie-breaking failed: contigs {tied_contigs} all have fraction {selected_fraction:.6f}. "
                f"Expected lexicographically smallest '{expected}', got '{selected_contig}'"
            )


class TestFlagBitUsage:
    """Tests verifying that the correct FLAG bit interpretation is used."""

    @pytest.fixture
    def extracted_unmap_bit(self):
        """Extract the UNMAP bit from learning_bam_file."""
        return extract_unmap_bit_from_learning_file()

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_PATH) as f:
            return json.load(f)

    def test_output_flag_bit_equals_extracted(self, output_data, extracted_unmap_bit):
        """Verify the output FLAG bit value equals what was extracted from learning_bam_file.

        This is the primary test for Requirement #1: the unmapped bit must be
        extracted from learning_bam_file, not hardcoded.
        """
        output_bit = output_data.get("flag_unmapped_bit_from_doc")
        assert output_bit == extracted_unmap_bit, (
            f"FLAG bit mismatch: output has {output_bit}, but learning_bam_file "
            f"documents UNMAP as {extracted_unmap_bit}. The program must extract "
            f"this value from learning_bam_file, not hardcode it."
        )

    def test_extracted_flag_bit_is_valid_power_of_2(self, extracted_unmap_bit):
        """Verify the extracted FLAG bit is a valid single bit (power of 2).

        SAM FLAG bits are individual bits in a bitfield, so the extracted value
        must be a power of 2 to be a valid FLAG bit.
        """
        assert extracted_unmap_bit > 0 and (extracted_unmap_bit & (extracted_unmap_bit - 1)) == 0, (
            f"Extracted UNMAP bit from learning_bam_file should be a power of 2 (single bit), "
            f"got {extracted_unmap_bit} (binary: {bin(extracted_unmap_bit)})"
        )

    def test_reads_classified_consistently_with_flag_bit(self, output_data, extracted_unmap_bit):
        """Verify read counts are consistent with FLAG bit classification.

        Independently count reads using the extracted FLAG bit and compare
        to the output values.
        """
        selected_contig = output_data.get("contig")
        reported_mapped = output_data.get("mapped_reads")
        reported_unmapped = output_data.get("unmapped_reads")

        # Count reads using the extracted FLAG bit, excluding reads with no reference name
        actual_mapped = 0
        actual_unmapped = 0

        with pysam.AlignmentFile(BAM_FILE, "rb") as bam:
            for read in bam.fetch(until_eof=True):
                # Only count reads with valid reference name matching the selected contig
                if read.reference_name == selected_contig:
                    if (read.flag & extracted_unmap_bit) != 0:
                        actual_unmapped += 1
                    else:
                        actual_mapped += 1

        assert reported_mapped == actual_mapped, (
            f"Mapped read count inconsistent with FLAG bit {extracted_unmap_bit} classification: "
            f"output={reported_mapped}, computed={actual_mapped}"
        )

        assert reported_unmapped == actual_unmapped, (
            f"Unmapped read count inconsistent with FLAG bit {extracted_unmap_bit} classification: "
            f"output={reported_unmapped}, computed={actual_unmapped}"
        )


class TestZeroReadContigHandling:
    """Tests for proper handling of contigs with zero total reads.

    The task does not require the selected contig to have any reads.
    If all contigs have zero reads, the correct output has 0 counts and 0.0 fraction.
    """

    @pytest.fixture
    def extracted_unmap_bit(self):
        """Extract the UNMAP bit from learning_bam_file."""
        return extract_unmap_bit_from_learning_file()

    @pytest.fixture
    def bam_stats(self, extracted_unmap_bit):
        """Compute BAM statistics using the extracted FLAG bit."""
        return compute_bam_stats_with_flag_bit(BAM_FILE, extracted_unmap_bit)

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_PATH) as f:
            return json.load(f)

    def test_zero_total_reads_implies_zero_fraction(self, output_data):
        """Verify that when mapped + unmapped = 0, the fraction is exactly 0.0."""
        mapped = output_data.get("mapped_reads", 0)
        unmapped = output_data.get("unmapped_reads", 0)
        fraction = output_data.get("unmapped_fraction")

        if mapped + unmapped == 0:
            assert fraction == 0.0, (
                f"When mapped_reads + unmapped_reads = 0, unmapped_fraction must be 0.0, "
                f"got {fraction}"
            )

    def test_max_fraction_selection_handles_all_zero_contigs(self, bam_stats):
        """Verify the selection logic handles the case where all contigs have 0 reads.

        In this case, all contigs have fraction 0.0, so the lexicographically smallest
        should be selected.
        """
        # Check if any contig has reads
        has_reads = any(
            s["mapped"] + s["unmapped"] > 0
            for s in bam_stats.values()
        )

        if not has_reads:
            # All contigs have 0 reads, so all have fraction 0.0
            # The lexicographically smallest should be selected
            expected_contig = min(bam_stats.keys())
            with open(OUTPUT_PATH) as f:
                output_data = json.load(f)
            selected_contig = output_data.get("contig")

            assert selected_contig == expected_contig, (
                f"When all contigs have 0 reads, should select lexicographically smallest "
                f"('{expected_contig}'), got '{selected_contig}'"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
