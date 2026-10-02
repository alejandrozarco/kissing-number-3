#!/usr/bin/env python3
"""Figures from the repository data only (light and dark SVG variants):

  bounds         numerics/kissing3/results.jsonl   floating-point bounds by degree
  configuration  lean/Kissing/Twelve.lean          the twelve balls around the central ball
  angles         lean/Kissing/Twelve.lean          the 66 angles between the twelve directions
  certificate    numerics/kissing3/cert_D10.json   the certificate polynomial R on the slice u = v

Usage: python3 figures/make_figures.py   (matplotlib 3.9.4, numpy)"""
import json, math, os, re, sys
from fractions import Fraction as Fr
import numpy as np
import matplotlib
matplotlib.use("svg")
matplotlib.rcParams["svg.hashsalt"] = "kissing-number-3"   # deterministic SVG ids
import matplotlib.pyplot as plt
from matplotlib import colors

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NUM = os.path.join(ROOT, "numerics", "kissing3")


def theme(dark):
    if dark:
        return dict(fg="#e6e6e6", bg="#0d1117", c1="#79c0ff", c2="#ffa657", c3="#7ee787", c4="#d2a8ff", grid="#30363d")
    return dict(fg="#1f2328", bg="#ffffff", c1="#0969da", c2="#bc4c00", c3="#1a7f37", c4="#8250df", grid="#d0d7de")


def style(fig, ax, th):
    fig.patch.set_facecolor(th["bg"]); ax.set_facecolor(th["bg"])
    ax.tick_params(colors=th["fg"])
    for s in ax.spines.values():
        s.set_color(th["fg"])
    ax.xaxis.label.set_color(th["fg"]); ax.yaxis.label.set_color(th["fg"]); ax.title.set_color(th["fg"])


def save(fig, name, dark, th):
    fig.savefig(os.path.join(HERE, f"{name}_{'dark' if dark else 'light'}.svg"), facecolor=th["bg"],
                metadata={"Date": None})
    plt.close(fig)


def legend(ax, th, **kw):
    leg = ax.legend(frameon=False, **kw)
    for t in leg.get_texts():
        t.set_color(th["fg"])


# ------------------------------------------------------------------ data
R = [json.loads(l) for l in open(os.path.join(NUM, "results.jsonl"))]
lp = {r["D"]: r["bound"] for r in R if r["mode"] == "bv" and not r["three_point"]}
bv = {r["D"]: r["bound"] for r in R if r["mode"] == "bv" and r["three_point"]}
fx = {}
for r in R:
    if r["mode"] == "fixn" and r["delsarte"] is None and "noq" not in r["tag"]:
        fx.setdefault(r["D"], []).append((r["n"], r["e"]))

tw = open(os.path.join(ROOT, "lean", "Kissing", "Twelve.lean"), encoding="utf-8").read()
L12 = int(re.search(r"def L : ℤ := (\d+)", tw).group(1))
rows = re.findall(r"!\[(-?\d+), (-?\d+), (-?\d+)\]", tw.split("def P")[1].split("theorem")[0])
PTS = np.array([[int(x) for x in r] for r in rows], float) / L12          # centres, norm 2
assert PTS.shape == (12, 3) and np.allclose(np.linalg.norm(PTS, axis=1), 2)


# ------------------------------------------------------------------ 1. bounds by degree
def bracket(pts):
    neg = [n for n, e in pts if e < 0]
    pos = [n for n, e in pts if e > 0]
    return (max(neg) if neg else None), (min(pos) if pos else None)


