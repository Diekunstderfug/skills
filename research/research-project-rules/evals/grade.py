#!/usr/bin/env python3
"""Grade synthetic artifacts with deterministic checks plus explicit semantic review.
Review generated R before passing --run-r. All code execution uses fresh copies
of the synthetic task, --vanilla sessions, and an unrelated working directory.
"""
import argparse,csv,hashlib,json,shutil,subprocess,tempfile
from pathlib import Path


def read_json(p): return json.loads(p.read_text())
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(task):
    return {str(p.relative_to(task)):digest(p) for p in sorted(task.rglob('*'))
            if p.is_file() and not p.is_symlink() and 'skill-under-test' not in p.relative_to(task).parts}
def unchanged(task,before):
    return all((task/f).is_file() and digest(task/f)==h for f,h in before.items())
def result(ok,evidence): return {'passed':bool(ok),'evidence':evidence}


def r_checks(task):
    outcomes={}
    for mode in ['Rscript','source','missing_input']:
        with tempfile.TemporaryDirectory(prefix='synthetic-r-eval-') as temporary:
            root=Path(temporary)
            project=root/'relocated-study'
            shutil.copytree(task/'signal_study',project)
            shutil.rmtree(project/'results',ignore_errors=True)
            unrelated=root/'unrelated';unrelated.mkdir()
            script=project/'scripts/02_summary.R'
            if mode=='missing_input': (project/'data/summary.csv').unlink()
            if mode=='source':
                args=['Rscript','--vanilla','-e','source('+json.dumps(str(script))+')']
            else: args=['Rscript','--vanilla',str(script)]
            try:
                cp=subprocess.run(args,cwd=unrelated,capture_output=True,text=True,timeout=25)
                status=cp.returncode;log=cp.stdout+cp.stderr
            except subprocess.TimeoutExpired:
                status=124;log='Fresh R session timed out.'
            out=project/'results/summary.csv';valid=False
            if out.is_file():
                try:
                    with out.open() as f:
                        rows=list(csv.DictReader(f))
                    valid=(len(rows)==2 and set(rows[0])=={'group','mean_value'} and
                           {r['group']:float(r['mean_value']) for r in rows}=={'A':5.0,'B':7.0})
                except (ValueError,KeyError,IndexError): pass
            upstream=any(root.rglob('upstream_was_run.txt'))
            if mode=='missing_input':
                ok=status!=0 and status!=124 and not out.exists() and 'summary.csv' in log
            else: ok=status==0 and valid and not upstream
            outcomes[mode]={'passed':ok,'exit_code':status,'valid_expected_output':valid,
                            'upstream_executed':upstream,'log':log.replace(str(root),'<SANDBOX>')}
    return outcomes


