"""Generate a deterministic, standalone HTML example for GitHub Actions."""
from pathlib import Path

from audit import render_html


def main():
    checks = {'README': False, 'Git ignore': False, 'License': False}
    output = Path('examples/sample-report.html')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_html(checks, 'example-empty-repository') + '\n', encoding='utf-8')
    print(f'Wrote {output}')


if __name__ == '__main__':
    main()