def fig_bounds(dark):
    th = theme(dark)
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); style(fig, ax, th)
    Ds = sorted(lp)
    ax.plot(Ds, [lp[d] for d in Ds], "s--", color=th["c1"], label="two-point (Delsarte) bound")
    Db = sorted(bv)
    ax.plot(Db, [bv[d] for d in Db], "o-", color=th["c2"], label="three-point bound")
    first = True
    for d, pts in sorted(fx.items()):
        lo, hi = bracket(pts)
        if lo is not None and hi is not None:
            ax.plot([d, d], [lo, hi], color=th["c3"], lw=6, solid_capstyle="butt",
                    label="three-point, fixed $n$: threshold" if first else None)
            first = False
    ax.axhline(13, color=th["fg"], lw=0.8, ls=":")
    ax.set_xlabel("total degree $D$ of the polynomials")
    ax.set_ylabel("upper bound for the kissing number")
    ax.set_xticks(sorted(set(Ds) | set(Db)))
    ax.set_ylim(12.3, 13.4)
    legend(ax, th, loc="lower left")
    ax.set_title("Floating-point bounds (numerics/kissing3/results.jsonl)", fontsize=10)
    fig.tight_layout(); save(fig, "bounds", dark, th)


# ------------------------------------------------------------------ 2. the twelve balls
def fig_configuration(dark):
    th = theme(dark)
    fig = plt.figure(figsize=(9.0, 4.6)); fig.patch.set_facecolor(th["bg"])
    elev, azim = 12, 20
    view = np.array([np.cos(np.radians(elev)) * np.cos(np.radians(azim)),
                     np.cos(np.radians(elev)) * np.sin(np.radians(azim)), np.sin(np.radians(elev))])
    uu, vv = np.meshgrid(np.linspace(0, 2 * np.pi, 48), np.linspace(0, np.pi, 24))
    sx, sy, sz = np.cos(uu) * np.sin(vv), np.sin(uu) * np.sin(vv), np.cos(vv)
    # (a) the thirteen unit balls, drawn back to front
    ax = fig.add_subplot(1, 2, 1, projection="3d"); ax.set_facecolor(th["bg"])
    centres = [(np.zeros(3), th["c2"])] + [(c, th["c1"]) for c in PTS]
    for c, col in sorted(centres, key=lambda cc: float(cc[0] @ view)):
        ax.plot_surface(sx + c[0], sy + c[1], sz + c[2], color=col, shade=True, linewidth=0, rasterized=True)
    ax.set_box_aspect((1, 1, 1))
    for f in (ax.set_xlim, ax.set_ylim, ax.set_zlim):
        f(-3, 3)
    ax.view_init(elev=elev, azim=azim); ax.set_axis_off()
    ax.set_title("the central ball and twelve touching balls", color=th["fg"], fontsize=10)
    # (b) the centres on the sphere of radius 2, with the 30 nearest-neighbour pairs
    ax = fig.add_subplot(1, 2, 2, projection="3d"); ax.set_facecolor(th["bg"])
    ax.plot_surface(2 * sx, 2 * sy, 2 * sz, color=th["grid"], alpha=0.25, linewidth=0, rasterized=True)
    U = PTS / 2
    for i in range(12):
        for j in range(i + 1, 12):
            if U[i] @ U[j] > 0.3:                         # the 30 nearest pairs, at 61.3 to 65.7 degrees
                ax.plot(*zip(PTS[i], PTS[j]), color=th["c1"], lw=1.2)
    front = PTS @ view >= 0
    ax.scatter(*PTS[front].T, color=th["c2"], s=28, depthshade=False)
    ax.scatter(*PTS[~front].T, color=th["c2"], s=28, alpha=0.4, depthshade=False)
    ax.set_box_aspect((1, 1, 1))
    for f in (ax.set_xlim, ax.set_ylim, ax.set_zlim):
        f(-2.2, 2.2)
    ax.view_init(elev=elev, azim=azim); ax.set_axis_off()
    ax.set_title("centres (radius 2) and nearest-neighbour pairs", color=th["fg"], fontsize=10)
    fig.suptitle("Twelve kissing balls in dimension 3 (lean/Kissing/Twelve.lean)", color=th["fg"], fontsize=11)
    fig.tight_layout(); save(fig, "configuration", dark, th)


