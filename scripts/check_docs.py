"""Check local Markdown file targets and UTF-8 text hygiene without a network."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
errors = []
count = 0
for path in ROOT.rglob('*.md'):
    if any(part in ('.terraform', '.venv', 'build') for part in path.parts):
        continue
    text = path.read_text(encoding='utf-8')
    count += 1
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
        if target.startswith(('http:', 'https:', 'mailto:', '#')):
            continue
        local = target.split('#')[0]
        if not (path.parent / local).exists():
            errors.append(f'{path.relative_to(ROOT)}: missing target {target}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: local links in {count} Markdown files')
