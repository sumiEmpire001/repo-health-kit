import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

from audit import render_html
import generate_sample_html


class ReportParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = []
        self.in_cell = False

    def handle_starttag(self, tag, attrs):
        if tag in ('th', 'td'):
            self.in_cell = True

    def handle_endtag(self, tag):
        if tag in ('th', 'td'):
            self.in_cell = False

    def handle_data(self, data):
        if self.in_cell:
            self.cells.append(data)


class SampleHtmlTests(unittest.TestCase):
    def test_report_is_parseable_and_contains_expected_results(self):
        html = render_html({'README': False, 'Git ignore': True, 'License': False}, 'a<&"b')
        parser = ReportParser()
        parser.feed(html)
        self.assertEqual(parser.cells[-6:], ['README', 'MISSING', 'Git ignore', 'OK', 'License', 'MISSING'])
        self.assertIn('a&lt;&amp;&quot;b', html)
        self.assertIn('Overall status: <strong>Needs attention</strong>', html)
        self.assertIn('body{font:', html)
        self.assertNotIn('body{{font:', html)

    def test_generator_creates_expected_standalone_report(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch('generate_sample_html.Path', wraps=Path) as path_mock:
                path_mock.return_value = Path(directory) / 'examples' / 'sample-report.html'
                generate_sample_html.main()
            report = (Path(directory) / 'examples' / 'sample-report.html').read_text(encoding='utf-8')
            expected = render_html({'README': False, 'Git ignore': False, 'License': False}, 'example-empty-repository')
            self.assertEqual(report, expected + '\n')


if __name__ == '__main__':
    unittest.main()
