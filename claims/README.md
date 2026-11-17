# Claims

One file per package being traced, `PREFIX.md`, written by `tools/claim.py take` and
pushed straight to main, so that everyone sees who is working where. Do not edit these
files by hand. `tools/claim.py list` shows them with each branch's last commit.

The coordinator removes a claim when it merges the work; its owner removes it with
`tools/claim.py release` if the work is abandoned. How work is shared: `notes/workflow.md`.
