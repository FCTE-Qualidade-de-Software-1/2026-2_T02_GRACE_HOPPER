import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from run import consolidate, verify_manifest

class ReportTests(unittest.TestCase):
    def result(self, xml, ids=('A01', 'A02'), code=0):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'junit.xml'
            if xml is not None:
                p.write_text('<testsuite>' + xml + '</testsuite>')
            return consolidate({'cases': [{'id': x} for x in ids]}, p, code)

    def test_all_pass(self):
        self.assertEqual('APROVADO', self.result('<testcase name="M3 A01"/><testcase name="M3 A02"/>')['gate'])

    def test_failure_skip_and_error_remain_in_denominator(self):
        for tag in ('failure', 'skipped', 'error'):
            result = self.result(f'<testcase name="M3 A01"/><testcase name="M3 A02"><{tag}/></testcase>')
            self.assertEqual((2, 1, 'BLOQUEADO'), (result['planned'], result['conforming'], result['gate']))

    def test_missing_report_and_missing_id(self):
        self.assertEqual(0, self.result(None)['conforming'])
        self.assertEqual('missing', self.result('<testcase name="M3 A01"/>')['cases'][1]['status'])

    def test_duplicate_and_unknown(self):
        self.assertEqual('duplicate', self.result('<testcase name="M3 A01"/><testcase name="M3 A01"/>')['cases'][0]['status'])
        self.assertTrue(self.result('<testcase name="M3 X99"/>')['anomalies'])

    def test_empty_and_process_error(self):
        self.assertIsNone(self.result('', ids=())['percent'])
        self.assertEqual('BLOQUEADO', self.result('', ids=())['gate'])
        self.assertEqual('BLOQUEADO', self.result('<testcase name="M3 A01"/><testcase name="M3 A02"/>', code=2)['gate'])

    def test_manifest_reference_matches(self):
        self.assertEqual(64, len(verify_manifest()))

    def test_changed_manifest_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'manifest.json').write_text('{"cases": []}')
            (root / 'manifest.sha256').write_text('0' * 64 + '  manifest.json\n')
            with patch('run.HERE', root):
                with self.assertRaisesRegex(RuntimeError, 'Manifest differs'):
                    verify_manifest()

if __name__ == '__main__':
    unittest.main()
