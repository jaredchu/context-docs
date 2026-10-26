# Local timeout check

Synthetic observation on October 22, 2026; supplied evidence, not a command for
the documentation agent to execute.

- Input: [worker configuration](../config/worker.json), timeout 30 seconds and
  retry limit two.
- Result: the isolated timeout configuration check passed for one example job.
- Not checked: retry-limit behavior, restore compatibility or the full test suite.
- No deployment occurred and no staging or production behavior was observed.

This report supports the limited local check only. Configuration values describe
the checked local input, not any deployed worker.
