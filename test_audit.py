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

    def test_alternative_readme_and_license_filenames(self):
        readme_names = ('README.md', 'README.rst', 'README.txt', 'README')
        license_names = ('LICENSE', 'LICENSE.md', 'LICENSE.txt', 'LICENCE', 'LICENCE.md', 'LICENCE.txt')
        for readme in readme_names:
            for license_name in license_names:
                with self.subTest(readme=readme, license=license_name):
                    with tempfile.TemporaryDirectory() as directory:
                        root = Path(directory)
                        (root / readme).touch()
                        (root / license_name).touch()
                        self.assertTrue(audit(root)['README'])
                        self.assertTrue(audit(root)['License'])

    def test_unrecognized_names_do_not_count(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.pdf').touch()
            (root / 'COPYING').touch()
            self.assertFalse(audit(root)['README'])
            self.assertFalse(audit(root)['License'])

    def test_alternative_names_must_be_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.rst').mkdir()
            (root / 'LICENCE.txt').mkdir()
            self.assertFalse(audit(root)['README'])
            self.assertFalse(audit(root)['License'])

    def test_mixed_case_supported_filenames(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('ReadMe.Md', '.GITIGNORE', 'LiCeNsE.TxT'):
                (root / name).touch()
            self.assertTrue(all(audit(root).values()))

    def test_mixed_case_directories_do_not_count(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('ReadMe.Md', '.GITIGNORE', 'LiCeNsE.TxT'):
                (root / name).mkdir()
            self.assertFalse(any(audit(root).values()))

    def test_unrelated_mixed_case_files_do_not_count(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.PDF').touch()
            (root / 'COPYING').touch()
            self.assertFalse(any(audit(root).values()))


if __name__ == "__main__":
    unittest.main()
