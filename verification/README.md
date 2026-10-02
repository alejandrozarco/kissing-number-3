# Verification records

Clean check of `lean/` at development revision `78bb32f`, 2026-10-02, Linux x86_64, Lean v4.34.1: a fresh copy of
the package, `regen.sh` (`regen.out`: the eight upstream-derived modules match `generated.sha256`),
`lake exe cache get`, then `scripts/run_comparator.sh` and `lake env lean Kissing/Axioms.lean`.

| file | content |
|---|---|
| `comparator.out` | full `lake build` of `Kissing.Statement` and `Kissing.Solution` from scratch (Mathlib from the cache), lean4export, "Lean default kernel accepts the solution", "Your solution is okay!", exit 0, for the six theorems of `lean/comparator.json` |
| `axioms.out` | `#print axioms`: `[propext, Classical.choice, Quot.sound]` for all six |
| `files.sha256` | sha256 of the Lean files present in the checked copy and the Lake configuration (`regen.sh` writes all split modules; eight of them are imported) |
| `time.txt` | resource use of the whole check (GNU time): 45.5 min wall, peak resident memory 9.4 GB |
| `regen.out` | output of `regen.sh` |
| `scan_upstream.txt` | `lean/ThomsonGen/scripts/scan_upstream.py` on the stored Lean files of this revision: 0 verbatim, all near-copies attributed |

Comparator step: 29.7 min wall (`comparator.out`). Comparator ran with its non-sandboxing shim
`fake-landrun.sh`, because `landrun` was not available on the machine.

Differences between the checked revision and this repository: comment lines only, in `Kissing/Bound.lean`,
`Kissing/CertK.lean`, `Kissing/Cert/ChkId.lean`, `Kissing/Cert/OkF.lean` and `Kissing/Cert/Check.lean` (attribution of
adapted upstream declarations and two reworded docstrings), so the sha256 of these five files in `files.sha256`
differ from the files here. No statement, definition or proof changed. A one-module-at-a-time build of this
revision is not yet recorded here.
