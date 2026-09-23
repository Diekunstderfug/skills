#!/usr/bin/env python3
"""Render graded synthetic runs with the pinned official Anthropic eval tooling."""
import argparse,importlib.util,json,subprocess
from pathlib import Path


def load_module(path):
    spec=importlib.util.spec_from_file_location('official_aggregate',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('iteration',type=Path)
    p.add_argument('--official-skill-creator',type=Path,required=True)
    a=p.parse_args()
    runs=sorted(a.iteration.glob('eval-*/*/run-*'))
    if not runs: raise SystemExit('No graded runs found')
    models=set();counts={}
    for run in runs:
        runtime=json.loads((run/'runtime.json').read_text())
        if runtime['exit_code'] or runtime['is_error']: raise SystemExit('Unsuccessful executor run must be resolved before comparison.')
        timing=json.loads((run/'timing.json').read_text())
        if not timing.get('total_tokens'): raise SystemExit('Missing measured token usage; never substitute output character counts.')
        grading=json.loads((run/'grading.json').read_text())
        if any('exclude this run' in x.lower() for x in grading.get('user_notes_summary',{}).get('needs_review',[])):
            raise SystemExit('Selected runs include an invalid skill-loading attempt.')
        models.update(runtime.get('model_names',[]))
        pair=(run.parent.parent.name,run.parent.name);counts[pair]=counts.get(pair,0)+1
    aggregate=load_module(a.official_skill_creator/'scripts/aggregate_benchmark.py')
    benchmark=aggregate.generate_benchmark(a.iteration,'research-project-rules','skill-under-test')
    benchmark['metadata'].update({
        'executor_model':', '.join(sorted(models)),
        'executor_host':'Claude Code isolated file-tool processes; provider model labels are reported verbatim',
        'analyzer_model':'Deterministic artifact/runtime checks plus unblinded semantic review',
        'runs_per_configuration':next(iter(set(counts.values()))) if len(set(counts.values()))==1 else 'varies',
        'aggregation':'Unweighted mean of case pass rates; pooled assertion counts are reported separately',
        'trigger_eval_status':'prepared_not_executed'})
    benchmark['notes']=[
        'Pilot only: one execution per case/configuration. Dispersion is across different tasks, not a reliability estimate from repeated trials.',
        'The configured provider model is not necessarily an Anthropic model. Results apply to the reported executor, not all Claude or Codex models.',
        'Only synthetic fixtures and sanitized skill snapshots were supplied. Global skill discovery, hooks, MCP, memory, and session persistence were disabled.',
        'Actors used file tools only; a separate evaluator ran reviewed generated R in fresh relocated synthetic copies.',
        'Semantic judgments are unblinded. No claim of statistical significance or universal performance improvement.',
        'Native skill-selection queries are prepared separately and have not been executed; behavior scores are not trigger scores.',
        'Any source iteration selection and rejected first attempts are documented in selection.json.']
    pooled={}
    for row in benchmark['runs']:
        totals=pooled.setdefault(row['configuration'],{'passed':0,'total':0})
        for key in totals: totals[key]+=row['result'][key]
    benchmark['pooled_assertions']=pooled
    (a.iteration/'benchmark.json').write_text(json.dumps(benchmark,ensure_ascii=False,indent=2)+'\n')
    (a.iteration/'benchmark.md').write_text(aggregate.generate_markdown(benchmark)+'\n')
    subprocess.run(['python3',str(a.official_skill_creator/'eval-viewer/generate_review.py'),
                    str(a.iteration),'--skill-name','research-project-rules',
                    '--benchmark',str(a.iteration/'benchmark.json'),'--static',str(a.iteration/'review.html')],check=True)
    print(json.dumps(pooled))
if __name__=='__main__': main()
