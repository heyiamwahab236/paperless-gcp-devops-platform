"""Copy local file secrets to a named Kubernetes context; never print their values."""
import argparse
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--context', default='paperless-lab')
    parser.add_argument('--namespace', default='paperless')
    args = parser.parse_args()
    for name in ('db-password', 'secret-key'):
        if not (ROOT / '.secrets' / name).is_file():
            raise SystemExit('Run scripts/init_local.py first.')
    base = ['kubectl', '--context', args.context, '-n', args.namespace]
    for command in (
        ['create', 'namespace', args.namespace, '--dry-run=client', '-o', 'json'],
        ['create', 'secret', 'generic', 'paperless-secrets',
         f'--from-file=db-password={ROOT / ".secrets/db-password"}',
         f'--from-file=secret-key={ROOT / ".secrets/secret-key"}',
         '--dry-run=client', '-o', 'json'],
    ):
        result = subprocess.run(base + command, check=True, capture_output=True)
        subprocess.run(base + ['apply', '-f', '-'], input=result.stdout, check=True)


if __name__ == '__main__':
    main()
