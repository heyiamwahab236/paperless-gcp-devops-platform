"""Generate local file secrets without printing or replacing existing values."""
import os
from pathlib import Path
import secrets

ROOT = Path(__file__).resolve().parents[1]


def initialize(root=ROOT):
    secret_dir = root / '.secrets'
    secret_dir.mkdir(mode=0o700, exist_ok=True)
    for name in ('db-password', 'secret-key'):
        path = secret_dir / name
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            if len(path.read_text().strip()) < 32:
                raise ValueError(f'{name} exists but is too short; investigate without overwriting it')
            continue
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as stream:
            stream.write(secrets.token_hex(32))
    for directory in ('runtime/consume', 'runtime/export'):
        (root / directory).mkdir(parents=True, exist_ok=True)
    env = root / '.env'
    if not env.exists():
        uid = os.getuid() if hasattr(os, 'getuid') else 1000
        gid = os.getgid() if hasattr(os, 'getgid') else 1000
        env.write_text(f'PAPERLESS_PORT=8000\nPAPERLESS_UID={uid}\nPAPERLESS_GID={gid}\n', encoding='utf-8')


if __name__ == '__main__':
    initialize()
    print('Local credentials and folders are ready. Existing secrets were preserved.')
