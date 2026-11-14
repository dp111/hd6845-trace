#!/bin/bash
# Coordinator's overview: what each block has on disk and how it extracts.
cd "$(dirname "$0")/.." || exit 1
printf '%-10s %7s %6s %6s %5s  %s\n' block shapes trans errors open "notes / floorplan"
for f in trace/*.txt; do
  b=$(basename "$f" .txt)
  r=$(TRACE="$b" .venv/bin/python tools/netlist.py 2>&1)
  head1=$(echo "$r" | head -1)
  if echo "$head1" | grep -q transistors; then
    tr=$(echo "$head1" | sed -E 's/.* ([0-9]+) transistors.*/\1/'); er=$(echo "$head1" | sed -E 's/.* ([0-9]+) errors.*/\1/')
  else tr='-'; er='PARSE'; fi
  op=$(echo "$r" | awk '/^unnamed open nets/{f=1;next} f&&/^  /{n++} END{print n+0}')
  sh=$(grep -c -E '^\??[MPDCBA] ' "$f")
  extra=""; [ -f "notes/blocks/$b.md" ] && extra="notes($(wc -l < notes/blocks/$b.md)) "; [ -f "floorplan.d/$b.txt" ] && extra="$extra fp($(grep -c -v '^#' floorplan.d/$b.txt))"
  printf '%-10s %7s %6s %6s %5s  %s\n' "$b" "$sh" "$tr" "$er" "$op" "$extra"
done
echo "all files together: $(.venv/bin/python tools/netlist.py 2>&1 | head -1)"
git log --oneline | head -5 | cat
