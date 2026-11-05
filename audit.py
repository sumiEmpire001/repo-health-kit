from pathlib import Path


def audit(path):
    root = Path(path)
    if not root.is_dir():
        raise ValueError('Repository directory not found')
    checks = {'README': (root / 'README.md').is_file(), 'Git ignore': (root / '.gitignore').is_file(), 'License': (root / 'LICENSE').is_file()}
    return checks


if __name__ == '__main__':
    for name, found in audit('.').items():
        print(f'{name}: {"OK" if found else "MISSING"}')
