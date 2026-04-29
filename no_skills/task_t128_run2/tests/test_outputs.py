"""Auto-generated expectation tests for fraud threshold transfer task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for finding the optimal fraud-flagging
amount threshold and applying it across multiple datasets.
"""

import os
from pathlib import Path

import pandas as pd
import pytest

# Constants
OUTPUT_FILE = "/root/fraud_threshold_transfer_report.xlsx"
INPUT_CREDITCARD = "/root/creditcard.csv"
INPUT_PURCHASES = "/root/purchases.csv"
INPUT_TRANSACTIONS = "/root/transactions.csv"

# Required metrics in threshold_result sheet
REQUIRED_METRICS = [
    "best_threshold_T",
    "max_f1",
    "precision_at_T",
    "recall_at_T",
    "creditcard_fraud_rate",
    "transactions_flag_rate",
    "transactions_usd_flagged_amount",
    "purchases_flag_rate",
    "purchases_flagged_amount",
]


class TestOutputFileExists:
    """Tests for output file existence and basic validity."""

    def test_output_file_exists(self):
        """Verify output Excel file was created at the specified path."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

    def test_output_file_is_not_empty(self):
        """Verify output file has content (non-zero size)."""
        assert os.path.getsize(OUTPUT_FILE) > 0, "Output file is empty"

    def test_output_file_is_valid_excel(self):
        """Verify output file is a valid Excel file that can be read."""
        try:
            xls = pd.ExcelFile(OUTPUT_FILE)
            assert xls is not None
        except Exception as e:
            pytest.fail(f"Failed to read Excel file: {e}")


class TestExcelSheetStructure:
    """Tests for Excel workbook sheet structure."""

    @pytest.fixture
    def excel_file(self):
        """Load the Excel file for testing."""
        return pd.ExcelFile(OUTPUT_FILE)

    def test_has_exactly_two_sheets(self, excel_file):
        """Verify workbook contains exactly two sheets."""
        assert len(excel_file.sheet_names) == 2, (
            f"Expected exactly 2 sheets, found {len(excel_file.sheet_names)}: {excel_file.sheet_names}"
        )

    def test_has_threshold_result_sheet(self, excel_file):
        """Verify workbook contains 'threshold_result' sheet."""
        assert "threshold_result" in excel_file.sheet_names, (
            f"Sheet 'threshold_result' not found. Available sheets: {excel_file.sheet_names}"
        )

    def test_has_validation_sheet(self, excel_file):
        """Verify workbook contains 'validation' sheet."""
        assert "validation" in excel_file.sheet_names, (
            f"Sheet 'validation' not found. Available sheets: {excel_file.sheet_names}"
        )


class TestThresholdResultSheet:
    """Tests for the threshold_result sheet content and structure."""

    @pytest.fixture
    def threshold_df(self):
        """Load the threshold_result sheet as a DataFrame."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="threshold_result")

    def test_has_metric_column(self, threshold_df):
        """Verify threshold_result sheet has 'metric' column."""
        assert "metric" in threshold_df.columns, (
            f"Column 'metric' not found. Columns: {list(threshold_df.columns)}"
        )

    def test_has_value_column(self, threshold_df):
        """Verify threshold_result sheet has 'value' column."""
        assert "value" in threshold_df.columns, (
            f"Column 'value' not found. Columns: {list(threshold_df.columns)}"
        )

    def test_has_exactly_two_columns(self, threshold_df):
        """Verify threshold_result sheet has exactly two columns (metric and value)."""
        assert len(threshold_df.columns) == 2, (
            f"Expected exactly 2 columns, found {len(threshold_df.columns)}: {list(threshold_df.columns)}"
        )

    def test_has_all_required_metrics(self, threshold_df):
        """Verify all required metrics are present in the threshold_result sheet."""
        metrics_in_file = set(threshold_df["metric"].astype(str).str.strip().tolist())
        missing_metrics = set(REQUIRED_METRICS) - metrics_in_file
        assert len(missing_metrics) == 0, (
            f"Missing required metrics: {missing_metrics}"
        )

    def test_has_exactly_nine_metrics(self, threshold_df):
        """Verify threshold_result sheet has exactly 9 metric rows."""
        assert len(threshold_df) == 9, (
            f"Expected exactly 9 metric rows, found {len(threshold_df)}"
        )

    def test_no_duplicate_metrics(self, threshold_df):
        """Verify there are no duplicate metric names."""
        metrics = threshold_df["metric"].astype(str).str.strip().tolist()
        duplicates = [m for m in metrics if metrics.count(m) > 1]
        assert len(set(duplicates)) == 0, f"Duplicate metrics found: {set(duplicates)}"


