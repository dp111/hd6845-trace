#!/bin/bash
# Commit and push some files:   tools/ship.sh "commit message" file [file ...]
# The only way anyone commits while several agents share this working tree. It commits
# exactly the named files (nothing else that happens to be modified), under a lock so
# that two ships cannot interleave, and refuses trace files that do not parse.
cd "$(dirname "$0")/.." || exit 1
if [ $# -lt 2 ]; then echo "usage: tools/ship.sh \"message\" file [file ...]"; exit 2; fi
msg="$1"; shift
for f in "$@"; do
  [ -e "$f" ] || { echo "ship: no such file: $f"; exit 2; }
  case "$f" in
    trace/*.txt)
      b="${f#trace/}"; b="${b%.txt}"
      if ! out=$(TRACE="$b" .venv/bin/python tools/netlist.py 2>&1 | head -3); then :; fi
      if ! TRACE="$b" .venv/bin/python -c "import sys; sys.path.insert(0,'tools'); import tracelib; tracelib.Trace()" 2>/tmp/ship_err_$$; then
        echo "ship: $f does not parse, not committed:"; tail -2 /tmp/ship_err_$$; rm -f /tmp/ship_err_$$; exit 3
      fi
      rm -f /tmp/ship_err_$$
      echo "ship: $f: $(echo "$out" | head -1)"
      ;;
  esac
done
exec 9>.git/ship.lock
flock -w 900 9 || { echo "ship: could not get the lock"; exit 1; }
git add -- "$@" || exit 1
if git diff --cached --quiet -- "$@"; then echo "ship: nothing to commit"; exit 0; fi
git commit -q -m "$msg" -- "$@" || { echo "ship: commit failed"; exit 1; }
for i in 1 2 3 4; do
  if git push -q origin main 2>/dev/null; then echo "ship: pushed $(git log --oneline -1)"; exit 0; fi
  sleep $((i * 8))
done
echo "ship: committed locally ($(git log --oneline -1)); push failed and will go out with the next ship"
exit 0
