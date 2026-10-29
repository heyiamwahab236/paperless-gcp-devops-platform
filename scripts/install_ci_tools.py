"""Download named validation tools from official releases and verify checksums.

Writes only under build/tools. No administrator installation or shell installer.
Checksums detect corruption; HTTPS GitHub release ownership remains a trust root.
"""
import argparse
import hashlib
import io
from pathlib import Path
import platform
import tarfile
import urllib.request
import zipfile

TOOLS = {
    'actionlint': ('rhysd/actionlint', '1.7.7', 'actionlint_{v}_{os}_amd64.{ext}', 'actionlint_{v}_checksums.txt'),
    'kubeconform': ('yannh/kubeconform', '0.7.0', 'kubeconform-{os}-amd64.{ext}', 'CHECKSUMS'),
    'trivy': ('aquasecurity/trivy', '0.76.1', 'trivy_{v}_{os}-64bit.{ext}', 'trivy_{v}_checksums.txt'),
}


def download(url):
    with urllib.request.urlopen(url, timeout=120) as response:
        return response.read()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tools', nargs='+', choices=TOOLS)
    args = parser.parse_args()
    if platform.machine().lower() not in ('x86_64', 'amd64'):
        raise SystemExit('This helper supports x86_64 only. Install native tools manually on ARM.')
    os_name = platform.system().lower()
    if os_name not in ('linux', 'windows'):
        raise SystemExit('Use Linux/WSL2, Windows, or install tools manually.')
    output = Path('build/tools')
    output.mkdir(parents=True, exist_ok=True)
    ext = 'zip' if os_name == 'windows' else 'tar.gz'
    for name in args.tools:
        repo, version, pattern, checksum_pattern = TOOLS[name]
        # Trivy release uses Linux (capital L) but windows (lowercase).
        release_os = 'Linux' if name == 'trivy' and os_name == 'linux' else os_name
        filename = pattern.format(v=version, os=release_os, ext=ext)
        base = f'https://github.com/{repo}/releases/download/v{version}/'
        checksum_file = download(base + checksum_pattern.format(v=version)).decode()
        raw = download(base + filename)
        digest = hashlib.sha256(raw).hexdigest()
        if not any(line.split()[0] == digest and line.split()[-1].lstrip('*') == filename for line in checksum_file.splitlines() if line.strip()):
            raise RuntimeError(f'Checksum mismatch for {name}')
        executable = name + ('.exe' if os_name == 'windows' else '')
        if ext == 'zip':
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                binary = archive.read(executable)
        else:
            with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as archive:
                binary = archive.extractfile(executable).read()
        path = output / executable
        path.write_bytes(binary)
        path.chmod(0o755)
        print(f'{name} {version}: checksum verified')


if __name__ == '__main__':
    main()
