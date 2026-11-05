import argparse
import json
from pathlib import Path


def audit(path):
    root = Path(path)
    if not root.is_dir():
        raise ValueError('Repository directory not found')
    checks = {
        'README': any((root / name).is_file() for name in ('README.md', 'README.rst', 'README.txt', 'README')),
        'Git ignore': (root / '.gitignore').is_file(),
        'License': any((root / name).is_file() for name in ('LICENSE', 'LICENSE.md', 'LICENSE.txt', 'LICENCE', 'LICENCE.md', 'LICENCE.txt')),
    }
    return checks


def main(argv=None):
    parser = argparse.ArgumentParser(description='Check repository hygiene files.')
    parser.add_argument('path', nargs='?', default='.', help='Repository directory (default: current directory)')
    parser.add_argument('--json', action='store_true', help='Print machine-readable JSON instead of text')
    parser.add_argument('--strict', action='store_true', help='Exit with status 1 when required files are missing')
    args = parser.parse_args(argv)
    try:
        checks = audit(args.path)
    except ValueError as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps({'checks': checks, 'healthy': all(checks.values())}, indent=2))
    else:
        for name, found in checks.items():
            print(f'{name}: {"OK" if found else "MISSING"}')
    return 1 if args.strict and not all(checks.values()) else 0


if __name__ == '__main__':
    raise SystemExit(main())
