#!/usr/bin/env python3
"""Prepare isolated synthetic tasks; never scan or copy real project data."""
import argparse, hashlib, json, shutil
from pathlib import Path


def snapshot(directory):
    return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(directory.rglob('*')) if p.is_file() and not p.is_symlink()}


def copy_skill(source, target):
    if not (source/'SKILL.md').is_file():
        raise ValueError('Skill source must contain SKILL.md')
    target.mkdir()
    for p in source.rglob('*'):
        rel=p.relative_to(source)
        if rel.parts[0] in {'.git','evals'} or p.is_symlink() or not p.is_file():
            continue
        if p.suffix not in {'.md','.yaml','.R'}:
            continue
        text=p.read_text()
        if '/root/' in text or '/home/' in text:
            raise ValueError('A skill snapshot contains a host-specific path; sanitize it before evaluation.')
        dest=target/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text)


def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--skill',type=Path,required=True)
    a.add_argument('--baseline-skill',type=Path)
    a.add_argument('--out',type=Path,required=True)
    a.add_argument('--case-id',type=int,help='Prepare only this case for a targeted rerun.')
    args=a.parse_args()
    if args.out.exists() and any(args.out.iterdir()):
        raise SystemExit('Use an empty output directory; existing runs are never overwritten.')
    suite=Path(__file__).parent
    cases=json.loads((suite/'evals.json').read_text())['evals']
    if args.case_id is not None:
        cases=[c for c in cases if c['id']==args.case_id]
        if not cases: raise SystemExit('Unknown case id')
    for case in cases:
        parent=args.out/('eval-'+str(case['id'])+'-'+case['name']);parent.mkdir(parents=True)
        (parent/'eval_metadata.json').write_text(json.dumps({
            'eval_id':case['id'],'eval_name':case['name'],'prompt':case['prompt'],
            'expectations':case['expectations']},ensure_ascii=False,indent=2)+'\n')
        variants=['new_skill','old_skill'] if args.baseline_skill else ['with_skill','without_skill']
        for variant in variants:
            run=parent/variant/'run-1';task=run/'task';run.mkdir(parents=True)
            shutil.copytree(suite/'fixtures'/case['name'],task)
            baseline=snapshot(task)
            (run/'before.json').write_text(json.dumps(baseline,indent=2)+'\n')
            if variant in {'new_skill','with_skill','old_skill'}:
                source=args.baseline_skill if variant=='old_skill' else args.skill
                copy_skill(source,task/'skill-under-test')
            (run/'outputs').mkdir()
            (run/'executor_prompt.txt').write_text(case['prompt']+'\n')
    print('Prepared',len(cases)*len(variants),'isolated runs.')

if __name__=='__main__': main()