class TestMetricValues:
    """Tests for individual metric value validity."""

    @pytest.fixture
    def metrics_dict(self):
        """Load metrics as a dictionary for easy access."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="threshold_result")
        return dict(zip(df["metric"].astype(str).str.strip(), df["value"]))

    def test_best_threshold_is_numeric(self, metrics_dict):
        """Verify best_threshold_T is a numeric value."""
        value = metrics_dict.get("best_threshold_T")
        assert value is not None, "best_threshold_T not found"
        assert pd.notna(value) and isinstance(float(value), float), (
            f"best_threshold_T should be numeric, got: {value}"
        )

    def test_best_threshold_is_non_negative(self, metrics_dict):
        """Verify best_threshold_T is >= 0 (amounts cannot be negative)."""
        value = float(metrics_dict.get("best_threshold_T"))
        assert value >= 0, f"best_threshold_T should be >= 0, got: {value}"

    def test_max_f1_is_valid_score(self, metrics_dict):
        """Verify max_f1 is between 0 and 1 (inclusive)."""
        value = float(metrics_dict.get("max_f1"))
        assert 0 <= value <= 1, f"max_f1 should be between 0 and 1, got: {value}"

    def test_precision_at_t_is_valid_score(self, metrics_dict):
        """Verify precision_at_T is between 0 and 1 (inclusive)."""
        value = float(metrics_dict.get("precision_at_T"))
        assert 0 <= value <= 1, f"precision_at_T should be between 0 and 1, got: {value}"

    def test_recall_at_t_is_valid_score(self, metrics_dict):
        """Verify recall_at_T is between 0 and 1 (inclusive)."""
        value = float(metrics_dict.get("recall_at_T"))
        assert 0 <= value <= 1, f"recall_at_T should be between 0 and 1, got: {value}"

    def test_creditcard_fraud_rate_is_valid_rate(self, metrics_dict):
        """Verify creditcard_fraud_rate is between 0 and 1."""
        value = float(metrics_dict.get("creditcard_fraud_rate"))
        assert 0 <= value <= 1, f"creditcard_fraud_rate should be between 0 and 1, got: {value}"

    def test_transactions_flag_rate_is_valid_rate(self, metrics_dict):
        """Verify transactions_flag_rate is between 0 and 1."""
        value = float(metrics_dict.get("transactions_flag_rate"))
        assert 0 <= value <= 1, f"transactions_flag_rate should be between 0 and 1, got: {value}"

    def test_transactions_usd_flagged_amount_is_non_negative(self, metrics_dict):
        """Verify transactions_usd_flagged_amount is >= 0."""
        value = float(metrics_dict.get("transactions_usd_flagged_amount"))
        assert value >= 0, f"transactions_usd_flagged_amount should be >= 0, got: {value}"

    def test_purchases_flag_rate_is_valid_rate(self, metrics_dict):
        """Verify purchases_flag_rate is between 0 and 1."""
        value = float(metrics_dict.get("purchases_flag_rate"))
        assert 0 <= value <= 1, f"purchases_flag_rate should be between 0 and 1, got: {value}"

    def test_purchases_flagged_amount_is_non_negative(self, metrics_dict):
        """Verify purchases_flagged_amount is >= 0."""
        value = float(metrics_dict.get("purchases_flagged_amount"))
        assert value >= 0, f"purchases_flagged_amount should be >= 0, got: {value}"


class TestValidationSheet:
    """Tests for the validation sheet content and structure."""

    @pytest.fixture
    def validation_df(self):
        """Load the validation sheet as a DataFrame."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="validation")

    def test_validation_has_amount_column(self, validation_df):
        """Verify validation sheet has an Amount column (case-insensitive)."""
        columns_lower = [c.lower() for c in validation_df.columns]
        assert "amount" in columns_lower, (
            f"Column 'Amount' not found in validation sheet. Columns: {list(validation_df.columns)}"
        )

    def test_validation_has_class_column(self, validation_df):
        """Verify validation sheet has a Class column (case-insensitive)."""
        columns_lower = [c.lower() for c in validation_df.columns]
        assert "class" in columns_lower, (
            f"Column 'Class' not found in validation sheet. Columns: {list(validation_df.columns)}"
        )

    def test_validation_has_exactly_10_rows(self, validation_df):
        """Verify validation sheet contains exactly 10 rows (top 10 amounts)."""
        assert len(validation_df) == 10, (
            f"Expected exactly 10 rows in validation sheet, found {len(validation_df)}"
        )

    def test_validation_amounts_are_sorted_descending(self, validation_df):
        """Verify validation amounts are sorted in descending order."""
        # Find Amount column (case-insensitive)
        amount_col = None
        for col in validation_df.columns:
            if col.lower() == "amount":
                amount_col = col
                break

        amounts = validation_df[amount_col].tolist()
        assert amounts == sorted(amounts, reverse=True), (
            "Validation amounts should be sorted in descending order"
        )

    def test_validation_amounts_are_positive(self, validation_df):
        """Verify all validation amounts are positive."""
        # Find Amount column (case-insensitive)
        amount_col = None
        for col in validation_df.columns:
            if col.lower() == "amount":
                amount_col = col
                break

        amounts = validation_df[amount_col].tolist()
        assert all(a > 0 for a in amounts), "All validation amounts should be positive"

    def test_validation_class_values_are_binary(self, validation_df):
        """Verify Class values are binary (0 or 1)."""
        # Find Class column (case-insensitive)
        class_col = None
        for col in validation_df.columns:
            if col.lower() == "class":
                class_col = col
                break

        classes = validation_df[class_col].tolist()
        assert all(c in [0, 1] for c in classes), (
            f"Class values should be 0 or 1, found: {set(classes)}"
        )


