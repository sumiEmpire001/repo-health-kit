import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from audit import main


class JsonOutputTests(unittest.TestCase):
    def test_json_reports_missing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main([directory, '--json']), 0)
            data = json.loads(out.getvalue())
            self.assertFalse(data['healthy'])
            self.assertEqual(set(data['checks']), {'README', 'Git ignore', 'License'})

    def test_json_reports_healthy_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            for filename in ('README.md', '.gitignore', 'LICENSE'):
                (Path(directory) / filename).touch()
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                main(['--json', directory])
            self.assertTrue(json.loads(out.getvalue())['healthy'])

    def test_default_output_is_human_readable(self):
        with tempfile.TemporaryDirectory() as directory:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                main([directory])
            self.assertIn('README: MISSING', out.getvalue())

    def test_invalid_path_exits_with_argparse_error(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = str(Path(directory) / 'missing')
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                with self.assertRaises(SystemExit) as caught:
                    main([missing])
            self.assertEqual(caught.exception.code, 2)
            self.assertIn('Repository directory not found', err.getvalue())

    def test_module_entry_point_exits_successfully(self):
        import runpy
        import sys
        from unittest.mock import patch

        with tempfile.TemporaryDirectory() as directory:
            out = io.StringIO()
            with patch.object(sys, 'argv', ['audit.py', '--json', directory]):
                with contextlib.redirect_stdout(out):
                    with self.assertRaises(SystemExit) as caught:
                        runpy.run_module('audit', run_name='__main__')
            self.assertEqual(caught.exception.code, 0)
            self.assertIn('"healthy": false', out.getvalue())

    def test_strict_mode_fails_on_missing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                status = main(['--strict', directory])
            self.assertEqual(status, 1)
            self.assertIn('README: MISSING', out.getvalue())

    def test_strict_mode_succeeds_on_complete_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            for filename in ('README.md', '.gitignore', 'LICENSE'):
                (Path(directory) / filename).touch()
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                status = main([directory, '--strict'])
            self.assertEqual(status, 0)
            self.assertIn('License: OK', out.getvalue())

    def test_strict_mode_keeps_json_machine_readable(self):
        with tempfile.TemporaryDirectory() as directory:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                status = main(['--json', '--strict', directory])
            self.assertEqual(status, 1)
            self.assertFalse(json.loads(out.getvalue())['healthy'])

    def test_sample_report_matches_empty_directory_output(self):
        sample_path = Path(__file__).resolve().parent / 'examples' / 'sample-report.json'
        expected = json.loads(sample_path.read_text(encoding='utf-8'))
        with tempfile.TemporaryDirectory() as directory:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main(['--json', directory]), 0)
            self.assertEqual(json.loads(out.getvalue()), expected)

    def test_html_report_for_missing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main(['--html', directory]), 0)
            self.assertIn('<!doctype html>', out.getvalue())
            self.assertIn('Needs attention', out.getvalue())
            self.assertIn('README</th><td>MISSING', out.getvalue())

    def test_html_report_for_healthy_repository_and_strict(self):
        with tempfile.TemporaryDirectory() as directory:
            for filename in ('README.md', '.gitignore', 'LICENSE'):
                (Path(directory) / filename).touch()
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main(['--html', '--strict', directory]), 0)
            self.assertIn('Overall status: <strong>Healthy</strong>', out.getvalue())
            self.assertIn('License</th><td>OK', out.getvalue())

    def test_html_strict_fails_for_missing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main(['--strict', '--html', directory]), 1)
            self.assertIn('<html lang="en">', out.getvalue())

    def test_html_escapes_directory_name(self):
        with tempfile.TemporaryDirectory() as directory:
            special = Path(directory) / 'a&b'
            special.mkdir()
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main(['--html', str(special)]), 0)
            self.assertIn('a&amp;b', out.getvalue())
            self.assertNotIn('a&b</code>', out.getvalue())

    def test_html_and_json_are_mutually_exclusive(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            with self.assertRaises(SystemExit) as caught:
                main(['--html', '--json'])
        self.assertEqual(caught.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
