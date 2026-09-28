"""Build/run the focused durable-capture-gap condition; no capture/read bridge."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import run

p=argparse.ArgumentParser();p.add_argument('mode',choices=('build','run'));p.add_argument('--output',type=Path,required=True);p.add_argument('--client',choices=('claude','codex'))
a=p.parse_args();out=a.output.resolve()
if a.mode=='build':
    run.build(out)
    frozen=json.loads((out/'frozen.json').read_text())
    for client,case in frozen['trajectories'].items():
        project=Path(case['project'])
        instructions=project/case['instruction']
        instructions.write_text(instructions.read_text().replace('Entry point: notes/current.md\n',
            'Entry point: notes/current.md\nEvent journal: jsonl\nEvent journal directory: history/events\n'))
        case['after_upgrade']=run.hashes(project)
        (out/(client+'-upgraded')/case['instruction']).write_text(instructions.read_text())
        common=case['prompts']['missing-helper'].split('Use context-docs to maintain',1)[0]
        invocation='/context-docs' if client=='claude' else 'Use context-docs'
        case['prompts']['missing-helper']=(invocation+' Maintain notes from the new supplied evidence/pending.md, following existing project settings. '
            'Installed packages are immutable; report unavailable capabilities and continue authorized documentation work.\n\nEvaluation constraints:\n'+common)
        case['prompts']['audit']=(invocation+' Conduct a read-only investigation: what new check is pending, was it executed, was the fact journaled, '
            'and what caused any capture gap? Cite stored evidence and distinguish the historical capture attempt from current availability. '
            'Do not rerun checks, repair, backfill or write anything.\n\nEvaluation constraints:\n'+common)
    frozen['condition']='Two sessions per client: logging enabled by fixture, requested capture with absent helper, then fresh investigation after restoration'
    for file in ('gap.py','gap-protocol.md'):
        source=run.HERE/file;rel=source.relative_to(run.ROOT)
        target=out/'source'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
        frozen['sources'][str(rel)]=hashlib.sha256(source.read_bytes()).hexdigest()
    shutil.copy2(run.HERE/'gap-protocol.md',out/'gap-protocol.md')
    run.dump(out/'frozen.json',frozen)
else:
    run.STAGES=('missing-helper','audit')
    run.run(out,a.client)