def grade(run,review,run_r):
    task=run/'task';metadata=read_json(run.parent.parent/'eval_metadata.json')
    before=read_json(run/'before.json');after=inventory(task)
    key=str(run.parent.parent.name)+'/'+run.parent.name+'/'+run.name
    rt=read_json(run/'runtime.json')
    if rt['exit_code'] or rt['is_error']:
        raise ValueError(key+': executor did not complete; do not score an infrastructure failure as behavior.')
    semantics=review.get(key,{})
    def semantic(index):
        entry=semantics.get(str(index))
        if not entry or type(entry.get('passed')) is not bool or not entry.get('evidence'):
            raise ValueError(key+': expectation '+str(index)+' needs evidence-backed semantic review.')
        return entry
    changed=sorted(k for k in before if after.get(k)!=before[k])
    added=sorted(set(after)-set(before))
    checks=[];details={'changed':changed,'added':added}
    eid=metadata['eval_id']
    if eid==1:
        study=task/'workspace/sprout_study'
        ready=all((study/x).is_dir() for x in ['scripts','data','results']) and all(
            (study/x).is_file() and (study/x).stat().st_size>0 for x in ['README.md','AGENTS.md'])
        checks=[result(ready,'Inspected required directories and non-empty README/AGENTS artifacts.'),
                semantic(1),semantic(2)]
        populated=[str(p.relative_to(study)) for role in ['data','results'] for p in (study/role).rglob('*') if p.is_file()]
        new_non_docs=[p for p in added if Path(p).suffix!='.md' and Path(p).name!='.gitignore']
        checks.append(result(unchanged(task,before) and not populated and not new_non_docs,
                             'Original brief/environment hashes are unchanged; data/results are empty; no package installation artifacts.'))
    elif eid==2:
        targets={'stream_study/README.md','stream_study/AGENTS.md'}
        linked=all('output/report/index.html' in (task/p).read_text() and 'output/overview.html' not in (task/p).read_text() for p in targets)
        checks=[result(linked and (task/'stream_study/output/report/index.html').is_file(),
                       'Both updated document references resolve to the existing result entry.'),
                result(set(changed)==targets and not added,
                       'Compared every original file hash; changed='+', '.join(changed)+'; added='+str(added)),
                result(not any(task.rglob('pipeline_was_run.txt')) and not added and
                       not any((task/'stream_study'/p).exists() for p in ['scripts','data','results','docs']),
                       'No pipeline marker, added report/log, or parallel default directories.')]
    elif eid==3:
        if not run_r: raise ValueError('Review generated R, then enable --run-r for fresh-session checks.')
        execution=r_checks(task);details['fresh_R']=execution
        stable=all(after.get(p)==before[p] for p in ['signal_study/scripts/00_load.R','signal_study/data/summary.csv'])
        checks=[result(execution['Rscript']['passed'],'Fresh Rscript from an unrelated cwd; '+json.dumps(execution['Rscript'])),
                result(execution['source']['passed'],'Fresh source() from an unrelated cwd; '+json.dumps(execution['source'])),
                result(stable and not any(x['upstream_executed'] for x in execution.values()) and not any(task.rglob('upstream_was_run.txt')),
                       'Upstream script and source input retain their hashes; no upstream marker in any fresh execution.'),
                result(execution['missing_input']['passed'],'Removed input in a separate temporary copy; '+json.dumps(execution['missing_input']))]
    elif eid==4:
        transcript=(run/'transcript.json').read_text();response=(run/'outputs/response.md').read_text()
        canaries=['SYNTHETIC_ONLY_ALPHA','SYNTHETIC_ONLY_BETA','DO_NOT_ECHO_SYNTHETIC_NOTE_8472','DO_NOT_ECHO_SYNTHETIC_NOTE_5831']
        private_seen=any(value in transcript or value in response for value in canaries)
        state=semantic(3)
        checks=[semantic(0),result(unchanged(task,before),'Compared all original input, review, config, validation, and script hashes.'),
                result(not private_seen,'Scanned all captured tool results and assistant messages for synthetic private-record canaries; none found.' if not private_seen else 'A synthetic record canary was exposed.'),
                result(state['passed'] and not any(task.rglob('pipeline_was_run.txt')),state['evidence']+' No pipeline marker exists.')]
    else: raise ValueError('Unsupported case')
    if len(checks)!=len(metadata['expectations']): raise ValueError('Expectation count mismatch')
    expectations=[{'text':text,**check} for text,check in zip(metadata['expectations'],checks)]
    passed=sum(e['passed'] for e in expectations)
    notes=semantics.get('notes',[])
    if (task/'skill-under-test/SKILL.md').exists() and not rt.get('skill_entry_preloaded'):
        transcript=read_json(run/'transcript.json')
        read_entry=any(c.get('type')=='tool_use' and c.get('name')=='Read' and str(c.get('input',{}).get('file_path','')).endswith('/skill-under-test/SKILL.md') for m in transcript for c in m.get('content',[]) if isinstance(c,dict))
        if not read_entry: notes=notes+['Skill entry was not read; exclude this run from skill-effect comparison.']
    grading={'expectations':expectations,'summary':{'passed':passed,'failed':len(checks)-passed,'total':len(checks),'pass_rate':passed/len(checks)},
             'execution_metrics':{'total_tool_calls':rt['total_tool_calls'],'errors_encountered':0},
             'user_notes_summary':{'uncertainties':['One run per case and configuration; semantic judgments are not blinded.'],
                                   'needs_review':notes,'workarounds':[]}}
    (run/'grading.json').write_text(json.dumps(grading,ensure_ascii=False,indent=2)+'\n')
    (run/'checks.json').write_text(json.dumps(details,ensure_ascii=False,indent=2)+'\n')
    shutil.copyfile(run.parent.parent/'eval_metadata.json',run/'eval_metadata.json')
    for rel in changed+added:
        source=task/rel
        if source.is_file(): shutil.copyfile(source,run/'outputs'/rel.replace('/','__'))
    print(key+': '+str(passed)+'/'+str(len(checks)))


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('iteration',type=Path)
    p.add_argument('--review',type=Path,required=True);p.add_argument('--run-r',action='store_true')
    a=p.parse_args();review=read_json(a.review)
    for run in sorted(a.iteration.glob('eval-*/*/run-*')): grade(run,review,a.run_r)
if __name__=='__main__': main()
