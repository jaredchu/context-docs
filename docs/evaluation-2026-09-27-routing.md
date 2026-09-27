# README routing and verified reading — September 27, 2026

The follow-up completed **12 fresh sessions and 72 answers**. All eight readers
given handoffs received the full document in model-visible tool responses before
answer-writing. All 72 answers meet the unchanged required criteria and source
support checks. **No Context Docs accuracy advantage was observed.**

| Reader mode and outcome | Upstream orientation | Ordinary handoff | Context Docs handoff |
| --- | ---: | ---: | ---: |
| README-first discovery: supported answers | 12/12 | 12/12 | 12/12 |
| README-first discovery: full orientation text exposed | 1/2 | 2/2 | 2/2 |
| Directed reading: supported answers | 12/12 | 12/12 | 12/12 |
| Directed reading: full orientation text exposed | 2/2 | 2/2 | 2/2 |

Both methods' handoffs were fully exposed in all four README-first discovery
sessions, without an explicit requirement to follow the link. Directed reading
also exposed all four handoffs and both upstream documentation indexes. Every
reader received the full README. The only orientation target not fully exposed
was Click's index in README-first discovery; that reader still answered correctly
from original sources and stays in the denominator.

## What changed and what it means

The [previous pilot](evaluation-2026-09-27-public.md) found no handoff-content
reading in eight readers. This follow-up changed **both** the temporary README
routing and the reader's entry instructions. It does not isolate the effect of a
link alone, provide a randomized contemporaneous comparison with the earlier
setup, or prove agents will discover context without guidance.

The previous ordinary Flask answer omitted safe handling of a connection that
was never created. Both new ordinary readers include the missing-resource guard,
as do all other Flask readers. The original handoff already contained it and was
not edited. This is a successful known-case repeat, not evidence that Context
Docs outperforms ordinary maintenance or that reading caused that one correction.

The practical setup is clearer: **link context from a known project entry point,
and start fresh sessions there**. When it matters that the context was read, ask
for the linked document to be read before work. README usage guidance now says
this explicitly. The installable skill and canonical standard remain unchanged;
the skill already asks initialization to create this link.

The next useful quality evaluation should use independently authored project
decisions and changing constraints across sessions—knowledge that cannot always
be recovered from code alone. Retain equal access to source evidence and measure
preservation, contradictions and supported future answers. More runs of these
already searchable questions are unlikely to resolve the accuracy question.
That next design is proposed, not evidence produced by this study.

## Design and scope

The [protocol](../evals/routing/README.md), prompts, exposure detector and report
aggregator were frozen in `a02cade` before the scored packages were built.
This reuses the four actual handoffs from the prior study, without correcting,
regenerating or shortening them. The skill remains v0.1.1.

Each temporary README gets the same `Contributor orientation` heading and
`Project orientation` link, placed before the original content. The link points
to the existing upstream documentation index or the applicable handoff. All other
source and handoff bytes remain unchanged; original upstream clones are untouched.
The harness adds these links. This does not measure whether a maintainer creates
the routing correctly. The [skill already instructs initialization](../skills/context-docs/SKILL.md) to
link the context entry point from a README or documentation index; the earlier pilot's
preservation constraint had prohibited that edit.

Two modes × two projects × three artifacts = **12 fresh sessions, 72 answers**:

- **README-first discovery:** read README, then choose relevant sources. Following
  the orientation link is optional. This is not completely unguided discovery.
- **Directed reading:** read README, follow its orientation link and read the whole
  target before answering, then check relevant sources.

Within a mode, the same prompt applies to all three conditions; only project
questions differ. All readers can inspect the same complete upstream text sources.
No skills, previous conversation, condition labels or answer key are supplied.
Both modes reuse the second question phrasing, including the prior omission case.
This is not held-out evaluation, and its aggregate is not directly comparable to
the earlier study's two-phrasing result. One sample per project/arm/mode is small.

The setup reuses Harbor 0.23.0, Codex CLI 0.158.0-alpha.2, gpt-6-astra with low
effort, concurrency three, a 480-second session limit and no retries. Raw sources
are pinned Flask 3.1.1 and Click 8.2.1, the same two familiar Pallets projects as
before. No upstream execution, dependency installation or external search is
part of the agent task. Timing and tokens are retained as secondary diagnostics.

## What verified exposure means

The detector reads **model-visible tool responses** in session JSONL rather than
unfiltered shell logs, which may include text truncated before reaching the model.
Every distinct nonblank line of the target must appear in visible responses
before the first tool call mentioning the answer file. Split reads are accepted.
A filename listing, heading, partial excerpt, citation or agent self-report does
not suffice. Whitespace is stripped at line edges; unrecognized formatting and
early answer-file preparation can cause conservative false negatives.

This verifies displayed text, not comprehension, reliance, trustworthiness or a
causal improvement. Answer quality is judged separately using the unchanged
required criteria and source support. All assigned readers remain in the accuracy
denominator whether or not exposure is verified. The upstream target is a short
navigation index, not an equivalent synthesized handoff; its exposure score is
an orientation control, not a stored-knowledge coverage score.

The exact answers, author reviews, input/source hashes, README prefixes, exposure
line counts/missing-line indices and source-call evidence are available in the
[evidence directory](../evals/results/2026-09-27-routing/README.md). Raw sessions
remain local due to service metadata. This is inspectable evidence, not a
cryptographically trusted trace of model understanding.

## Validation and interpretation limits

Before scored runs, two reference controls passed and two no-op controls failed
as expected. All 2300 generated package files match between controls and scored
runs. Nine exposure controls cover listing/partial/split/full text, nested output
decoding and answer ordering. The decoder also recognizes a complete known
source document in an earlier real model-visible session. Report controls verify
that exposure is not mistaken for correctness, and omissions, unsupported claims,
material errors and execution failures affect answer scores correctly.

All 12 sessions passed project/Git preservation, answer schema, citation-path and
recorded-input isolation checks. No unexpected user/global AGENTS instructions,
execution exceptions, timeouts, retries or discarded scored runs were observed.
Frozen harness and artifact hashes still match, and all answer outputs are
published unchanged. The table reproduces from the explicit reviews and exposure
records. Semantic correctness is author-reviewed, not a mechanical reward.

Questions and review are by the authoring agent, not independent or blinded.
The same four maintained artifacts and familiar public questions are reused.
The source-only condition already performed well, leaving limited scope to show
an accuracy gain. No significance, equivalence, general accuracy, automatic skill
selection or long-term retention claim follows from this small comparison. Prior
results, their exact omission and the earlier private-project miss remain visible.