# ------------------------------------------------------------------ 3. the 66 angles
def fig_angles(dark):
    th = theme(dark)
    U = PTS / 2
    ang = sorted(math.degrees(math.acos(max(-1.0, min(1.0, float(U[i] @ U[j])))))
                 for i in range(12) for j in range(i + 1, 12))
    fig, ax = plt.subplots(figsize=(7.2, 3.6)); style(fig, ax, th)
    ax.plot(range(1, 67), ang, "o", color=th["c1"], ms=4, label="angle between two centres (66 pairs)")
    ax.axhline(60, color=th["c2"], lw=1.2, label="$60^\\circ$: touching (inner product $1/2$)")
    ax.axhline(math.degrees(math.acos(1 / math.sqrt(5))), color=th["fg"], lw=0.8, ls=":",
               label="regular icosahedron, nearest neighbours")
    ax.set_xlabel("pairs, sorted by angle")
    ax.set_ylabel("angle (degrees)")
    ax.set_ylim(55, 185)
    legend(ax, th, loc="upper left", fontsize=8)
    ax.set_title(f"Smallest angle {math.floor(ang[0] * 100) / 100:.2f}$^\\circ$ "
                 f"(lean/Kissing/Twelve.lean)", fontsize=10)
    fig.tight_layout(); save(fig, "angles", dark, th)


# ------------------------------------------------------------------ 4. the certificate polynomial
def fig_certificate(dark):
    th = theme(dark)
    sys.path.insert(0, NUM)
    import round_k3 as RK
    J = json.load(open(os.path.join(NUM, "cert_D10.json")))
    n, D, e = J["n"], J["D"], Fr(J["e"])
    F = [[[Fr(x) for x in row] for row in M] for M in J["F"]]
    P = RK.target_poly(F, n, e, D)                       # P = -R - e/C(n,2)
    C = math.comb(n, 2)
    m = np.linspace(-1, 0.5, 601)
    U, T = np.meshgrid(m, m)                              # slice u = v
    Pv = np.zeros_like(U)
    for (a, b, c), coef in P.items():
        Pv += float(coef) * U ** (a + b) * T ** c
    Rv = -Pv - float(e) / C
    ok = 1 + 2 * U * U * T - 2 * U * U - T * T >= 0      # Gram condition with v = u
    ratio = np.where(ok, -Rv / (float(e) / C), np.nan)   # >= 1 means R <= -e/C(n,2)
    fig, ax = plt.subplots(figsize=(5.8, 4.8)); style(fig, ax, th)
    im = ax.pcolormesh(U, T, ratio, shading="auto", cmap="viridis",
                       norm=colors.LogNorm(vmin=1, vmax=np.nanmax(ratio)), rasterized=True)
    cb = fig.colorbar(im, ax=ax)
    cb.set_label("$-R(u,u,t)\\,/\\,(e/78)$", color=th["fg"])
    cb.ax.tick_params(colors=th["fg"]); cb.outline.set_edgecolor(th["fg"])
    k = np.nanargmin(ratio)
    ax.plot(U.flat[k], T.flat[k], "x", color=th["c2"], ms=9, mew=2,
            label=f"minimum {math.floor(np.nanmin(ratio) * 100) / 100:.2f} at $({U.flat[k]:.2f}, {T.flat[k]:.2f})$")
    ax.set_xlabel("$u = v$")
    ax.set_ylabel("$t$")
    ax.set_aspect("equal")
    legend(ax, th, loc="lower left", fontsize=8)
    ax.set_title("Certificate inequality on the slice $u = v$\n(values $\\geq 1$ mean $R \\leq -e/78$; "
                 "cert_D10.json)", fontsize=10)
    fig.tight_layout(); save(fig, "certificate", dark, th)


for dark in (False, True):
    fig_bounds(dark)
    fig_configuration(dark)
    fig_angles(dark)
    fig_certificate(dark)
