"""Public synthetic worlds, three layouts each, and hidden-at-execution evidence ledgers.

Authored for this study, not independent held-out projects. No private project input.
"""
from copy import deepcopy
from textwrap import dedent


def text(s):
    return dedent(s).strip() + '\n'


def fact(key, expected, sources, *, critical=False):
    return dict(id=key, expected=expected, sources=sources, critical=critical)


WORLDS = {
 'kestrel': {
  'title': 'Kestrel field catalogue',
  'purpose': 'A static catalogue of approved sample equipment manuals for a small pilot team.',
  'sources': {
   'config/service.yaml': 'timeout_seconds: 60\n',
   'evidence/01-design.txt': text('''
       September 1, 2026 — Contributor release design, not an owner decision.
       Publish on every main-branch push after mandatory CI. Automation would reduce
       repetitive operator work and tie artifacts to source revisions. A proposed
       timeout of 30 seconds would keep failed builds from occupying an operator.
       These are design suggestions, not a record of implementation or deployment.
       The catalogue is a static artifact; equipment specifications remain upstream.
   '''),
   'evidence/02-owner.txt': text('''
       September 8, 2026 — Owner Mira, DEC-101: approve manual publication for the
       pilot, with optional CI, so the operator reviews every artifact. The command
       is `wrangler pages deploy dist`. Automatic Git publication and mandatory CI
       remain deferred proposals, not the current policy. Revisit them if release
       frequency makes their setup worthwhile. A new proposal date is not approval.
       DEC-102: only approved sample manuals may enter the catalogue. Public/customer
       uploads and external ingestion are not approved; document rights and update
       ownership must be agreed before expanding sources. This boundary survives
       changes to the publication process.
   '''),
   'evidence/03-review.txt': text('''
       September 13, 2026 — Preview reviewer note.
       Keep preview links with their artifact revision. Rebuilding a preview does
       not transfer a previous review to the replacement. A failed preview alone
       does not show a failed production deployment. The previous accepted artifact
       should remain available until its replacement is accepted; do not reconstruct
       it from a newer revision and call that the reviewed artifact.
   '''),
   'evidence/04-work.txt': text('''
       September 15, 2026 — Operator work list.
       REST-101 is blocked: no disposable restore volume has been allocated. Next:
       operator requests a test volume, then runs and records the restore exercise.
       CAL-102 is separately blocked: a leading-zero sensor identifier is absent
       from the calibration sample. Next: ask the test maintainer for an approved
       synthetic sample. Neither blocker is resolved merely by writing a procedure.
       No production on-call owner has been assigned in the supplied project records.
       Escalation contact remains an open staffing question, not Mira's automatic role.
   '''),
   'evidence/05-demo.txt': text('''
       September 20, 2026 — Contributor demonstration note.
       A Git integration might have been enabled during a dashboard demonstration.
       The screenshot is missing. No owner decision superseding DEC-101 accompanies
       this note. Confirm settings before a real release; do not treat possible
       implementation as owner approval. This note cannot establish the deployed
       revision or publication path. Receipt storage has not been selected yet.
   '''),
   'evidence/06-build.txt': text('''
       September 21, 2026 — Local build observation.
       Building the sample catalogue produced an artifact. The checked-in timeout
       is now 60 seconds. This observation says nothing about production rollout.
       A staging-only preview receipt names revision sample-17; it is not production
       evidence and does not establish the timeout used by the running pilot site.
       No production receipt or runtime configuration export is supplied.
   '''),
  },
  'uncommitted': {'scratch/operator.txt': text('''
       Uncommitted operator note, September 22, 2026.
       The restore fixture uses `./data files/pilot.db`. Preserve its sparse-file
       flag when allocating the test volume; otherwise quota estimates are wrong.
       Ask the storage maintainer before reserving the volume. Keep this constraint
       even after allocation or a successful restore; future exercises still need it.
   ''')},
  'updates': {
   'config/service.yaml': 'timeout_seconds: 45\n',
   'evidence/07-update.txt': text('''
       September 25, 2026 — Operator update and repository change.
       The checked-in timeout changed from 60 to 45 seconds. No production rollout
       or runtime observation accompanies the change. REST-101 is now closed: the
       disposable volume was allocated with its sparse-file flag preserved and the
       synthetic restore exercise passed on September 25, receipt restore-25.
       This closes only REST-101. CAL-102 still lacks the leading-zero sample; ask
       the test maintainer for it. DEC-101 manual publication and DEC-102 source
       restrictions still apply. Production on-call ownership remains unassigned.
   '''),
  },
 },
 'oriole': {
  'title': 'Oriole warehouse reconciliation',
  'purpose': 'An offline tool that compares local warehouse exports for human review without modifying either input.',
  'sources': {
   'config/report.yaml': 'batch_rows: 200\nformats: [csv]\n',
   'evidence/01-design.txt': text('''
       September 2, 2026 — Contributor draft design.
       A hosted viewer could support shared review. A simple matcher might compare
       item identifiers as numbers and treat blank quantities as zero. A batch of
       100 rows was suggested for the first demonstration. These are unapproved
       suggestions; they are not requirements or evidence of running behavior.
       A discrepancy report should help a person investigate, not silently pick an
       authoritative ledger. Export timestamps may explain differences between rows.
   '''),
   'evidence/02-owner.txt': text('''
       September 7, 2026 — Owner Lina, DEC-201: approve offline CSV reports for the
       pilot because operators work in a disconnected warehouse office. The tool
       reads local exports and must not modify them. A hosted viewer remains an
       unapproved proposal. Tool output does not approve corrections to warehouse
       records or establish which ledger is financially authoritative.
       DEC-202: match the pair item_id and location_id as opaque strings. Preserve
       case and leading zeros; item-only or numeric matching can merge distinct
       locations or records. A blank quantity means unknown, not zero. These
       decisions supersede the corresponding September 2 draft suggestions.
   '''),
   'evidence/03-usage.txt': text('''
       September 12, 2026 — Supported workflow note.
       Run `oriole compare left.csv right.csv --output report.csv`. Inputs are
       read-only and output must not overwrite either input. Keep source exports
       until a reviewer accepts or rejects the report. The left export determines
       field order, followed by right-only fields in their original order. Duplicate
       item identifiers can represent separate locations; do not deduplicate them
       automatically. Missing records may reflect filtered exports rather than deletion.
   '''),
   'evidence/04-work.txt': text('''
       September 16, 2026 — Work list.
       SAMPLE-201 is open: request an approved synthetic export containing one item
       at two locations, then run the duplicate-location comparison. ENC-202 is
       separately open: request an approved non-ASCII location sample from the
       test maintainer. Passing the duplicate-location case cannot close ENC-202.
       The person authorized to approve actual warehouse ledger corrections has
       not been identified in the supplied records. Lina's tool-design role does
       not establish that she has warehouse correction authority.
   '''),
   'evidence/05-proposal.txt': text('''
       September 20, 2026 — Contributor viewer and JSON proposal.
       A browser viewer might ease shared report review. JSON output could support
       local downstream analysis without changing the offline boundary. Neither
       proposal has owner approval in this note. The contributor made a local viewer
       mockup; implementation of a demo does not establish an approved hosted service.
       No delivery date, production rollout or telemetry system was approved.
   '''),
   'evidence/06-check.txt': text('''
       September 21, 2026 — Repository and test observation.
       The checked-in batch limit is 200 rows and CSV is the configured format.
       A local unit test used a tiny synthetic input. That is not evidence of a
       production installation, of representative warehouse coverage, or of an
       accepted end-user report. No running installation's configuration is supplied.
   '''),
  },
  'uncommitted': {'scratch/reviewer.txt': text('''
       Uncommitted review note, September 22, 2026.
       Keep leading zeros and case in both parts of the matching key. In the fixture,
       item "0042" at location "a" is distinct from "42" at location "A". Preserve
       the input exports while reviewing a discrepancy; never rewrite them to make
       the comparison pass. A blank quantity is missing evidence rather than zero.
   ''')},
  'updates': {
   'config/report.yaml': 'batch_rows: 125\nformats: [csv, json]\n',
   'evidence/07-update.txt': text('''
       September 25, 2026 — Owner Lina and test maintainer update.
       DEC-203: Lina approves optional local JSON reports alongside CSV to support
       downstream offline analysis. The offline and read-only boundaries stay in
       force; the hosted viewer remains an unapproved proposal. DEC-203 supersedes
       CSV-only output, not DEC-202 matching or blank-quantity semantics.
       Configuration now sets batch_rows to 125 and formats to CSV and JSON. No
       running installation was observed. SAMPLE-201 is closed: its synthetic
       duplicate-location fixture was created and the comparison passed, test D201.
       ENC-202 remains open; next action is to request the non-ASCII location sample
       from the test maintainer. Warehouse correction approver remains unidentified.
   '''),
  },
 },
}


