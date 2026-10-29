import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LocalToolsTests(unittest.TestCase):
    def test_secrets_are_unique_and_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            init = load('init_local')
            init.initialize(root)
            db = (root / '.secrets/db-password').read_text()
            key = (root / '.secrets/secret-key').read_text()
            self.assertNotEqual(db, key)
            self.assertGreaterEqual(len(db.strip()), 64)
            init.initialize(root)
            self.assertEqual(db, (root / '.secrets/db-password').read_text())

    def test_bad_existing_secret_is_not_replaced(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / '.secrets').mkdir()
            path = root / '.secrets/db-password'
            path.write_text('invalid')
            with self.assertRaises(ValueError):
                load('init_local').initialize(root)
            self.assertEqual(path.read_text(), 'invalid')

    def test_pdf_cross_reference_offsets(self):
        pdf = load('smoke').make_pdf('portfolio-test')
        start = int(pdf.split(b'startxref\n')[1].splitlines()[0])
        self.assertEqual(pdf[start:start+4], b'xref')
        lines = pdf[start:].splitlines()
        for index, entry in enumerate(lines[3:8], 1):
            offset = int(entry.split()[0])
            self.assertTrue(pdf[offset:].startswith(f'{index} 0 obj'.encode()))

    def test_locked_images_match_both_runtimes(self):
        lock = json.loads((ROOT / 'images.lock.json').read_text())
        for ref in lock['images'].values():
            self.assertIn(ref, (ROOT / 'compose.yaml').read_text())
            self.assertIn(ref, (ROOT / 'helm/paperless/values.yaml').read_text())
            self.assertRegex(ref, r'@sha256:[a-f0-9]{64}$')


if __name__ == '__main__':
    unittest.main()
