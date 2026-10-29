import copy
from pathlib import Path
import shutil
import subprocess
import unittest
import yaml
from test_local_tools import ROOT, load


class ManifestPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which('helm'):
            raise unittest.SkipTest('helm required for rendered-manifest policy tests')
        output = subprocess.check_output(['helm', 'template', 'demo', str(ROOT / 'helm/paperless'), '--namespace', 'paperless'], text=True)
        cls.documents = list(yaml.safe_load_all(output))
        cls.policy = load('check_manifests')

    def test_valid_chart(self):
        self.assertEqual(self.policy.check(self.documents), [])

    def test_public_service_rejected(self):
        docs = copy.deepcopy(self.documents)
        next(d for d in docs if d['kind'] == 'Service')['spec']['type'] = 'LoadBalancer'
        self.assertTrue(any('public service' in e for e in self.policy.check(docs)))

    def test_multiple_writers_rejected(self):
        docs = copy.deepcopy(self.documents)
        next(d for d in docs if d['kind'] == 'Deployment')['spec']['replicas'] = 2
        self.assertTrue(any('single writer' in e for e in self.policy.check(docs)))

    def test_selector_typo_rejected(self):
        docs = copy.deepcopy(self.documents)
        next(d for d in docs if d['kind'] == 'Service')['spec']['selector']['typo'] = 'bad'
        self.assertTrue(any('selector' in e for e in self.policy.check(docs)))

    def test_plaintext_secret_rejected(self):
        docs = copy.deepcopy(self.documents)
        deployment = next(d for d in docs if d['kind'] == 'Deployment')
        deployment['spec']['template']['spec']['containers'][0]['env'].append({'name': 'PAPERLESS_SECRET_KEY', 'value': 'invalid-fixture'})
        self.assertTrue(any('secretKeyRef' in e for e in self.policy.check(docs)))


if __name__ == '__main__':
    unittest.main()
