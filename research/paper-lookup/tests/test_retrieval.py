"""Local regressions for observed failures and recovery. No network required."""
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
import urllib.error
from unittest.mock import patch

sys.dont_write_bytecode = True
SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / 'scripts'))
import paginate
from _common import Reconciliation
from _pagination_state import Progress


def rows(start, end):
    return [{'id': str(i)} for i in range(start, end)]


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name) / 'results.json'
        self.api = paginate.Api('test', .01, lambda q,s,n: f'https://example.invalid/{s}', lambda p,s: p)
        self.registry = patch.dict(paginate.APIS, {'test': self.api})
        self.registry.start(); self.addCleanup(self.registry.stop)

    def run_cli(self, responses, *args):
        with patch.object(paginate, 'fetch', side_effect=responses) as fetch, \
             patch.object(paginate.time, 'sleep') as sleep, \
             contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            try:
                code = paginate.main(list(args))
            except SystemExit as e:
                code = e.code
        return code, fetch.call_count, sleep

    def start(self, responses, *args):
        return self.run_cli(responses, '--api','test','--query','q','--output',str(self.out),*args)

    def data(self):
        return json.loads(self.out.read_text())

    def test_last_page_cap_is_partial_not_missing(self):
        code, _, _ = self.start([paginate.Page(rows(0,30),60,30),paginate.Page(rows(30,60),60,None)], '--max-records','35')
        self.assertEqual(code, 0)
        d = self.data()
        self.assertEqual(len(d['records']),35)
        self.assertTrue(d['reconciliation']['stopped_at_limit'])
        self.assertFalse(d['reconciliation']['complete'])
        self.assertEqual(len(d['checkpoint']['buffered_records']),25)

    def test_resume_drains_last_page_buffer_without_network(self):
        self.start([paginate.Page(rows(0,30),60,30),paginate.Page(rows(30,60),60,None)], '--max-records','35')
        code, calls, _ = self.run_cli([], '--resume',str(self.out),'--max-records','100')
        self.assertEqual((code,calls),(0,0))
        d=self.data()
        self.assertEqual(d['records'], rows(0,60))
        self.assertTrue(d['reconciliation']['complete'])

    def test_resume_keeps_provider_notes_and_prior_limit_event(self):
        self.start([paginate.Page(rows(0,2),2,None,notes=['counts include all versions'])], '--max-records','1')
        code,calls,_=self.run_cli([], '--resume',str(self.out),'--max-records','2')
        self.assertEqual((code,calls),(0,0))
        self.assertEqual(self.data()['reconciliation']['notes'],['counts include all versions'])
        self.assertTrue(any(e['type']=='limit' for e in self.data()['events']))

    def test_failure_saves_first_page_and_retries_same_cursor_on_resume(self):
        code, _, _ = self.start([paginate.Page(rows(0,2),4,2),RuntimeError('failed page 2')])
        self.assertEqual(code,1)
        d=self.data()
        self.assertEqual(d['records'],rows(0,2))
        self.assertEqual(d['checkpoint']['next_state'],2)
        self.assertEqual(d['status'],'failed')
        self.assertFalse(d['reconciliation']['complete'])
        code,calls,_=self.run_cli([paginate.Page(rows(2,4),4,None)],'--resume',str(self.out))
        self.assertEqual((code,calls),(0,1))
        self.assertEqual(self.data()['records'],rows(0,4))
        self.assertTrue(self.data()['reconciliation']['complete'])

    def test_progress_is_on_disk_before_next_page_request(self):
        def second(url):
            self.assertEqual(self.data()['records'],rows(0,1))
            return paginate.Page(rows(1,2),2,None)
        calls=[]
        def fetch(url):
            calls.append(url)
            return paginate.Page(rows(0,1),2,1) if len(calls)==1 else second(url)
        code,_,_=self.start(fetch)
        self.assertEqual(code,0)

    def test_duplicate_page_never_counts_as_complete(self):
        code,_,_=self.start([paginate.Page(rows(0,1),2,1),paginate.Page(rows(0,1),2,None)])
        self.assertNotEqual(code,0)
        self.assertEqual(self.data()['records'],rows(0,1))
        self.assertFalse(self.data()['reconciliation']['complete'])
        self.assertIn('duplicate',self.data()['reconciliation']['error'])

    def test_duplicate_inside_page_is_rejected(self):
        code,_,_=self.start([paginate.Page(rows(0,1)*2,2,None)])
        self.assertNotEqual(code,0)
        self.assertEqual(self.data()['records'],[])

    def test_missing_identity_does_not_look_complete(self):
        code,_,_=self.start([paginate.Page([{'title':'paper'}],1,None)])
        self.assertNotEqual(code,0)
        self.assertFalse(self.data()['reconciliation']['complete'])

    def test_total_changes_are_reported(self):
        code,_,_=self.start([paginate.Page(rows(0,1),2,1),paginate.Page(rows(1,2),3,None)])
        self.assertNotEqual(code,0)
        self.assertIn('total changed',self.data()['reconciliation']['error'])

    def test_premature_empty_page_keeps_cursor_for_retry(self):
        code,_,_=self.start([paginate.Page(rows(0,2),3,2),paginate.Page([],3,None)])
        self.assertEqual(code,4)
        self.assertEqual(self.data()['checkpoint']['next_state'],2)
        self.assertEqual(self.data()['records'],rows(0,2))
        code,calls,_=self.run_cli([paginate.Page(rows(2,3),3,None)],'--resume',str(self.out))
        self.assertEqual((code,calls),(0,1))
        self.assertEqual(self.data()['records'],rows(0,3))

    def test_incomplete_http_200_is_retried_at_the_saved_cursor(self):
        p=Progress('europepmc','q','second',records=[{'id':'1','source':'MED'}])
        p.reconciliation.expected=2
        p.save(self.out)
        responses=[paginate.Fetched({'version':'6.9'}),paginate.Fetched({
            'hitCount':2,'resultList':{'result':[{'id':'2','source':'MED'}]}})]
        code,calls,_=self.run_cli(responses,'--resume',str(self.out))
        self.assertEqual((code,calls),(0,2))
        self.assertEqual(self.data()['status'],'complete')
        self.assertEqual(self.data()['provenance']['urls'][0],self.data()['provenance']['urls'][1])
        self.assertEqual([r['id'] for r in self.data()['records']],['1','2'])

    def test_persistent_incomplete_http_200_fails_with_progress_intact(self):
        p=Progress('europepmc','q','second',records=[{'id':'1','source':'MED'}])
        p.reconciliation.expected=2
        p.save(self.out)
        code,calls,_=self.run_cli([paginate.Fetched({'version':'6.9'})]*3,'--resume',str(self.out))
        self.assertEqual((code,calls),(1,3))
        self.assertEqual(self.data()['status'],'failed')
        self.assertEqual(self.data()['checkpoint']['next_state'],'second')
        self.assertEqual([r['id'] for r in self.data()['records']],['1'])

    def test_total_unknown_is_null_not_true(self):
        self.start([paginate.Page(rows(0,1),None,None)])
        self.assertIsNone(self.data()['reconciliation']['complete'])
        self.assertEqual(self.data()['status'],'unverified')

    def test_empty_success_is_complete_zero(self):
        code,_,_=self.start([paginate.Page([],0,None)])
        self.assertEqual(code,0)
        self.assertEqual(self.data()['status'],'zero_hits')
        self.assertTrue(self.data()['reconciliation']['complete'])

    def test_changed_query_resume_rejected_without_overwrite(self):
        self.start([paginate.Page(rows(0,1),2,1)],'--max-calls','1')
        before=self.out.read_bytes()
        code,calls,_=self.run_cli([], '--resume',str(self.out),'--query','different')
        self.assertEqual((code,calls),(2,0))
        self.assertEqual(self.out.read_bytes(),before)

    def test_smaller_resume_cap_rejected_without_data_loss(self):
        self.start([paginate.Page(rows(0,2),2,None)])
        before=self.out.read_bytes()
        code,calls,_=self.run_cli([], '--resume',str(self.out),'--max-records','1')
        self.assertEqual((code,calls),(2,0))
        self.assertEqual(self.out.read_bytes(),before)

    def test_retries_are_counted_against_call_budget(self):
        error=paginate.FetchError('HTTP 429',retryable=True,retry_after=2)
        code,calls,_=self.start([error]*3,'--max-calls','2','--max-retries','3')
        self.assertEqual(calls,2)
        self.assertTrue(self.data()['reconciliation']['stopped_at_limit'])
        self.assertFalse(self.data()['reconciliation']['complete'])

    def test_retry_after_is_respected(self):
        error=paginate.FetchError('HTTP 429',retryable=True,retry_after=7)
        code,calls,sleep=self.start([error,paginate.Page(rows(0,1),1,None)])
        self.assertEqual((code,calls),(0,2))
        self.assertTrue(any(c.args[0]>=7 for c in sleep.call_args_list))
        self.assertEqual(self.data()['provenance']['requests_made'],2)

    def test_long_retry_after_stops_and_saves_instead_of_retrying_early(self):
        error=paginate.FetchError('HTTP 429',retryable=True,retry_after=3600)
        code,calls,_=self.start([error])
        self.assertEqual((code,calls),(1,1))
        self.assertEqual(self.data()['status'],'failed')

    def test_retry_exhaustion_preserves_valid_records(self):
        error=paginate.FetchError('HTTP 503',retryable=True,retry_after=1)
        code,calls,_=self.start([paginate.Page(rows(0,1),2,1),error,error,error])
        self.assertEqual((code,calls),(1,4))
        self.assertEqual(self.data()['records'],rows(0,1))

    def test_interrupt_preserves_checkpoint(self):
        code,_,_=self.start([paginate.Page(rows(0,1),2,1),KeyboardInterrupt()])
        self.assertEqual(code,130)
        self.assertEqual(self.data()['records'],rows(0,1))
        self.assertEqual(self.data()['status'],'interrupted')

    def test_full_result_at_exact_cap_is_complete(self):
        self.start([paginate.Page(rows(0,2),2,None)],'--max-records','2')
        self.assertTrue(self.data()['reconciliation']['complete'])

    def test_no_output_flag_still_saves_progress(self):
        previous=os.getcwd()
        try:
            os.chdir(self.temp.name)
            code,_,_=self.run_cli([paginate.Page(rows(0,1),1,None)],'--api','test','--query','q')
        finally:
            os.chdir(previous)
        self.assertEqual(code,0)
        self.assertEqual(len(list(Path(self.temp.name).glob('paper-lookup-test-*.json'))),1)

    def test_existing_output_requires_resume(self):
        self.out.write_text('prior output')
        code,calls,_=self.start([])
        self.assertEqual((code,calls),(2,0))
        self.assertEqual(self.out.read_text(),'prior output')

    def test_atomic_write_failure_keeps_last_checkpoint(self):
        progress=Progress('test','q',0)
        progress.save(self.out)
        before=self.out.read_bytes()
        with patch('_pagination_state.os.replace',side_effect=OSError('disk failure')):
            with self.assertRaises(OSError):
                progress.save(self.out)
        self.assertEqual(self.out.read_bytes(),before)
        self.assertEqual(list(self.out.parent.iterdir()),[self.out])

    def test_header_pacing_survives_resume(self):
        p=Progress('test','q',0,delay=2.5)
        p.save(self.out)
        restored=Progress.load(self.out)
        self.assertEqual(restored.delay,2.5)

    def test_crossref_expired_cursor_fails_without_network(self):
        p=Progress('crossref','query.bibliographic=q','opaque',last_page_at=time.time()-301)
        p.save(self.out)
        code,calls,_=self.run_cli([], '--resume',str(self.out))
        self.assertEqual((code,calls),(1,0))
        self.assertIn('expired',self.data()['reconciliation']['error'])

    def test_saved_cooldown_prevents_an_early_resume(self):
        p=Progress('test','q',0,retry_not_before=time.time()+600)
        p.save(self.out)
        code,calls,_=self.run_cli([], '--resume',str(self.out))
        self.assertEqual((code,calls),(1,0))
        self.assertIn('cooldown',self.data()['reconciliation']['error'])

    def test_malformed_checkpoint_is_rejected_before_writing(self):
        self.start([paginate.Page(rows(0,1),2,1)],'--max-calls','1')
        d=self.data();d['reconciliation']['retrieved_total']=99
        self.out.write_text(json.dumps(d))
        before=self.out.read_bytes()
        code,calls,_=self.run_cli([], '--resume',str(self.out))
        self.assertEqual((code,calls),(2,0))
        self.assertEqual(self.out.read_bytes(),before)


