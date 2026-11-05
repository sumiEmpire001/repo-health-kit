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


if __name__ == '__main__':
    unittest.main()
