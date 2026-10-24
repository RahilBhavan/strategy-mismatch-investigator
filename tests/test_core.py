import json
import tempfile
import threading
import time
import unittest
from copy import deepcopy
from pathlib import Path
from app.adapter import AdapterFailure, SimulatedAdapter
from app.fixtures import example, examples
from app.investigate import investigate
from app.schema import CaseError, MAX_ROWS, fingerprint, validate_case
from app.store import Store


def run(case, phase='diagnose', mode='normal'):
    case = validate_case(case)
    adapter = SimulatedAdapter(case, mode=mode)
    try:
        result = investigate(case, adapter, phase)
    finally:
        cleanup = adapter.cleanup()
    return result, cleanup


class CoreTests(unittest.TestCase):
    def test_record_backed_experiment_and_no_mutation(self):
        case = example(); before = fingerprint(case)
        result, cleanup = run(case)
        self.assertEqual([r['total'] for r in result['originals']], ['220.00', '180.00'])
        self.assertEqual(result['delta'], '-40.00')
        self.assertEqual(result['experiment']['impact'], '40.00')
        self.assertEqual(result['residual'], '0.00')
        self.assertEqual(result['status'], 'demonstrated')
        self.assertEqual(fingerprint(case), before)
        self.assertEqual(cleanup['created'], 3)
        self.assertEqual(cleanup['released'], 3)
        case['records'][1]['amount'] = '17.35'
        changed, _ = run(case)
        self.assertEqual(changed['originals'][0]['total'], '197.35')
        self.assertEqual(changed['experiment']['impact'], '17.35')

    def test_comparison_is_candidate_not_proof(self):
        r, c = run(example(), 'compare')
        self.assertEqual(r['status'], 'candidate')
        self.assertIsNone(r['experiment'])
        self.assertEqual(c['created'], 2)

    def test_context_controls(self):
        for name in ('snapshots', 'missing', 'ambiguous', 'null'):
            with self.subTest(name=name):
                r, _ = run(examples()[name])
                self.assertEqual(r['status'], 'unresolved')
                self.assertIsNone(r['experiment'])
        r, _ = run(examples()['equal'])
        self.assertEqual(r['status'], 'equal')
        case = examples()['equal'];case['reports'][1]['metric'] = 'different-definition'
        r, _ = run(case)
        self.assertEqual(r['status'], 'unresolved')

    def test_zero_negative_and_exact_large(self):
        case = example()
        case['records'] = [dict(id='a', amount='-4.00', status='paid', region='East'),
                           dict(id='b', amount='4.00', status='refunded', region='East')]
        r, _ = run(case)
        self.assertEqual(r['originals'][0]['total'], '0.00')
        self.assertIsNone(r['percent_delta'])
        self.assertEqual(r['experiment']['impact'], '4.00')
        case['records'] = [dict(id='a',amount='90071992547409.93',status='paid',region='East'),
                           dict(id='b',amount='0.01',status='refunded',region='East')]
        r, _ = run(case)
        self.assertEqual(r['originals'][0]['total'], '90071992547409.94')
        self.assertEqual(r['delta'], '-0.01')

    def test_overflow_and_completeness(self):
        case = example()
        case['records'][0]['amount']='92233720368547758.07'
        with self.assertRaises(AdapterFailure):run(case)
        r, _ = run(example(), mode='incomplete')
        self.assertEqual(r['status'], 'unresolved')
        self.assertIsNone(r['delta'])

    def test_boundary(self):
        changes = [lambda c:c['reports'][1].update(project='another'),
                   lambda c:c['reports'][0].update(type='dashboard'),
                   lambda c:c['records'][0].update(amount='NaN'),
                   lambda c:c['records'][0].update(amount='0.001'),
                   lambda c:c['records'][0].update(amount=4),
                   lambda c:c.update(synthetic=False),
                   lambda c:c.update(auth_token='never-accepted')]
        for change in changes:
            case=example();change(case)
            with self.assertRaises(CaseError):validate_case(case)
        case=example();case['records']=[case['records'][0]]*(MAX_ROWS+1)
        with self.assertRaises(CaseError):validate_case(case)
        case=example();case['name']='x'*500
        for report in case['reports']:report['name']='r'*500
        validate_case(case)
        case['records']=[dict(id=str(i),amount='1.00',status='s'*500,region='r'*500) for i in range(21000)]
        with self.assertRaisesRegex(CaseError,'20 MB'):validate_case(case)

    def test_faults_and_retry_limit(self):
        for mode in ('denied','expired','error','timeout'):
            adapter=SimulatedAdapter(example(),mode=mode)
            with self.assertRaises(AdapterFailure):
                investigate(example(),adapter)
            cleanup=adapter.cleanup()
            self.assertEqual(cleanup['released'],cleanup['created'])
            self.assertEqual(len([e for e in cleanup['events'] if e['event']=='retry']),0)
        for mode in ('transient','rate_limit'):
            r, c = run(example(),mode=mode)
            self.assertEqual(r['status'],'demonstrated')
            self.assertEqual(len([e for e in c['events'] if e['event']=='retry']),1)

    def test_execution_deadline(self):
        adapter=SimulatedAdapter(example(),mode='slow',timeout=.01)
        with self.assertRaisesRegex(AdapterFailure,'5 seconds'):
            adapter.execute(example()['reports'][0])
        self.assertEqual(adapter.cleanup()['released'],1)


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=Path(self.temp.name)/'test.sqlite3';self.store=Store(self.path)
    def tearDown(self):self.temp.cleanup()
    def wait(self,job):
        for _ in range(200):
            job=self.store.job(job['id'])
            if job['state'] not in ('running','queued'):return job
            time.sleep(.02)
        self.fail('job did not finish')
    def submit(self,phase='diagnose',mode='normal'):
        source=self.store.case('status')
        return self.store.submit('status',source['fingerprint'],phase,mode)
    def test_retry_idempotent_and_restart(self):
        job=self.wait(self.submit())
        self.assertEqual(job['state'],'complete')
        same=self.submit();self.assertEqual(job['id'],same['id'])
        restarted=Store(self.path)
        self.assertEqual(restarted.job(job['id'])['result'],job['result'])
        packet=restarted.export(job['id'])
        restored=restarted.restore(packet)
        self.assertEqual(restored['result']['status'],'demonstrated')
        self.assertEqual(restored['result']['originals'][0]['total'],'220.00')
    def test_canceled_cannot_publish_and_cleanup_is_local(self):
        job=self.submit(mode='slow')
        self.store.cancel(job['id']);finished=self.wait(job)
        self.assertEqual(finished['state'],'canceled')
        self.assertIsNone(finished['result'])
        self.assertEqual(finished['cleanup']['released'],finished['cleanup']['created'])
        self.assertEqual(self.wait(self.submit())['state'],'complete')
    def test_change_invalidates_and_old_export_is_versioned(self):
        source=self.store.case('status');job=self.wait(self.submit())
        changed=source['case'];changed['records'][1]['amount']='5.00'
        self.store.save_case(changed,'status')
        self.assertTrue(self.store.job(job['id'])['stale'])
        with self.assertRaises(CaseError):self.store.submit('status',source['fingerprint'],'compare','normal')
        packet=self.store.export(job['id'])
        self.assertEqual(packet['payload']['case']['records'][1]['amount'],'40.00')
        self.assertTrue(packet['payload']['source_stale'])
    def test_tampered_packet_and_recomputed_fraud_rejected(self):
        job=self.wait(self.submit());packet=self.store.export(job['id'])
        packet['payload']['result']['originals'][0]['total']='999'
        with self.assertRaises(CaseError):self.store.restore(packet)
        packet['sha256']=fingerprint(packet['payload'])
        with self.assertRaisesRegex(CaseError,'recomputation'):self.store.restore(packet)
    def test_failed_attempt_has_no_result_and_can_retry(self):
        job=self.wait(self.submit(mode='denied'))
        self.assertEqual(job['state'],'failed');self.assertIsNone(job['result'])
        retry=self.submit(mode='denied');self.assertNotEqual(job['id'],retry['id'])
        self.wait(retry)
    def test_incomplete_export_reopens_as_unresolved(self):
        job=self.wait(self.submit(mode='incomplete'))
        restored=self.store.restore(self.store.export(job['id']))
        self.assertEqual(restored['result']['status'],'unresolved')
    def test_software_revision_invalidates_old_conclusions(self):
        job=self.wait(self.submit())
        result=job['result'];result['software_version']='old'
        with self.store.db() as db:
            db.execute('UPDATE jobs SET result=? WHERE id=?',(json.dumps(result),job['id']))
        self.assertTrue(self.store.job(job['id'])['stale'])
        fresh=self.wait(self.submit())
        self.assertNotEqual(fresh['id'],job['id'])
        self.assertFalse(fresh['stale'])

    def test_restart_marks_unfinished_interrupted(self):
        with self.store.db() as db:
            source=self.store.case('status')
            db.execute('INSERT INTO jobs(id,case_id,case_fp,snapshot,phase,mode,state,created) VALUES(?,?,?,?,?,?,?,?)',
                       ('interrupted','status',source['fingerprint'],json.dumps(source['case']),'compare','normal','running',time.time()))
        restarted=Store(self.path)
        self.assertEqual(restarted.job('interrupted')['state'],'interrupted')


if __name__=='__main__':unittest.main()
