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


if __name__ == '__main__':
    unittest.main()