def ledger(world, stage):
    final = stage > 0
    if world == 'kestrel':
        return [
          fact('workflow','Manual publication with optional CI, owner Mira / DEC-101, to review every artifact.', ['evidence/02-owner.txt'],critical=True),
          fact('proposal','Automatic Git publication and mandatory CI remain deferred proposals despite the later demonstration note; retain operator-effort/revision rationale.', ['evidence/01-design.txt','evidence/02-owner.txt','evidence/05-demo.txt'],critical=True),
          fact('configured',f'Checked-in timeout is {45 if final else 60} seconds, supported by config/service.yaml.', ['config/service.yaml']),
          fact('runtime','Production timeout and deployed state are unknown; local build/staging receipt do not establish production.', ['evidence/06-build.txt']+(['evidence/07-update.txt'] if final else []),critical=True),
          fact('closed_work','REST-101 is closed after sparse volume allocation and passing synthetic restore, September 25 receipt restore-25.' if final else 'REST-101 remains blocked on volume allocation; operator must request volume and run/record the exercise.', ['evidence/07-update.txt'] if final else ['evidence/04-work.txt']),
          fact('open_work','CAL-102 remains open; ask the test maintainer for an approved leading-zero sensor sample.', ['evidence/04-work.txt']+(['evidence/07-update.txt'] if final else [])),
          fact('constraint','Preserve the sparse-file flag and ./data files/pilot.db path; consult storage maintainer; the constraint survives closure of REST-101.', ['scratch/operator.txt'],critical=True),
          fact('boundary','DEC-102 permits only approved sample manuals; public/customer uploads and external ingestion need agreement on rights/update ownership and are not approved.', ['evidence/02-owner.txt'],critical=True),
          fact('unknown_owner','Production on-call owner is unassigned/unknown; do not infer that Mira holds that role.', ['evidence/04-work.txt']+(['evidence/07-update.txt'] if final else []),critical=True),
        ]
    return [
      fact('workflow','CSV plus optional local JSON is approved by Lina / DEC-203 for downstream offline analysis; offline/read-only boundaries survive.' if final else 'Offline read-only CSV reports are approved by Lina / DEC-201 because operators work disconnected; JSON is not yet approved.', ['evidence/07-update.txt','evidence/02-owner.txt'] if final else ['evidence/02-owner.txt','evidence/05-proposal.txt'],critical=True),
      fact('proposal','Hosted viewer remains unapproved despite a newer demo; shared review is its rationale and a demo is not owner authority.', ['evidence/05-proposal.txt','evidence/02-owner.txt'],critical=True),
      fact('configured',f'Checked-in batch limit is {125 if final else 200} rows, supported by config/report.yaml.', ['config/report.yaml']),
      fact('runtime','Running installation batch limit/state are unknown; a local tiny-fixture test or code configuration does not establish them.', ['evidence/06-check.txt']+(['evidence/07-update.txt'] if final else []),critical=True),
      fact('closed_work','SAMPLE-201 is closed after creation of synthetic duplicate-location input and passing D201.' if final else 'SAMPLE-201 remains open; request a synthetic same-item/two-location export and run its comparison.', ['evidence/07-update.txt'] if final else ['evidence/04-work.txt']),
      fact('open_work','ENC-202 remains open; request an approved non-ASCII location sample from the test maintainer.', ['evidence/04-work.txt']+(['evidence/07-update.txt'] if final else [])),
      fact('constraint','DEC-202 uses both item_id and location_id as opaque strings; preserve case/leading zeros to avoid merging distinct locations or records.', ['evidence/02-owner.txt','scratch/reviewer.txt'],critical=True),
      fact('boundary','A blank quantity is unknown, not zero; reports do not approve upstream corrections and inputs remain read-only.', ['evidence/02-owner.txt','evidence/03-usage.txt','scratch/reviewer.txt'],critical=True),
      fact('unknown_owner','Warehouse correction approver is unidentified; Lina tool-design authority must not be treated as ledger-correction authority.', ['evidence/04-work.txt']+(['evidence/07-update.txt'] if final else []),critical=True),
    ]


