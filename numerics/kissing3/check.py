"""Independent float post-check of a fixed-n solution sol/<tag>.npz (from k3.py fixn/mu):
rebuilds s and the upstream Rk-form R(u,v,t) from the F blocks, and maximises R over Delta by dense
sampling + local refinement (no use of the SOS blocks).  A valid certificate needs max_Delta R < 0;
the solver claims max R <= -e/C(n,2).  Also reports block eigenvalues and coefficient sizes.

usage: python3 check.py TAG
"""
import os, sys, json
import numpy as np

tag = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
Z = np.load(os.path.join(HERE, "sol", tag + ".npz"), allow_pickle=True)
meta = json.loads(str(Z["meta"]))
os.environ["POLYD"] = str(meta["D"])
sys.path.insert(0, HERE)
import polyk
from polyk import SYM_AVG, Yk_columns, subst_matrix, univ_embed, peval, N3
from numpy.polynomial import legendre as Lg
from scipy.optimize import minimize

D = meta["D"]; n = meta["n"]
mu = float(meta.get("mu") or 0.0)      # mu mode: actual blocks are X + mu I
sizes = [D // 2 + 1 - k for k in range(D // 2 + 1)]
s = np.zeros(N3); Fs = []
for k, m in enumerate(sizes):
    F = Z[f"F{k}"] + mu * np.eye(m)
    Fs.append(F)
    s += np.asarray(SYM_AVG @ Yk_columns(k, m)) @ F.ravel()
if meta.get("delsarte") is not None:
    a = Z["a"]; d2 = len(a) - 1
    L2 = np.zeros((D + 1, d2 + 1))
    for j in range(d2 + 1):
        c = Lg.leg2poly(np.eye(d2 + 1)[j][:j + 1]); L2[:len(c), j] = c
    s += (univ_embed(0) + univ_embed(1) + univ_embed(2)) @ L2 @ a / 3.0
sub = lambda spec: np.asarray(subst_matrix(spec) @ s)
R = (n - 2) * s + sub((0, 0, 1.0)) + sub((1, 1, 1.0)) + sub((2, 2, 1.0)) + sub((1.0, 1.0, 1.0)) / (n - 1)
e = float(np.ravel(Z["e"])[0]) if "e" in Z.files else meta["e"]
C2 = n * (n - 1) / 2

rng = np.random.default_rng(0)
det = lambda u, v, t: 1 + 2 * u * v * t - u * u - v * v - t * t
pts = []
# (a) uniform box samples inside Delta
P = rng.uniform(-1, 0.5, size=(2_000_000, 3)); P = P[det(*P.T) >= 0]; pts.append(P)
# (b) Gram-boundary (coplanar triples) and faces x = 1/2
th = rng.uniform(0, 2 * np.pi, size=(2_000_000, 2))
Q = np.stack([np.cos(th[:, 0]), np.cos(th[:, 1]), np.cos(th[:, 0] - th[:, 1])], 1)
pts.append(Q[(Q <= 0.5).all(1)])
for i in range(3):
    W = rng.uniform(-1, 0.5, size=(1_000_000, 3)); W[:, i] = 0.5; pts.append(W[det(*W.T) >= 0])
# (c) a grid incl. corners
g = np.linspace(-1, 0.5, 61); G = np.array(np.meshgrid(g, g, g)).reshape(3, -1).T; pts.append(G[det(*G.T) >= -1e-12])
P = np.concatenate(pts)
vals = np.concatenate([peval(R, *P[i:i + 200000].T) for i in range(0, len(P), 200000)])
order = np.argsort(-vals)[:40]
best = vals[order[0]]; bestp = P[order[0]]


def negR(x):
    return -peval(R, *x)[0]


cons = [{"type": "ineq", "fun": lambda x: det(*x)}]
for p in P[order]:
    r = minimize(negR, p, method="SLSQP", bounds=[(-1, 0.5)] * 3, constraints=cons, options=dict(ftol=1e-14))
    if r.success and det(*r.x) >= -1e-10 and (r.x <= 0.5 + 1e-12).all() and -r.fun > best:
        best, bestp = -r.fun, r.x
eigF = [float(np.linalg.eigvalsh(F)[0]) for F in Fs]
out = dict(tag=tag, n=n, D=D, e=e, claimed_maxR=-e / C2, sampled_maxR=float(best), argmax=[round(x, 6) for x in bestp],
           n_samples=int(len(P)), F_mineig=min(eigF), F_maxabs=float(max(np.abs(F).max() for F in Fs)),
           F_trace=float(sum(np.trace(F) for F in Fs)), R_coef_l1=float(np.abs(R).sum()),
           OK=bool(best < 0 and min(eigF) >= -1e-12))
print(json.dumps(out))
with open(os.path.join(HERE, "checks.jsonl"), "a") as fh:
    fh.write(json.dumps(out) + "\n")
