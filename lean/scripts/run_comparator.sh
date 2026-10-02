#!/usr/bin/env bash
# Run leanprover/comparator on this package. It checks that the theorems listed in comparator.json, proved in
# Kissing/Solution.lean, have the same statements as the sorry'd ones in Kissing/Statement.lean, use only propext,
# Quot.sound and Classical.choice, and are accepted by the Lean kernel (replayed from a lean4export dump).
# Needs a workspace prepared by ./regen.sh and `lake exe cache get`, and the comparator and lean4export binaries
# (COMPARATOR_BIN, COMPARATOR_LEAN4EXPORT; pins as in huwngtran/thomson-n7-lean's verification record:
# comparator fd5d5bc, lean4export 076e8e5). Comparator runs the solution under `landrun` (Linux Landlock); if
# COMPARATOR_LANDRUN is unset and `landrun` is not on PATH, Comparator's non-sandboxing shim scripts/fake-landrun.sh
# is used and a warning is printed.
# Adapted from ComparatorChallenges/run_comparator.sh of huwngtran/thomson-n7-lean.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
: "${COMPARATOR_BIN:?set COMPARATOR_BIN}"; : "${COMPARATOR_LEAN4EXPORT:?set COMPARATOR_LEAN4EXPORT}"
export COMPARATOR_LEAN4EXPORT LAKE_ARTIFACT_CACHE=false
if [ -z "${COMPARATOR_LANDRUN:-}" ]; then
  if command -v landrun >/dev/null 2>&1; then COMPARATOR_LANDRUN="$(command -v landrun)"
  else COMPARATOR_LANDRUN="$(dirname "$(dirname "$(dirname "$(dirname "$COMPARATOR_BIN")")")")/scripts/fake-landrun.sh"
       echo "WARNING: no landrun found, using the non-sandboxing shim $COMPARATOR_LANDRUN" >&2; fi
fi
export COMPARATOR_LANDRUN
mkdir -p logs
/usr/bin/time -p lake env "$COMPARATOR_BIN" comparator.json 2>&1 | tee logs/comparator.log
echo "COMPARATOR EXIT: ${PIPESTATUS[0]}"