QUESTIONS = {
 'kestrel': [
  ('q1',['workflow','proposal'], 'Which publication workflow applies now, who approved it and why, and does the later Git demonstration change that?', 'What should the next operator use to publish, on whose authority and rationale? Explain the standing of automated Git publication.'),
  ('q2',['configured','runtime'], 'What timeout is configured, and what timeout is established for production?', 'State the repository timeout and separately what the evidence proves about the running production timeout.'),
  ('q3',['closed_work','open_work'], 'Which of REST-101 and CAL-102 is closed, what supports closure, and what work remains with its next action?', 'Describe the current restore and calibration ticket states, the evidence for completed work and the next step for unfinished work.'),
  ('q4',['constraint'], 'What restore-fixture constraint must survive the completed exercise, including the path and who to consult?', 'Before another restore exercise, what path and allocation property must be preserved, and whom should the operator consult?'),
  ('q5',['boundary'], 'May the pilot ingest public/customer uploads or external manuals? Explain the approved boundary and what prevents expansion.', 'Which manual sources are authorized for this pilot, and what is the status and unresolved prerequisite of broader ingestion?'),
  ('q6',['unknown_owner'], 'Who is the assigned production on-call owner?', 'Whom do the supplied project records establish as responsible for production on-call coverage?'),
 ],
 'oriole': [
  ('q1',['workflow','proposal'], 'Which report formats and operating boundaries are approved now, by whom and why, and is the hosted viewer approved?', 'What output workflow can the pilot use on current owner authority and rationale? Distinguish the viewer proposal from approved scope.'),
  ('q2',['configured','runtime'], 'What batch limit is configured, and what batch limit is established for a running installation?', 'State the repository batch size and separately what the evidence proves about actual running installations.'),
  ('q3',['closed_work','open_work'], 'Which of SAMPLE-201 and ENC-202 is closed, what supports closure, and what work remains with its next action?', 'Describe the current duplicate-location and encoding test work: completed evidence, remaining blocker and next step.'),
  ('q4',['constraint'], 'How are records matched and identifiers preserved, and why would item-only numeric matching be wrong?', 'What key and normalization rules apply to identifiers, and which data loss do they prevent?'),
  ('q5',['boundary'], 'How should a blank quantity be interpreted, and may a discrepancy report authorize changes to the source exports?', 'What do missing quantities mean, and what authority does the tool have to alter either input ledger?'),
  ('q6',['unknown_owner'], 'Who is authorized to approve actual warehouse ledger corrections?', 'Which person do the supplied records establish as the approver of changes to warehouse ledger data?'),
 ],
}


