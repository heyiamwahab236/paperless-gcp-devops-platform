"""Sequential registry-only image scans; bounded memory; aggregate failures."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
out = ROOT / 'build/security'
out.mkdir(parents=True, exist_ok=True)
tool = ROOT / 'build/tools' / ('trivy.exe' if os.name == 'nt' else 'trivy')
failed = False
for name, ref in json.loads((ROOT / 'images.lock.json').read_text())['images'].items():
    common = [str(tool), 'image', '--image-src', 'remote', '--parallel', '1', '--timeout', '15m', '--no-progress']
    scan = subprocess.run(common + ['--scanners', 'vuln', '--severity', 'HIGH,CRITICAL', '--exit-code', '1', '--format', 'json', '--output', str(out / f'{name}.json'), ref])
    sbom = subprocess.run(common + ['--format', 'cyclonedx', '--output', str(out / f'{name}.cdx.json'), ref])
    failed = failed or scan.returncode != 0 or sbom.returncode != 0
raise SystemExit(1 if failed else 0)
