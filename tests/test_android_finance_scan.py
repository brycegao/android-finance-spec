#!/usr/bin/env python3
"""Regression tests for the Android finance scanner."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "skills" / "android-finance-spec" / "scripts" / "android_finance_scan.py"


def run_scan(path: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCANNER), str(ROOT / path)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


class AndroidFinanceScanTest(unittest.TestCase):
    def test_bad_example_reports_expected_findings(self) -> None:
        result = run_scan("examples/bad-android-finance")

        self.assertEqual(result.returncode, 1)
        self.assertIn("FIN_FLOATING_DECIMAL_FIELD", result.stdout)
        self.assertIn("FIN_TO_DOUBLE_FLOAT", result.stdout)
        self.assertIn("FIN_MANUAL_FORMAT", result.stdout)
        self.assertIn("RTL_LEFT_RIGHT_XML", result.stdout)
        self.assertIn("I18N_HARDCODED_ANDROID_TEXT", result.stdout)
        self.assertIn("KOTLIN_NOT_NULL_ASSERT", result.stdout)
        self.assertIn("KOTLIN_GLOBAL_SCOPE", result.stdout)

    def test_fixed_example_is_clean(self) -> None:
        result = run_scan("examples/fixed-android-finance")

        self.assertEqual(result.returncode, 0)
        self.assertIn("No first-pass issues found.", result.stdout)


if __name__ == "__main__":
    unittest.main()