class ProviderAndTransportTests(unittest.TestCase):
    def test_error_and_malformed_success_bodies_are_rejected(self):
        for api in paginate.APIS.values():
            for p in ({},{'error':'backend problem'},{'message':{'items':'not a list'}}):
                with self.subTest(api=api.name,p=p), self.assertRaises(RuntimeError):
                    api.parse(p,api.initial_state)

    def test_rxiv_unknown_status_is_not_zero_hits(self):
        with self.assertRaises(RuntimeError):
            paginate._rxiv_parse({'messages':[{'status':'backend unavailable'}],'collection':[]},0)

    def test_europepmc_empty_container_is_a_valid_empty_page(self):
        page=paginate._europepmc_parse({'hitCount':3,'resultList':{},'nextCursorMark':'same'},'same')
        self.assertEqual(page.records,[])
        self.assertEqual(page.total,3)
        self.assertIsNone(page.next_state)

    def test_europepmc_absent_result_container_is_still_an_error(self):
        with self.assertRaises(RuntimeError):
            paginate._europepmc_parse({'hitCount':0},'*')

    def test_rxiv_versions_are_distinct(self):
        a=paginate.record_key('biorxiv',{'doi':'10.1101/x','version':'1'})
        b=paginate.record_key('biorxiv',{'doi':'10.1101/x','version':'2'})
        self.assertNotEqual(a,b)

    def test_crossref_doi_identity_is_case_insensitive(self):
        self.assertEqual(paginate.record_key('crossref',{'DOI':'10.1/ABC'}),paginate.record_key('crossref',{'DOI':'10.1/abc'}))

    def test_openalex_page_size_is_supported_maximum(self):
        self.assertIn('per-page=100',paginate._openalex_url('search=q','*',200))

    def test_crossref_uses_conservative_list_pacing(self):
        self.assertGreaterEqual(paginate.APIS['crossref'].delay,1)

    def test_crossref_keyword_sample_requests_relevance_order(self):
        from urllib.parse import parse_qs, urlsplit
        q=parse_qs(urlsplit(paginate._crossref_url('query.bibliographic=breast+cancer','*',10)).query)
        self.assertEqual(q['sort'],['score'])
        self.assertEqual(q['order'],['desc'])

    def test_crossref_keeps_explicit_order_and_filter_only_walks(self):
        from urllib.parse import parse_qs, urlsplit
        q=parse_qs(urlsplit(paginate._crossref_url('query=breast&sort=published&order=asc','*',10)).query)
        self.assertEqual(q['sort'],['published'])
        self.assertEqual(q['order'],['asc'])
        self.assertNotIn('sort=',paginate._crossref_url('filter=prefix:10.1','*',10))

    def test_europepmc_rejects_unknown_mesh_field_but_allows_quoted_text(self):
        with self.assertRaisesRegex(RuntimeError,'no MESH: field'):
            paginate.validate_query('europepmc','MESH:"Breast Neoplasms" AND TITLE:young')
        paginate.validate_query('europepmc','KW:"Breast Neoplasms" AND TITLE:young')
        paginate.validate_query('europepmc','TITLE:"MESH: a method"')

    def test_http_error_does_not_echo_secrets(self):
        url='https://example.invalid/?api_key=TOP_SECRET'
        error=urllib.error.HTTPError(url,429,'limit',{'Retry-After':'9'},io.BytesIO(b'TOP_SECRET'))
        with patch.object(paginate.urllib.request,'urlopen',side_effect=error):
            with self.assertRaises(paginate.FetchError) as caught:
                paginate.fetch(url)
        self.assertNotIn('TOP_SECRET',str(caught.exception))
        self.assertEqual(caught.exception.retry_after,9)

    def test_server_response_can_slow_down_requests(self):
        response=io.BytesIO(b'{"results":[],"meta":{"count":0}}')
        response.headers={'x-rate-limit-limit':'1','x-rate-limit-interval':'2s'}
        with patch.object(paginate.urllib.request,'urlopen',return_value=response):
            result=paginate.fetch('https://example.invalid/')
        self.assertGreaterEqual(result.delay,2)

    def test_retry_after_accepts_http_date(self):
        from email.utils import formatdate
        with patch.object(paginate.time,'time',return_value=1000):
            self.assertEqual(paginate.retry_seconds(formatdate(1010,usegmt=True)),10)

    def test_nontransient_http_error_is_not_retried(self):
        error=urllib.error.HTTPError('https://example.invalid',400,'bad query',{},io.BytesIO(b'error'))
        with patch.object(paginate.urllib.request,'urlopen',side_effect=error):
            with self.assertRaises(paginate.FetchError) as caught:
                paginate.fetch('https://example.invalid')
        self.assertFalse(caught.exception.retryable)

    def test_invalid_url_error_does_not_echo_credentials(self):
        import http.client
        with patch.object(paginate.urllib.request,'urlopen',side_effect=http.client.InvalidURL('bad URL with SECRET')):
            with self.assertRaises(paginate.FetchError) as caught:
                paginate.fetch('https://example.invalid/?api_key=SECRET')
        self.assertNotIn('SECRET',str(caught.exception))

    def test_query_cannot_override_pagination_or_persist_credentials(self):
        for q in ('search=q&api_key=SECRET','search=q&cursor=other','search=q&per-page=200'):
            with self.subTest(q=q),self.assertRaises(RuntimeError):
                paginate.validate_query('openalex',q)

    def test_reconciliation_unknown_count_is_unverified(self):
        r=Reconciliation(expected=None,retrieved=1,pages=1)
        self.assertIsNone(r.complete)
        self.assertTrue(r.ok)

    def test_skill_curl_parameters_are_separate(self):
        text=(SKILL/'SKILL.md').read_text()
        self.assertNotIn("--data-urlencode 'format=json&pageSize",text)
        self.assertIn("--data-urlencode 'pageSize=10'",text)
        for path in [SKILL/'SKILL.md', *sorted((SKILL/'references').glob('*.md'))]:
            with self.subTest(path=path.name):
                self.assertNotRegex(path.read_text(), r"--data-urlencode\s+['\"][^'\"]*=[^'\"]*&[A-Za-z][A-Za-z0-9_-]*=")


if __name__=='__main__':
    unittest.main()
