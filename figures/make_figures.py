#!/usr/bin/env python3
"""Figures from the repository data only: numerics/kissing3/results.jsonl.
Usage: python3 figures/make_figures.py   (writes figures/bounds_{light,dark}.svg)"""
import json, os
import matplotlib
matplotlib.use("svg")
matplotlib.rcParams["svg.hashsalt"] = "kissing-number-3"   # deterministic SVG ids
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
R = [json.loads(l) for l in open(os.path.join(HERE, "..", "numerics", "kissing3", "results.jsonl"))]
lp = {r["D"]: r["bound"] for r in R if r["mode"] == "bv" and not r["three_point"]}
bv = {r["D"]: r["bound"] for r in R if r["mode"] == "bv" and r["three_point"]}
fx = {}
for r in R:
    if r["mode"] == "fixn" and r["delsarte"] is None and "noq" not in r["tag"]:
        fx.setdefault(r["D"], []).append((r["n"], r["e"]))


def bracket(pts):
    """largest real n with e < 0 and smallest with e > 0 (the fixed-n threshold lies between them)."""
    neg = [n for n, e in pts if e < 0]
    pos = [n for n, e in pts if e > 0]
    return (max(neg) if neg else None), (min(pos) if pos else None)


def draw(dark):
    fg, bg = ("#e6e6e6", "#0d1117") if dark else ("#1f2328", "#ffffff")
    c1, c2, c3 = ("#79c0ff", "#ffa657", "#7ee787") if dark else ("#0969da", "#bc4c00", "#1a7f37")
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    fig.patch.set_facecolor(bg); ax.set_facecolor(bg)
    Ds = sorted(lp)
    ax.plot(Ds, [lp[d] for d in Ds], "s--", color=c1, label="two-point (Delsarte) bound")
    Db = sorted(bv)
    ax.plot(Db, [bv[d] for d in Db], "o-", color=c2, label="three-point bound")
    for d, pts in sorted(fx.items()):
        lo, hi = bracket(pts)
        if lo is not None and hi is not None:
            ax.plot([d, d], [lo, hi], color=c3, lw=6, solid_capstyle="butt",
                    label="three-point, fixed $n$: threshold" if d == min(fx) or lo else None)
    for y in (12, 13):
        ax.axhline(y, color=fg, lw=0.8, ls=":")
    ax.set_xlabel("total degree $D$ of the three-point polynomials", color=fg)
    ax.set_ylabel("upper bound for the kissing number", color=fg)
    ax.set_xticks(sorted(set(Ds) | set(Db)))
    ax.set_ylim(12.3, 13.4)
    ax.tick_params(colors=fg)
    for s in ax.spines.values():
        s.set_color(fg)
    h, l = ax.get_legend_handles_labels()
    seen = {}
    for hh, ll in zip(h, l):
        seen.setdefault(ll, hh)
    leg = ax.legend(seen.values(), seen.keys(), frameon=False, loc="lower left")
    for t in leg.get_texts():
        t.set_color(fg)
    ax.set_title("Floating-point bounds (numerics/kissing3/results.jsonl)", color=fg, fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, f"bounds_{'dark' if dark else 'light'}.svg"), facecolor=bg, metadata={"Date": None})


for dark in (False, True):
    draw(dark)
