# Verification records

Release check of `lean/` exactly as published (every `.lean` file and the Lake configuration byte-identical; sha256 in
`files.sha256`), 2026-10-02/03, Linux x86_64, Lean v4.34.1, in two fresh copies of the package, each prepared with
`regen.sh` (`regen.out`: the eight imported upstream-derived modules match `generated.sha256`) and
`lake exe cache get` (Mathlib from the cache).

| file | content |
|---|---|
| `build_test.tsv` | first copy: `scripts/build_test.sh`, the 41 modules reachable from `Kissing.Statement`, `Kissing.Solution` and `Kissing.Axioms` (eight of them regenerated upstream modules), each compiled one at a time in dependency order (`lean -j1`), wall time and peak resident memory (KiB) per module, all exit 0; then `#print axioms` |
| `comparator.out` | second copy: `scripts/run_comparator.sh`, a `lake build` of `Kissing.Statement` and `Kissing.Solution` from scratch, lean4export, "Lean default kernel accepts the solution", "Your solution is okay!", exit 0, for the six theorems of `lean/comparator.json`; Comparator step 26.3 min wall |
| `axioms.out` | `#print axioms`: `[propext, Classical.choice, Quot.sound]` for all six (the same output in both copies) |
| `files.sha256` | sha256 of the Lean files present in the checked copies and the Lake configuration (`regen.sh` writes all split modules; eight of them are imported) |
| `regen.out` | output of `regen.sh` |
| `scan_upstream.txt` | `lean/ThomsonGen/scripts/scan_upstream.py` (default selection: the 33 stored Lean files under `lean/Kissing/`): 0 verbatim, all near-copies attributed |
| `time.txt` | GNU time of the whole check (both copies, including waiting for an idle machine): peak resident memory of any single process 9281496 KiB (8.85 GiB) |

Comparator ran with its non-sandboxing shim `fake-landrun.sh`, because `landrun` was not available on the machine.
Tool revisions and binary sha256: `lean/scripts/tools.sh`.
