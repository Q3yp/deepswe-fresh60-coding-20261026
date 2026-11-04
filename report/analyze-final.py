import json,re,math,collections,statistics
from pathlib import Path
from datetime import datetime,timezone
import numpy as np

root=Path(__file__).resolve().parent.parent
plan=json.loads((root/'experiment-plan.json').read_text());rows=json.loads((root/'results.json').read_text())
assert len(rows)==240 and all(r['status']=='scored' for r in rows), 'Final analysis requires 240 primary scores'
conditions=['bundled','override-coding'];tasks={t['name']:t for t in plan['tasks']};files=[];slot_code={}
code_ext={'.go','.py','.pyi','.js','.jsx','.mjs','.cjs','.ts','.tsx','.mts','.cts','.rs','.sh','.c','.h','.cpp','.java','.html','.css','.scss','.vue','.svelte','.ne','.jinja','.j2'}
for r in rows:
 b=json.loads((root/'behavior'/f"{r['job']}.json").read_text());v=b['validation']
 reviewed_tests=set(v.get('new_test_files',[])+v.get('new_test_code_files',[])+v.get('modified_existing_test_files',[]))
 embedded=set(v.get('embedded_tests_in_production_file',[]))
 patch=(root/r['result_path']).parent/'artifacts/model.patch'
 entries=[]
 for part in patch.read_text().split('diff --git ')[1:]:
  m=re.search(r'^\+\+\+ b/(.*)$',part,re.M) or re.search(r'^--- a/(.*)$',part,re.M)
  if not m:continue
  name=m[1];ext=Path(name).suffix;segments=set(Path(name).parts)
  is_test=name in reviewed_tests or bool(segments & {'test','tests','__tests__','fixtures','__fixtures__','__snapshots__','dtslint','testdata','testutils','query-test-utils'}) or name.endswith('_test.go') or bool(re.search(r'\.(test|spec)(-d)?\.[cm]?[jt]sx?$',name)) or name.endswith('.snap')
  group='tests' if is_test else 'docs' if ext in {'.md','.mdx','.rst'} or bool(segments & {'docs','doc','documentation'}) else 'examples' if bool(segments & {'examples','example','demo','demos'}) else 'source' if ext in code_ext else 'other'
  counts=collections.Counter();in_hunk=False;block=False;triple=None;in_embedded=False
  for line in part.splitlines():
   if line.startswith('@@'):in_hunk=True;block=False;triple=None;continue
   if not in_hunk or line.startswith('\\'):continue
   if not line.startswith(('+','-',' ')):continue
   sign,text=line[0],line[1:];s=text.strip()
   if name in embedded and s=='#[cfg(test)]' and sign!='-':in_embedded=True
   category='tests' if in_embedded else group
   if sign in '+-':counts[category+('_added' if sign=='+' else '_removed')]+=1
   if sign=='-':continue
   stripped=s
   if ext in {'.py','.pyi'}:
    if triple:
     if triple in stripped:triple=None
     stripped=''
    elif stripped.startswith(('"""',"'''")):
     delimiter=stripped[:3]
     if delimiter not in stripped[3:]:triple=delimiter
     stripped=''
    elif stripped.startswith('#'):stripped=''
   else:
    if block:
     if '*/' in stripped:stripped=stripped.split('*/',1)[1].lstrip();block=False
     else:stripped=''
    if stripped.startswith('/*'):
     if '*/' in stripped[2:]:stripped=stripped.split('*/',1)[1].lstrip()
     else:block=True;stripped=''
    if stripped.startswith('//') or (ext=='.sh' and stripped.startswith('#')):stripped=''
   if sign=='+':
    if not s:counts[category+'_blank_added']+=1
    elif not stripped:counts[category+'_comment_only_added']+=1
    else:counts[category+'_nonblank_noncomment_added']+=1
  entry={'job':r['job'],'path':name,'category':group,'embedded_test_split':name in embedded,**counts};entries.append(entry);files.append(entry)
 totals=collections.Counter()
 for e in entries:totals.update({k:v for k,v in e.items() if k.endswith(('_added','_removed'))})
 slot_code[r['job']]=dict(totals)
metrics=['agent_seconds','input_tokens','cached_input_tokens','uncached_input_tokens','output_tokens','reasoning_output_tokens','tool_calls','all_added','source_added','source_nonblank_noncomment_added','source_comment_only_added','tests_added','docs_added','examples_added']
paired=[]
for task in tasks:
 rr=[r for r in rows if r['task']==task];assert len(rr)==4
 p={'task':task,'language_metadata':tasks[task]['language'],'repository_seen_before':tasks[task].get('repository_seen_in_previous30',False),'conditions':{}}
 for c in conditions:
  cc=[r for r in rr if r['condition']==c];assert sorted(r['repeat'] for r in cc)==[1,2]
  d={'passed':sum(r['reward'] for r in cc),'reward':statistics.mean(r['reward'] for r in cc)}
  for m in metrics:
   values=[]
   for r in cc:
    sc=slot_code[r['job']]
    values.append(r['input_tokens']-r['cached_input_tokens'] if m=='uncached_input_tokens' else sum(v for k,v in sc.items() if k.endswith('_added') and not any(z in k for z in ['blank','comment'])) if m=='all_added' else sc.get(m,0) if m.endswith('_added') else r[m])
   d[m]=statistics.mean(values)
  p['conditions'][c]=d
 paired.append(p)

