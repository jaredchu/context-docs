# Verify and record the a441129 website deployment

## Scope

Verify the existing automatic deploy from `a441129` and bring the
[deployment record](../../site/README.md#latest-deployment) up to date. The
[Landing page run](https://github.com/jaredchu/context-docs/actions/runs/45480049082)
reported a successful deploy, and two live pages returned HTTP 200. This ticket
covers read-side verification and local documentation.

## Done when

- The CI artifact and build and deploy manifests match a build from the exact
  deployed source, accounting for the empty `.nojekyll` marker.
- Canonical live responses match the artifact, with any differences explained
  and bounded by the [deployment checklist](../../site/README.md#deployment-checklist).
- The public deployment record and its project-context pointer identify the
  verified source. Preserve the earlier receipt and pass repository static checks.

## Status

Closed on November 25, 2026.

## Outcome

The [deployment receipt](../../site/README.md#latest-deployment) records the
artifact, CI manifest and live HTTPS comparisons. The [earlier receipt](../../site/README.md#earlier-antigravity-label-deployment)
is preserved. The project context now points to the verified source, and the
progress view's active ticket link was removed on closure.

## Handoff check

Two fresh, read-only Codex CLI sessions got the same prompt and started at
the [progress view](../project-context.md#current-focus). Both followed the
link to this ticket. The view stayed the same between sessions.

1. The first session identified the unverified CI artifact and job manifests as
   the blocker and called for comparing them with a pinned build. It repeated
   the ticket's incorrect artifact name, `public-site`. The
   [workflow](../../.github/workflows/site.yml) names it `site-dist`.
2. After the 19-file artifact comparison passed, the second session identified
   unverified live response contents as the new blocker. It proposed fetching
   the canonical HTTPS responses and comparing them with `site-dist`, allowing
   for the documented analytics beacon and holding the record update for any
   unexplained difference. It needed no follow-up prompt.
