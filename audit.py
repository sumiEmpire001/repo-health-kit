import argparse
import json
from pathlib import Path


def audit(path):
    root = Path(path)
    if not root.is_dir():
        raise ValueError('Repository directory not found')
    checks = {'README': (root / 'README.md').is_file(), 'Git ignore': (root / '.gitignore').is_file(), 'License': (root / 'LICENSE').is_file()}
    return checks


def main(argv=None):
    parser = argparse.ArgumentParser(description='Check repository hygiene files.')
    parser.add_argument('path', nargs='?', default='.', help='Repository directory (default: current directory)')
    parser.add_argument('--json', action='store_true', help='Print machine-readable JSON instead of text')
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
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
