"""Independent reference math frozen in verification/independent-cases.json first."""
import json
import unittest
from copy import deepcopy
from pathlib import Path

from app.adapter import SimulatedAdapter
from app.fixtures import example
from app.investigate import investigate
from app.schema import fingerprint, validate_case

REFERENCES = json.loads((Path(__file__).resolve().parents[1] /
                         'verification/independent-cases.json').read_text())['cases']


def build_case(reference):
    case = deepcopy(example())
    case['name'] = reference['id']
    case['records'] = [dict(id=f'independent-{index}', amount=row[0],
                            status=row[1], region=row[2])
                       for index, row in enumerate(reference['rows'])]
    case['reports'][0]['filters']['status'] = deepcopy(reference['a'])
    case['reports'][1]['filters']['status'] = deepcopy(reference['b'])
    if 'region_b' in reference:
        case['reports'][1]['filters']['region'] = deepcopy(reference['region_b'])
    for key in ('definition', 'unit'):
        if key + '_b' in reference:
            case['reports'][1][key] = reference[key + '_b']
    return validate_case(case)


class IndependentTests(unittest.TestCase):
    def check_reference(self, reference):
        case = build_case(reference)
        before = fingerprint(case)
        adapter = SimulatedAdapter(case)
        try:
            result = investigate(case, adapter, 'diagnose')
        finally:
            cleanup = adapter.cleanup()
        self.assertEqual(fingerprint(case), before)
        self.assertEqual(cleanup['created'], cleanup['released'])
        self.assertTrue(all(i['state'] == 'released' for i in cleanup['instances']))
        self.assertEqual(result['live_connection'], 'not tested')
        expected = reference['expected']
        if reference['id'] == 'equal-different-definitions':
            # Preserve and expose the initial reviewer scope error; this is not
            # a supported equal control. The supplementary control supplies it.
            self.assertEqual(result['status'], 'unresolved')
            self.assertEqual(result['originals'], [])
            self.assertIsNone(result['experiment'])
            self.assertTrue(any('outside the supported' in u for u in result['unknowns']))
            return
        self.assertEqual(result['status'], expected['status'])
        self.assertEqual([r['total'] for r in result['originals']],
                         [expected['a'], expected['b']])
        if reference['id'] == 'missing-unit':
            self.assertIsNone(result['delta'])
            self.assertIsNone(result['experiment'])
            self.assertTrue(any('unit' in u for u in result['unknowns']))
        else:
            self.assertEqual(result['delta'], expected['difference'])
        if expected['status'] == 'demonstrated':
            experiment = result['experiment']
            self.assertEqual(experiment['result']['total'], expected['variant'])
            self.assertEqual(experiment['impact'], expected['impact'])
            self.assertEqual(result['residual'], expected['residual'])
            self.assertEqual(experiment['before'], reference['b'])
            self.assertEqual(experiment['after'], reference['a'])
            self.assertEqual(experiment['result']['filters']['region'],
                             case['reports'][1]['filters']['region'])
            self.assertEqual(cleanup['created'], 3)
            self.assertEqual(result['differences'][0]['status'],
                             'numerical cause demonstrated on synthetic data')
            if 'percentage' in expected:
                self.assertEqual(result['percent_delta'], expected['percentage'])
        else:
            self.assertIsNone(result['experiment'])
            self.assertEqual(cleanup['created'], 2)
            if expected['status'] == 'equal':
                self.assertEqual(result['summary'],
                                 'No numerical difference in these captured results.')
                self.assertTrue(any('do not establish' in u for u in result['unknowns']))
            if reference['id'] == 'overlapping-selections':
                self.assertEqual({d['field'] for d in result['differences']}, {'status', 'region'})
                self.assertTrue(all(d['status'] == 'candidate' for d in result['differences']))
                self.assertIsNone(result['residual'])


def make_test(reference):
    def test(self):
        self.check_reference(reference)
    return test


for reference in REFERENCES:
    setattr(IndependentTests, 'test_' + reference['id'].replace('-', '_'), make_test(reference))


if __name__ == '__main__':
    unittest.main()
