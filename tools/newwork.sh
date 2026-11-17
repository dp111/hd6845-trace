#!/bin/bash
# Start work on a claimed package in a worktree of its own:   tools/newwork.sh PREFIX [DIR]
# Creates branch PREFIX from the shared repository's main in DIR (default: a sibling
# directory hd6845-trace-PREFIX), links cache/ and .venv/ from this checkout (they are
# not in git and cache/ is about 10 GB), and pushes the branch so others see it.
# Use one worktree per agent: several agents in one working tree overwrite each other.
cd "$(dirname "$0")/.." || exit 1
p="$1"; [ -n "$p" ] || { echo "usage: tools/newwork.sh PREFIX [DIR]"; exit 2; }
git fetch -q origin || exit 1
claim=$(git show "origin/main:claims/$p.md" 2>/dev/null) \
  || { echo "newwork: $p is not claimed on origin/main; run tools/claim.py take first"; exit 2; }
owner=$(printf '%s\n' "$claim" | sed -n 's/^| Who | \(.*\) |$/\1/p')
me=$(gh api user -q .login 2>/dev/null || git config user.name)
[ "$owner" = "$me" ] || { echo "newwork: $p is claimed by $owner, not by you ($me)"; exit 2; }
# A branch of this name from an earlier, merged run is fine (main fast-forwards over it);
# one that is not merged is someone's unfinished work: stop rather than build beside it.
if git rev-parse -q --verify "origin/$p" >/dev/null && ! git merge-base --is-ancestor "origin/$p" origin/main; then
  echo "newwork: origin/$p exists and is not merged into main: resume it (git worktree add DIR $p) or ask its owner"; exit 2
fi
dir="${2:-$(cd .. && pwd)/hd6845-trace-$p}"
git worktree add -q -b "$p" "$dir" origin/main || exit 1
ln -s "$PWD/cache" "$dir/cache"
ln -s "$PWD/.venv" "$dir/.venv"
(cd "$dir" && git push -q -u origin "$p") && echo "newwork: $dir on branch $p (pushed)"
