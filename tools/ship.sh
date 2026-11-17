#!/bin/bash
# Commit and push some files:   tools/ship.sh "commit message" file [file ...]
# The only way anyone commits trace work. It commits exactly the named files (nothing
# else that happens to be modified), under a lock so that two ships in one repository
# cannot interleave, refuses trace files that do not parse, and pushes the current branch.
# Work happens on a branch named for the claimed package (notes/workflow.md); committing
# on main is the coordinator's alone, and needs HD_COORD=1.
cd "$(dirname "$0")/.." || exit 1
if [ $# -lt 2 ]; then echo "usage: tools/ship.sh \"message\" file [file ...]"; exit 2; fi
branch=$(git symbolic-ref --short HEAD 2>/dev/null) || { echo "ship: not on a branch"; exit 2; }
if [ "$branch" = main ] && [ -z "$HD_COORD" ]; then
  echo "ship: you are on main. Work on your package's branch (tools/newwork.sh PREFIX);"
  echo "      only the coordinator commits on main (HD_COORD=1)."; exit 2
fi
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
exec 9>"$(git rev-parse --git-common-dir)/ship.lock"
flock -w 900 9 || { echo "ship: could not get the lock"; exit 1; }
git add -- "$@" || exit 1
if git diff --cached --quiet -- "$@"; then echo "ship: nothing to commit"; exit 0; fi
git commit -q -m "$msg" -- "$@" || { echo "ship: commit failed"; exit 1; }
for i in 1 2 3 4; do
  if git push -q -u origin "$branch" 2>/dev/null; then echo "ship: pushed $(git log --oneline -1) to $branch"; exit 0; fi
  # rejected: someone else pushed to this branch (on main: a claim). Rebase once onto it.
  if [ "$i" = 1 ] && git pull -q --rebase --autostash origin "$branch" 2>/dev/null; then continue; fi
  sleep $((i * 8))
done
echo "ship: committed locally ($(git log --oneline -1)); push failed and will go out with the next ship"
exit 0