def docs_for(world, condition):
    w = WORLDS[world]
    readme = f"# {w['title']}\n\n{w['purpose']}\n\nRaw project/work evidence is in `evidence/`, configuration in `config/`, and uncommitted work notes in `scratch/`.\n"
    if condition == 'absent':
        return {'README.md': readme}
    if world == 'kestrel':
        scattered = {
         'notes/release.md': '# Publication notes\n\nMira approved manual publication with optional CI to review each artifact (DEC-101). Automation remains deferred to reduce operator work later.\n',
         'notes/status.md': '# Working state\n\nTimeout is configured to 30 seconds. Production timeout has not been checked. REST-101 awaits a test volume; operator must request it and run the exercise. CAL-102 awaits a leading-zero sample from the test maintainer.\n',
         'notes/boundaries.md': '# Content boundary\n\nDEC-102 permits approved sample manuals only. Broader uploads/ingestion still need agreement on rights and update ownership.\n',
         'notes/operations.md': '# Operator fragments\n\nKeep the last accepted artifact until replacement acceptance. Keep preview reviews tied to their actual artifact revision. Production on-call ownership remains unassigned.\n',
        }
        conflict = {
         'notes/release.md': '# Release procedure\n\nPublish automatically on every main-branch push after required CI. September 20 demonstration establishes this as the current policy.\n',
         'notes/status.md': '# Current status\n\nProduction uses a 30-second timeout. Both REST-101 and CAL-102 are complete. Mira is production on-call.\n',
         'notes/boundaries.md': '# Content scope\n\nPublic uploads and external manuals are approved.\n',
         'notes/operations.md': '# Design history\n\nSeptember 8 owner note: manual publication allowed artifact review with optional CI. Automation was deferred to reduce pilot setup. Keep earlier accepted artifacts and revision-specific preview reviews.\n',
        }
    else:
        scattered = {
         'notes/release.md': '# Report notes\n\nLina approved offline read-only CSV for disconnected operators (DEC-201). A hosted viewer and JSON remain proposals; the viewer is meant to ease shared review.\n',
         'notes/status.md': '# Working state\n\nBatch size is configured to 100 rows; installation state has not been verified. SAMPLE-201 needs a synthetic two-location input and comparison. ENC-202 needs a non-ASCII sample from the test maintainer.\n',
         'notes/boundaries.md': '# Matching details\n\nDEC-202 matches item_id and location_id as opaque strings, preserving case and leading zeros so distinct records are not merged. Blank quantities mean unknown.\n',
         'notes/operations.md': '# Operator fragments\n\nKeep exports until report review. Preserve left-side field order and append right-only fields in their original order. The warehouse correction approver remains unknown; tool-design authority is separate.\n',
        }
        conflict = {
         'notes/release.md': '# Current output\n\nThe hosted browser viewer is approved because its newer mockup works. CSV is the only output we will ever support.\n',
         'notes/status.md': '# Current status\n\nRunning installations use 100-row batches. SAMPLE-201 and ENC-202 are complete. Lina approves warehouse corrections.\n',
         'notes/boundaries.md': '# Matching procedure\n\nMatch numeric item_id alone and convert blank quantities to zero. The report authorizes correcting source exports.\n',
         'notes/operations.md': '# Earlier rationale\n\nSeptember 7 owner note: offline CSV accommodated disconnected operators, and opaque composite identifiers prevented record merging. Keep exports until report review and preserve left-field order before right-only fields.\n',
        }
    files = scattered if condition == 'scattered' else conflict
    # Same four files in both layouts; no privileged initial source content.
    return {'README.md':readme+'\nWorking documentation is in `notes/`; it has no maintained index.\n', **files}


