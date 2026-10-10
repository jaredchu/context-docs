# Selection sequence — maintainer Jo, September 25
Mira's preview reply means --limit applies after the existing tenant selection
and stable first-occurrence deduplication. Selecting two raw records can produce
only one selected record when the first two share an identity. Selecting before
tenant filtering can similarly consume the quota with another tenant's rows.
Route the CLI option through service.execute into selection.select. Keep loader,
validation and render semantics unchanged; full loading precedes selection.
Without a limit, the result remains exactly the current formatter output.
