# AI disclosure

AI models produced the content of this repository: the certificate, the numerical and exact checkers, the Lean
formalisation, the figure and the text. The repository owner chose the problem, approved the Lean statement, directed
the work and decided on scope and publication. The owner did not check the mathematics or the Lean code line by line.

**Models**
- Claude Opus 5.5 (Anthropic, via Claude Code) did the work.
- The review was run as a separate read-only instance of Claude Opus 5.5 without access to the working context.
- The commits carry a `Co-Authored-By: Claude Opus 5.5` trailer.

**Review and errors found.** The review found no mathematical error. It asked for:
- evidence that the committed files are the ones that were checked (now: a clean build and a Comparator run of a
  fresh copy of the committed package, with sha256 of every checked file, in `verification/`);
- a Comparator run and a package that builds on its own (now: `lean/regen.sh`, `lean/comparator.json`);
- a further test of the definition, a ball that does not touch the central ball (now `not_isKissing_far`).

Problems found and fixed during the work: one certificate-check module needed more memory than intended and was split
into one module per block; adapted upstream declarations lacked per-declaration attribution, which
`lean/ThomsonGen/scripts/scan_upstream.py` now checks.

AI review is not peer review, and no human expert has checked this work. In the terminology of the Lean community
this is a *warrant*, not a human-readable proof.

**What is checked by software**
- `numerics/kissing3/check_cert_k3.py` checks the certificate in exact rational arithmetic, independently of the
  rounding code.
- The Lean 4 kernel checks the formalisation in `lean/`. `#print axioms` reports `[propext, Classical.choice, Quot.sound]`.
- Comparator checks that the proved theorems have the statements of `lean/Kissing/Statement.lean`. It ran without the
  `landrun` sandbox (`verification/`).

What remains to be trusted:
- that `lean/Kissing/Statement.lean` expresses the intended theorem (see `lean/STATEMENT.md`);
- the Mathlib definitions used in `lean/Kissing/Statement.lean`, which imports only Mathlib;
- the Lean kernel and toolchain;
- Comparator and lean4export (run without the `landrun` sandbox).

The code regenerated from the upstream formalisation,
[huwngtran/thomson-n7-lean](https://github.com/huwngtran/thomson-n7-lean) (itself produced with AI agents), is used only
inside the proof, which the kernel checks; it does not enter the statement.
