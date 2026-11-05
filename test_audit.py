"""Tests for repository hygiene checks using only Python's standard library."""

import tempfile
import unittest
from pathlib import Path

from audit import audit


class AuditTests(unittest.TestCase):
    def test_empty_directory_reports_all_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(audit(directory), {
                "README": False,
                "Git ignore": False,
                "License": False,
            })

    def test_existing_files_are_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("README.md", ".gitignore", "LICENSE"):
                (root / name).write_text("", encoding="utf-8")
            self.assertTrue(all(audit(root).values()))

    def test_directories_do_not_count_as_files(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "README.md").mkdir()
            self.assertFalse(audit(directory)["README"])

    def test_nonexistent_path_raises_value_error(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing"
            with self.assertRaisesRegex(ValueError, "Repository directory not found"):
                audit(missing)


if __name__ == "__main__":
    unittest.main()
