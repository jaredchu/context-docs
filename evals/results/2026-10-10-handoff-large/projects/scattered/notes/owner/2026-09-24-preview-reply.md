# Reply — project owner Mira, September 24
Ship the --limit option, but keep the arrival order. Consumers interpret arrival
order as priority; sorting by id would silently change which job they see first.
Do not use the sorting or early-stop parts of Dev's September 21 design. Load
and validate the entire input before choosing the preview. We need to catch
corrupt later records even when the limit is zero or already satisfied.
The limit is a nonnegative integer, defaults to absent, and limits the selected
records rather than raw input lines. Zero emits nothing; excess emits all selected
records. Reject negative or noninteger values with the usual argparse error.
Keep the input file untouched. No queue merging is part of this task.
