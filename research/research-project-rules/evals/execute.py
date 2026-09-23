#!/usr/bin/env python3
"""Execute prepared synthetic cases with isolated Claude Code file tools.
Authentication/model routing must already be available in the process environment.
This script never reads user settings or credentials and never installs packages.
"""
import argparse,collections,json,subprocess,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path

SYSTEM='''You are executing one synthetic research-project task. All task material is in the current directory. Do not read outside it, use network resources, global skills, memory, or unrelated projects. Follow the supplied task and its local project instructions. If skill-under-test/SKILL.md exists, read it and only its relevant supporting files. Do not change the skill-under-test directory. You have file tools only in this execution phase; a separate evaluator runs generated code. Do not claim code was executed. Complete authorized file changes. File Write can create parent directories. For required empty directories, write a JSON list of relative directory paths to directory_requests.json; the harness will create those directories after the turn. Do not create this file when no new directories are needed. End with a concise factual handoff using relative paths. Never inspect sibling runs or grading criteria.'''


def clean(value,task):
 if isinstance(value,str): return value.replace(str(task),'<TASK>')
 if isinstance(value,list): return [clean(x,task) for x in value]
 if isinstance(value,dict): return {k:clean(v,task) for k,v in value.items()}
 return value


def sanitize_transcript(events):
 """Keep observable actions/results; omit opaque provider metadata and reasoning."""
 ids={}
 def visible(value):
  if isinstance(value,list):
   return [visible(x) for x in value if not isinstance(x,dict) or x.get('type') not in {'thinking','redacted_thinking'}]
  if isinstance(value,dict):
   output={}
   for key,item in value.items():
    if key in {'signature'}: continue
    if key in {'id','tool_use_id'} and isinstance(item,str):
     if item not in ids: ids[item]='tool_'+str(len(ids)+1)
     output[key]=ids[item]
    else: output[key]=visible(item)
   return output
  return value
 return visible(events)


def run_one(run,timeout):
 task=(run/'task').resolve();prompt=(run/'executor_prompt.txt').read_text()
 if (run/'runtime.json').exists(): raise ValueError('Refusing to overwrite a completed run')
 skill_entry=task/'skill-under-test/SKILL.md'
 system=SYSTEM
 if skill_entry.exists():
  system+='\n\nThe selected skill entry is preloaded below. Resolve its relative resources under skill-under-test/:\n\n'+skill_entry.read_text()
 args=['claude','--safe-mode','--restricted','--tools','Read,Write,Edit,Glob,Grep',
       '--permission-mode','acceptEdits','--strict-mcp-config','--mcp-config','{"mcpServers":{}}',
       '--no-session-persistence','--output-format','stream-json','--verbose',
       '--max-budget-usd','2','--system-prompt',system,'-p',prompt]
 start=time.monotonic()
 try:
  cp=subprocess.run(args,cwd=task,capture_output=True,text=True,timeout=timeout)
  raw=cp.stdout;code=cp.returncode
 except subprocess.TimeoutExpired as e:
  raw=e.stdout or '';raw=raw.decode() if isinstance(raw,bytes) else raw;code=124
 elapsed=time.monotonic()-start
 events=[];final={};calls=collections.Counter();message_text=[]
 for line in raw.splitlines():
  try: event=json.loads(line)
  except ValueError: continue
  if event.get('type') in {'assistant','user'}:
   message=event.get('message',{})
   blocks=message.get('content',[])
   for block in blocks if isinstance(blocks,list) else []:
    if block.get('type')=='tool_use': calls[block.get('name','unknown')]+=1
    if block.get('type')=='text' and message.get('role')=='assistant': message_text.append(block.get('text',''))
   events.append(clean({'role':message.get('role'),'content':blocks},task))
  elif event.get('type')=='result': final=event
 usage=final.get('usage',{})
 tokens=sum(usage.get(k,0) or 0 for k in ['input_tokens','output_tokens','cache_creation_input_tokens','cache_read_input_tokens'])
 status={'exit_code':code,'is_error':final.get('is_error',True),'terminal_reason':final.get('terminal_reason'),
         'model_names':list(final.get('modelUsage',{})),'permission_denials':clean(final.get('permission_denials',[]),task),
         'total_tool_calls':sum(calls.values()),'tool_calls':dict(calls),'num_turns':final.get('num_turns'),'skill_entry_preloaded':skill_entry.exists()}
 (run/'runtime.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
 (run/'timing.json').write_text(json.dumps({'total_duration_seconds':elapsed,'duration_ms':round(elapsed*1000),'total_tokens':tokens if usage else None,'token_accounting':'API usage including cache read/creation; not a character estimate'},indent=2)+'\n')
 (run/'transcript.json').write_text(json.dumps(sanitize_transcript(events),ensure_ascii=False,indent=2)+'\n')
 text=final.get('result') or '\n\n'.join(message_text)
 (run/'outputs/response.md').write_text(clean(text,task)+'\n')
 requests=task/'directory_requests.json'
 if requests.exists() and code==0 and not status['is_error']:
  paths=json.loads(requests.read_text())
  if not isinstance(paths,list): raise ValueError('directory_requests must be a list')
  for rel in paths:
   if not isinstance(rel,str) or Path(rel).is_absolute(): raise ValueError('directory path must be relative')
   dest=(task/rel).resolve()
   if not dest.is_relative_to(task) or (task/'skill-under-test') in (dest,*dest.parents):
    raise ValueError('directory request escaped the task')
   dest.mkdir(parents=True,exist_ok=True)
  requests.unlink()
 print(json.dumps({'run':str(run.parent.parent.name)+'/'+run.parent.name,'completed':code==0 and not status['is_error'],'seconds':round(elapsed,1),'tool_calls':sum(calls.values())}),flush=True)


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('iteration',type=Path);p.add_argument('--workers',type=int,default=2);p.add_argument('--timeout',type=int,default=240)
 a=p.parse_args()
 runs=sorted(a.iteration.glob('eval-*/*/run-*'))
 with ThreadPoolExecutor(max_workers=a.workers) as pool:
  futures=[pool.submit(run_one,r,a.timeout) for r in runs]
  for f in as_completed(futures): f.result()
if __name__=='__main__':main()
