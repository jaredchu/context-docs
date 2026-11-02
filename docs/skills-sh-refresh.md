# skills.sh metadata refresh

The [GitHub Actions workflow](../.github/workflows/skills-sh-refresh.yml) runs daily
at 02:17 UTC (09:17 in Vietnam), with a manual **Run workflow** trigger. GitHub
may delay scheduled jobs or disable schedules after 60 days without repository
activity. It runs only in `jaredchu/context-docs`.

The job checks both skill pages against a GitHub star-count snapshot first and
skips installation when both already agree. Otherwise, it installs both skills
from the public default branch once into a temporary runner project using
`skills@1.7.4`, with npm lifecycle scripts disabled. The CLI version is fixed;
npm resolves its dependency versions at run time.
CLI telemetry is enabled and truthfully marked as CI. The CLI installation is the
refresh trigger; merely visiting the listing does not trigger the repository check.
See the [skills.sh refresh documentation](https://www.skills.sh/docs/customize#when-changes-appear).

The job then checks both public skill pages against that GitHub snapshot. A star
change after the refresh does not move this target; a change between the snapshot
and the refresh can cause a false failure that a rerun resolves.
It retries reads for a bounded interval without repeating the installation, and
fails if either page remains stale or cannot be checked. Compact labels are
compared at their displayed precision. It uses the built-in read-only GitHub token;
no additional secret, agent subscription or model call is needed.

On November 2, 2026, an isolated CI-marked installation returned exit zero and its
original telemetry request returned HTTP 200. Both canonical skill pages then
changed from **2** stars to **194**, agreeing with GitHub; page responses reported
revalidation, and a fresh route also showed 194. Search install counts remained
2 per skill. Existing installed files and repository files were unchanged during
that refresh. The maintainer retains the private operator receipt under evidence
ID `skills-sh-refresh-2026-11-02`.

This verifies that one refresh updated the displayed star metadata. It does not
establish future refresh reliability, independent adoption, install attribution,
supporting-file freshness or audit reruns. This workflow is separate from the
[release content verification](../CONTRIBUTING.md#release-checklist).