class TestThresholdConsistency:
    """Tests for consistency between threshold and derived metrics."""

    @pytest.fixture
    def metrics_dict(self):
        """Load metrics as a dictionary."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="threshold_result")
        return dict(zip(df["metric"].astype(str).str.strip(), df["value"]))

    def test_f1_score_formula_consistency(self, metrics_dict):
        """Verify F1 score is consistent with precision and recall (F1 = 2*P*R/(P+R))."""
        precision = float(metrics_dict.get("precision_at_T"))
        recall = float(metrics_dict.get("recall_at_T"))
        f1 = float(metrics_dict.get("max_f1"))

        # Handle edge case where precision + recall = 0
        if precision + recall == 0:
            expected_f1 = 0
        else:
            expected_f1 = 2 * precision * recall / (precision + recall)

        # Allow small floating point tolerance
        assert abs(f1 - expected_f1) < 0.0001, (
            f"F1 score {f1} inconsistent with precision {precision} and recall {recall}. "
            f"Expected F1 = {expected_f1}"
        )

    def test_threshold_is_from_creditcard_amounts(self, metrics_dict):
        """Verify threshold is a distinct Amount value from creditcard.csv."""
        threshold = float(metrics_dict.get("best_threshold_T"))

        # Load creditcard.csv and get distinct amounts
        creditcard_df = pd.read_csv(INPUT_CREDITCARD)
        distinct_amounts = set(creditcard_df["Amount"].unique())

        # Threshold should be one of the distinct amounts
        assert threshold in distinct_amounts, (
            f"Threshold {threshold} is not a distinct Amount value from creditcard.csv"
        )


class TestCrossDatasetConsistency:
    """Tests for consistency between threshold application across datasets."""

    @pytest.fixture
    def metrics_dict(self):
        """Load metrics as a dictionary."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="threshold_result")
        return dict(zip(df["metric"].astype(str).str.strip(), df["value"]))

    def test_transactions_flag_rate_matches_data(self, metrics_dict):
        """Verify transactions_flag_rate is consistent with applying threshold to transactions.csv."""
        threshold = float(metrics_dict.get("best_threshold_T"))
        reported_rate = float(metrics_dict.get("transactions_flag_rate"))

        # Load transactions.csv (no header, 3rd column is amount)
        trans_df = pd.read_csv(INPUT_TRANSACTIONS, header=None)
        amounts = pd.to_numeric(trans_df.iloc[:, 2], errors='coerce')

        # Calculate expected flag rate
        total_rows = len(amounts)
        flagged_rows = (amounts >= threshold).sum()
        expected_rate = flagged_rows / total_rows if total_rows > 0 else 0

        # Allow small tolerance
        assert abs(reported_rate - expected_rate) < 0.0001, (
            f"transactions_flag_rate {reported_rate} doesn't match calculated rate {expected_rate}"
        )

    def test_transactions_usd_flagged_amount_matches_data(self, metrics_dict):
        """Verify transactions_usd_flagged_amount is consistent with applying threshold."""
        threshold = float(metrics_dict.get("best_threshold_T"))
        reported_amount = float(metrics_dict.get("transactions_usd_flagged_amount"))

        # Load transactions.csv (no header, 3rd column is amount, 4th is currency)
        trans_df = pd.read_csv(INPUT_TRANSACTIONS, header=None)
        amounts = pd.to_numeric(trans_df.iloc[:, 2], errors='coerce')
        currencies = trans_df.iloc[:, 3].astype(str).str.strip()

        # Filter for USD and amount >= threshold
        usd_mask = currencies == "USD"
        flagged_mask = amounts >= threshold
        expected_amount = amounts[usd_mask & flagged_mask].sum()

        # Allow small tolerance for floating point
        assert abs(reported_amount - expected_amount) < 0.01, (
            f"transactions_usd_flagged_amount {reported_amount} doesn't match calculated {expected_amount}"
        )

    def test_purchases_flag_rate_matches_data(self, metrics_dict):
        """Verify purchases_flag_rate is consistent with applying threshold to purchases.csv."""
        threshold = float(metrics_dict.get("best_threshold_T"))
        reported_rate = float(metrics_dict.get("purchases_flag_rate"))

        # Load purchases.csv
        purchases_df = pd.read_csv(INPUT_PURCHASES)
        amounts = pd.to_numeric(purchases_df["amount"], errors='coerce')

        # Calculate expected flag rate
        total_rows = len(amounts)
        flagged_rows = (amounts >= threshold).sum()
        expected_rate = flagged_rows / total_rows if total_rows > 0 else 0

        # Allow small tolerance
        assert abs(reported_rate - expected_rate) < 0.0001, (
            f"purchases_flag_rate {reported_rate} doesn't match calculated rate {expected_rate}"
        )

    def test_purchases_flagged_amount_matches_data(self, metrics_dict):
        """Verify purchases_flagged_amount is consistent with applying threshold."""
        threshold = float(metrics_dict.get("best_threshold_T"))
        reported_amount = float(metrics_dict.get("purchases_flagged_amount"))

        # Load purchases.csv
        purchases_df = pd.read_csv(INPUT_PURCHASES)
        amounts = pd.to_numeric(purchases_df["amount"], errors='coerce')

        # Calculate expected flagged amount
        expected_amount = amounts[amounts >= threshold].sum()

        # Allow small tolerance for floating point
        assert abs(reported_amount - expected_amount) < 0.01, (
            f"purchases_flagged_amount {reported_amount} doesn't match calculated {expected_amount}"
        )