rng=np.random.default_rng(20261031);indices=rng.integers(0,60,size=(100000,60))
def paired_analysis(pop):
 n=len(pop);out={};ix=indices if n==60 else rng.integers(0,n,size=(100000,n))
 for m in ['reward',*metrics]:
  a=np.array([p['conditions']['bundled'][m] for p in pop],float);b=np.array([p['conditions']['override-coding'][m] for p in pop],float);diff=b-a
  ba=a[ix].mean(axis=1);bb=b[ix].mean(axis=1)
  out[m]={'bundled_mean':float(a.mean()),'coding_mean':float(b.mean()),'difference':float(diff.mean()),'difference_bootstrap95':np.percentile(bb-ba,[2.5,97.5]).tolist(),'relative_change_percent':float(100*(b.mean()/a.mean()-1)) if a.mean() else None,'relative_bootstrap95_percent':np.percentile(100*(bb/ba-1),[2.5,97.5]).tolist() if np.all(ba>0) else None,'coding_lower_tasks':int(sum(diff<0)),'coding_higher_tasks':int(sum(diff>0)),'ties':int(sum(diff==0)),'median_task_difference':float(np.median(diff))}
 deltas=[p['conditions']['override-coding']['passed']-p['conditions']['bundled']['passed'] for p in pop]
 distribution={0:1}
 for d in deltas:
  if d==0:continue
  nxt=collections.Counter()
  for s,v in distribution.items():nxt[s+abs(d)]+=v;nxt[s-abs(d)]+=v
  distribution=dict(nxt)
 observed=abs(sum(deltas));out['reward']['paired_sign_flip_exact_p']=sum(v for s,v in distribution.items() if abs(s)>=observed)/sum(distribution.values())
 return {'tasks':n,'slots_per_condition':n*2,'passes':{c:sum(p['conditions'][c]['passed'] for p in pop) for c in conditions},'metrics':out}
analysis={'created_at':datetime.now(timezone.utc).isoformat(),'scored_slots':240,'tasks':60,'primary':paired_analysis(paired),'subgroups':{},'task_pairs':paired,'slot_code':slot_code,'method':{'primary_unit':'Task; average two repeats per condition; retain both attempts and all valid zeros.','score_test':'Exact two-sided condition-label sign-flip test on 60 task-paired pass-count differences.','intervals':'Percentile paired-task bootstrap,100000 resamples, fixed NumPy RNG seed20261031; same resampled task indices for both conditions. Descriptive95% intervals, no multiplicity correction for secondary metrics or subgroups.','efficiency':'Model agent execution only; excludes setup/grading/downtime. One valid memory-limit failure included. Unreported external-interruption usage stays null.','code':'Unified-diff changed physical lines. Reviewed test paths plus path conventions separate tests/fixtures, documentation, examples, source extensions, other files. Reviewed Rust cfg(test) suffixes separated. Source proxy excludes blank and comment-looking lines using hunk-local lexical rules; inline comments remain code, docstring/string ambiguity possible. This is not an AST complexity measure.','scope':'Fresh60 study only; selected from83 remaining tasks, quota sampling,52 unseen repositories and8 previously seen repositories; no imported scores.','original_score':'Model-complete infrastructure-interrupted graders replaced by first valid same-patch official grade; native originals preserved. Ordinary scored zeros and12 test-overlay observations remain unchanged.'},'interruption_usage':json.loads((root/'infrastructure/interrupted-attempts-summary.json').read_text())}
for label,subset in [('unseen_repositories',[p for p in paired if not p['repository_seen_before']]),('seen_repositories',[p for p in paired if p['repository_seen_before']])]:analysis['subgroups'][label]=paired_analysis(subset)
observations=json.loads((root/'infrastructure/fixture-diagnostics-final-disposition.json').read_text())
flagged_tasks={d['job'].split('--')[0] for d in observations['entries']}
analysis['posthoc_sensitivity']={'without_eight_overlay_tasks':paired_analysis([p for p in paired if p['task'] not in flagged_tasks]),'without_optique_resource_failure_task':paired_analysis([p for p in paired if p['task']!='optique-conditional-option-dependencies'])}
analysis['posthoc_sensitivity']['method']='Remove entire tasks from both conditions, both repeats. Selected after outcomes; different population, not corrected official scores and not an estimate of hypothetical regrades.'
analysis['native_original_scores']={c:{'passes':sum((json.loads((root/r['result_path']).read_text()).get('verifier_result') or {}).get('rewards',{}).get('reward',0) for r in rows if r['condition']==c),'records_with_native_grade':sum(json.loads((root/r['result_path']).read_text()).get('verifier_result') is not None for r in rows if r['condition']==c)} for c in conditions}
analysis['language_scores']={lang:{c:{'passes':sum(p['conditions'][c]['passed'] for p in paired if p['language_metadata']==lang),'slots':2*sum(p['language_metadata']==lang for p in paired)} for c in conditions} for lang in plan['language_quotas']}
analysis['recoveries']=[{'job':r['job'],**json.loads(((root/r['result_path']).parent/'verifier-recovery.json').read_text())} for r in rows if r['verifier_recovered']]
(root/'report/final-analysis.json').write_text(json.dumps(analysis,indent=2)+'\n');(root/'report/final-code-file-metrics.json').write_text(json.dumps(files,indent=2)+'\n');(root/'report/checkpoint-240-results.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(analysis['primary'],indent=2))
