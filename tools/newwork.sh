#!/bin/bash
# Start work on a claimed package in a worktree of its own:   tools/newwork.sh PREFIX [DIR]
# Creates branch PREFIX from the shared repository's main in DIR (default: a sibling
# directory hd6845-trace-PREFIX), links cache/ and .venv/ from this checkout (they are
# not in git and cache/ is about 10 GB), and pushes the branch so others see it.
# Use one worktree per agent: several agents in one working tree overwrite each other.
cd "$(dirname "$0")/.." || exit 1
p="$1"; [ -n "$p" ] || { echo "usage: tools/newwork.sh PREFIX [DIR]"; exit 2; }
git fetch -q origin || exit 1
git show "origin/main:claims/$p.md" >/dev/null 2>&1 \
  || { echo "newwork: $p is not claimed on origin/main; run tools/claim.py take first"; exit 2; }
dir="${2:-$(cd .. && pwd)/hd6845-trace-$p}"
git worktree add -q -b "$p" "$dir" origin/main || exit 1
ln -s "$PWD/cache" "$dir/cache"
ln -s "$PWD/.venv" "$dir/.venv"
(cd "$dir" && git push -q -u origin "$p") && echo "newwork: $dir on branch $p (pushed)"
