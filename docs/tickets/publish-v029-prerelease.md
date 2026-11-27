# Publish v0.2.9 and switch the install pins

## Scope

Publish the verified experimental bundle, update current install instructions,
and verify the resulting CI, automatic website deployment and skills.sh listing.
Confirm that release and site publication fall within the owner's authorization
before acting on this ticket.

## Done when

- The GitHub prerelease names the tag commit and both package versions. The tag
  contains the release preparation notes, and its 13 skill package files match
  the verified `45557cf` package files.
- The README, guide, website and tests agree on the published install pins. The
  changelog, release index and context show the published disposition.
- The deployment and isolated skills.sh install/listing comparisons are recorded,
  including any limits of the public listing refresh.

## Status

Completed 2026-11-25. [v0.2.9](https://github.com/jaredchu/context-docs/releases/tag/v0.2.9)
is published from `3337eb9`. The [website deployment](../../site/README.md#v029-install-pin-deployment)
verified the install pins from `9008ac6`. Both archives and the isolated install
matched the 13 verified package files. Both skills.sh listings still showed
earlier text at the final check.
See the [verification record](../releases/v0.2.9.md#publication-and-upgrade-verification).
