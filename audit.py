import argparse
import json
from html import escape
from pathlib import Path


def audit(path):
    root = Path(path)
    if not root.is_dir():
        raise ValueError('Repository directory not found')
    filenames = {entry.name.casefold() for entry in root.iterdir() if entry.is_file()}
    checks = {
        'README': any(name in filenames for name in ('readme.md', 'readme.rst', 'readme.txt', 'readme')),
        'Git ignore': '.gitignore' in filenames,
        'License': any(name in filenames for name in ('license', 'license.md', 'license.txt', 'licence', 'licence.md', 'licence.txt')),
    }
    return checks


def render_html(checks, path):
    rows = '\n'.join(
        '<tr><th scope="row">{}</th><td>{}</td></tr>'.format(
            escape(name), 'OK' if found else 'MISSING'
        )
        for name, found in checks.items()
    )
    status = 'Healthy' if all(checks.values()) else 'Needs attention'
    return (
        '<!doctype html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>Repository health report</title>\n'
        '<style>body{font:16px system-ui,sans-serif;max-width:700px;margin:3rem auto;padding:0 1rem}'
        'table{border-collapse:collapse;width:100%}th,td{padding:.8rem;text-align:left;border-bottom:1px solid #ddd}'
        'th{width:60%}</style>\n</head>\n<body>\n'
        '<h1>Repository health report</h1>\n'
        '<p>Directory: <code>{}</code></p>\n'
        '<p>Overall status: <strong>{}</strong></p>\n'
        '<table><thead><tr><th>Check</th><th>Status</th></tr></thead>'
        '<tbody>{}</tbody></table>\n</body>\n</html>'
    ).format(escape(str(path)), status, rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Check repository hygiene files.')
    parser.add_argument('path', nargs='?', default='.', help='Repository directory (default: current directory)')
    output = parser.add_mutually_exclusive_group()
    output.add_argument('--json', action='store_true', help='Print machine-readable JSON instead of text')
    output.add_argument('--html', action='store_true', help='Print a standalone HTML report')
    parser.add_argument('--strict', action='store_true', help='Exit with status 1 when required files are missing')
    args = parser.parse_args(argv)
    try:
        checks = audit(args.path)
    except ValueError as exc:
        parser.error(str(exc))
    if args.html:
        print(render_html(checks, args.path))
    elif args.json:
        print(json.dumps({'checks': checks, 'healthy': all(checks.values())}, indent=2))
    else:
        for name, found in checks.items():
            print(f'{name}: {"OK" if found else "MISSING"}')
    return 1 if args.strict and not all(checks.values()) else 0


if __name__ == '__main__':
    raise SystemExit(main())
