"""Fail a security audit if scanner output silently omitted the expected config."""
import json
from pathlib import Path
import sys

for filename in sys.argv[1:]:
    report = json.loads(Path(filename).read_text(encoding='utf-8'))
    results = [r for r in report.get('Results', []) if r.get('Class') == 'config']
    if not results:
        raise SystemExit(f'No configuration coverage in {filename}; inspect scanner errors')
    findings = sum(len(r.get('Misconfigurations', [])) for r in results)
    print(f'{Path(filename).name}: {len(results)} configuration result(s), {findings} HIGH/CRITICAL finding(s). Report-only audit.')