class TestCreditcardFraudRateConsistency:
    """Tests for creditcard fraud rate consistency."""

    @pytest.fixture
    def metrics_dict(self):
        """Load metrics as a dictionary."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="threshold_result")
        return dict(zip(df["metric"].astype(str).str.strip(), df["value"]))

    def test_fraud_rate_matches_data(self, metrics_dict):
        """Verify creditcard_fraud_rate matches the mean of Class column."""
        reported_rate = float(metrics_dict.get("creditcard_fraud_rate"))

        # Load creditcard.csv
        creditcard_df = pd.read_csv(INPUT_CREDITCARD)
        expected_rate = creditcard_df["Class"].mean()

        # Allow small tolerance
        assert abs(reported_rate - expected_rate) < 0.0001, (
            f"creditcard_fraud_rate {reported_rate} doesn't match calculated {expected_rate}"
        )


class TestValidationSheetMatchesTopAmounts:
    """Tests to verify validation sheet contains the actual top 10 amounts."""

    def test_validation_contains_top_10_amounts(self):
        """Verify validation sheet contains the top 10 Amount values from creditcard.csv."""
        # Load creditcard.csv and get top 10 amounts
        creditcard_df = pd.read_csv(INPUT_CREDITCARD)
        top_10_amounts = creditcard_df.nlargest(10, "Amount")["Amount"].tolist()

        # Load validation sheet
        validation_df = pd.read_excel(OUTPUT_FILE, sheet_name="validation")

        # Find Amount column (case-insensitive)
        amount_col = None
        for col in validation_df.columns:
            if col.lower() == "amount":
                amount_col = col
                break

        validation_amounts = validation_df[amount_col].tolist()

        # Compare (allowing for floating point comparison)
        for i, (expected, actual) in enumerate(zip(top_10_amounts, validation_amounts)):
            assert abs(expected - actual) < 0.01, (
                f"Row {i}: Expected amount {expected}, got {actual}"
            )

    def test_validation_class_values_match_source(self):
        """Verify validation Class values match the source creditcard.csv data."""
        # Load creditcard.csv and get top 10 rows by Amount
        creditcard_df = pd.read_csv(INPUT_CREDITCARD)
        top_10_rows = creditcard_df.nlargest(10, "Amount")[["Amount", "Class"]]

        # Load validation sheet
        validation_df = pd.read_excel(OUTPUT_FILE, sheet_name="validation")

        # Find columns (case-insensitive)
        amount_col = class_col = None
        for col in validation_df.columns:
            if col.lower() == "amount":
                amount_col = col
            if col.lower() == "class":
                class_col = col

        # Compare Class values
        expected_classes = top_10_rows["Class"].tolist()
        actual_classes = validation_df[class_col].tolist()

        assert expected_classes == actual_classes, (
            f"Validation Class values don't match source. "
            f"Expected: {expected_classes}, Got: {actual_classes}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
