# Certificate for thirteen points (dimension 3)

Floating-point SDP, exact rounding and exact check of the three-point certificate used in `lean/Kissing/Cert/`.

| file | content |
|---|---|
| `k3.py` | SDP formulations (Clarabel via cvxpy): `bv D` (classical three-point bound), `fixn D n` (fixed-$`n`$ form used here), `mu D n frac` (interior solution at a fraction of the optimal margin), `test` (unit tests of the kernels and the identity) |
| `polyk.py` | polynomial toolkit (from alejandrozarco/thomson-n7-log) |
| `check.py` | floating-point check of a solution: maximum of $`R`$ over the region by dense sampling, eigenvalues |
| `run.sh` | runs `k3.py` at low priority with one thread |
| `results.jsonl`, `checks.jsonl` | outputs of `k3.py` and `check.py` (all degrees tried) |
| `sol/fixn_D10_n13.npz`, `sol/fixn_D10_n13_mu0.5.npz` | the degree-10 solutions (maximal margin; interior, used for rounding) |
| `round_k3.py` | exact rounding: blocks rounded to multiples of $`2^{-24}`$, margin $`e = 1/32`$, residual absorbed into the constant-multiplier block. Its log warns that the absorbed residual is not small compared with the interior margin; the exact positive-definiteness check that follows (and `check_cert_k3.py`) settles this |
| `cert_D10.json` | the exact certificate (rationals as strings). Its multipliers are $`1/2 - x`$; `lean/gen/emit_k3.py` rescales those blocks by 2 for the Lean multipliers $`1 - 2x`$ |
| `check_cert_k3.py` | independent exact check: input validation, degree bound computed from the data (here 10), the identity on an $`11^3`$ grid, positive definiteness by leading principal minors (python-flint) |
| `check_controls_k3.py` | negative controls: nine tampered certificates, all of which `check_cert_k3.py` must reject |
| `logs/` | output of `round_k3.py`, `check_cert_k3.py` and `check_controls_k3.py` |

Floating-point summary from `results.jsonl` (not certified): for $`n = 13`$ the fixed-$`n`$ problem has no positive
margin at degree 6 or 8, and margin $`e \approx 0.0706`$ at degree 10 (normalisation $`\sum_k \mathrm{tr}\, F_k = 1`$).
The interior solution at half that margin has all blocks at least $`1.19 \cdot 10^{-5} I`$.