def reference_docs(world, condition, stage):
    files = docs_for(world, condition)
    facts = ledger(world, stage)
    details = '# Project context\n\n' + WORLDS[world]['purpose'] + '\n\n'
    for f in facts:
        details += f"## {f['id'].replace('_',' ')}\n\n{f['expected']}\n\nSources: " + ', '.join(f'[{p}]({p})' for p in f['sources']) + '.\n\n'
    # Preserve useful extra operational details, not just benchmark answer facts.
    extra = ('Keep the last accepted artifact until replacement acceptance; do not rebuild it from a newer revision. Preview links and review results stay tied to the reviewed artifact revision. Receipt storage remains undecided.' if world=='kestrel' else 'Keep inputs until report review, refuse output over an input, preserve left-field order followed by right-only fields, and do not automatically deduplicate item identifiers.')
    details += '## Operational details\n\n'+extra+'\n'
    files['context.md'] = details
    files['README.md'] = files['README.md'].split('\nWorking documentation')[0] + '\nStart with [project context](context.md).\n'
    for path in list(files):
        if path.startswith('notes/'):
            files[path] = '# Historical working notes\n\nEarlier working claims are superseded by the evidence-backed [current context](../context.md). Useful rationale and operational constraints are retained there; original dated evidence remains in `../evidence/`.\n'
    return files


CONDITIONS = ('scattered','conflicting','absent')
ARMS = ('untreated','ordinary','skill')
CASES = []
for world,w in WORLDS.items():
    for condition in CONDITIONS:
        files = {**w['sources'], **docs_for(world,condition)}
        steps=[]
        for stage in range(3):
            request = ('Prepare reliable project documentation for someone continuing this work. Update or establish context from supplied project/work evidence, reconcile supported inconsistencies, and preserve useful decisions, rationale, constraints and unresolved work. Make the maintained record discoverable without imposing a new layout.' if stage==0 else
                       'New project/work evidence is now present. Update the existing documentation to reflect supported changes while preserving useful knowledge and decision status.' if stage==1 else
                       'No project evidence, decisions or status changed after the previous pass. Review the maintained record and edit only for a concrete remaining defect; avoid bookkeeping-only edits.')
            steps.append(dict(request=request, updates=w['updates'] if stage==1 else {}, oracle=reference_docs(world,condition,stage), rubric=[f['expected'] for f in ledger(world,stage)]))
        CASES.append(dict(id=world+'-'+condition, world=world, condition=condition, files=files, uncommitted=w['uncommitted'], steps=steps, protected=[], immutable=[]))


def materialized(case, stage):
    files={**case['files'],**case['uncommitted']}
    if stage>0: files.update(WORLDS[case['world']]['updates'])
    return deepcopy(files)
