#!/bin/bash
# Run a tool for one block:   tools/t.sh BLOCK tool.py [args ...]
# Sets TRACE=BLOCK (unless TRACE is already set, e.g. TRACE=blk,other tools/t.sh blk ...)
# and puts scratch output in cache/scratch/BLOCK/. A bare --out name lands there.
cd "$(dirname "$0")/.." || exit 1
blk="$1"; shift
export TRACE="${TRACE:-$blk}"
export HD_SCRATCH="cache/scratch/$blk"
mkdir -p "$HD_SCRATCH"
tool="$1"; shift
exec .venv/bin/python "tools/$tool" "$@"
