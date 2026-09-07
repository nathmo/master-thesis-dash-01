"""Thesis figures for DASH-01, built from the training archive.

Every curve reads a run's progress.csv directly, so the numbers in the caption and the
numbers in the figure come from the same file. Episode length is converted from control
steps to seconds with that run's own control_decimation against the 1 ms physics step.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

RUNS = "c:/Users/Nathann/Downloads/running_robot/training"
OUT = "c:/Users/Nathann/ClawdDrive/Code/master-thesis-dash-01/Figures"
PREVIEW = os.path.dirname(os.path.abspath(__file__)) + "/preview"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "font.size": 8,
    "axes.labelsize": 8,
    "axes.titlesize": 8.5,
    "legend.fontsize": 7,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linewidth": 0.5,
    "lines.linewidth": 1.0,
    "figure.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
})

C = {
    "blue": "#2b6cb0", "orange": "#c05621", "green": "#2f855a",
    "red": "#9b2c2c", "purple": "#6b46c1", "grey": "#4a5568",
    "teal": "#2c7a7b", "olive": "#7b6a1f",
}


def save(fig, name):
    fig.savefig(f"{OUT}/{name}.pdf")
    fig.savefig(f"{PREVIEW}/{name}.png", dpi=200)
    plt.close(fig)
    print(name, "ok")


def load(run, root=None):
    """The archive holds duplicate copies of some runs, and some copies are resume
    windows rather than full histories. Prefer the copy that starts earliest, then the
    longest of those; an explicit root overrides both."""
    best = None
    for root in ((root,) if root else ("runs_dl", "runs", "runs_restored")):
        p = f"{RUNS}/{root}/{run}/progress.csv"
        if not os.path.exists(p):
            continue
        d = pd.read_csv(p)
        cfgp = f"{RUNS}/{root}/{run}/resolved_config.json"
        cfg = json.load(open(cfgp))["config"] if os.path.exists(cfgp) else {}
        dec = float(cfg.get("control_decimation", 5))
        d = d.dropna(subset=["time/total_timesteps", "rollout/ep_len_mean"])
        d = d.sort_values("time/total_timesteps")
        d["Msteps"] = d["time/total_timesteps"] / 1e6
        d["ep_s"] = d["rollout/ep_len_mean"] * dec * 1e-3
        key = (d["Msteps"].iloc[0], -d["Msteps"].iloc[-1])
        if best is None or key < (best["Msteps"].iloc[0], -best["Msteps"].iloc[-1]):
            best = d
    if best is None:
        raise FileNotFoundError(run)
    return best


def smooth(y, w=41):
    y = np.asarray(y, float)
    if len(y) < w:
        return y
    k = np.ones(w) / w
    pad = w // 2
    yp = np.concatenate([np.full(pad, y[0]), y, np.full(pad, y[-1])])
    return np.convolve(yp, k, mode="valid")[: len(y)]


# ---------------------------------------------------------------- fig: ladder
def fig_ladder():
    # greedy survival from the deterministic evaluation of the same checkpoints
    arms = [
        ("m2_sprint", "m2   $x,z$", C["blue"], "-", 53.0),
        ("m3_stiff_hi", "m3   $+$ pitch", C["orange"], "-", 39.0),
        ("m4_stiff", "m4   $+\\,y$", C["green"], "-", 38.0),
        ("m5_stiff", "m5   $+$ roll", C["red"], "-", 26.0),
        ("m6_stiff", "m6   all six free", C["purple"], "-", 60.0),
        ("m7_freq", "m7   m3, cadence fixed", C["teal"], "--", 37.0),
    ]
    fig, ax = plt.subplots(figsize=(5.6, 2.6))
    for run, lab, col, ls, greedy in arms:
        d = load(run)
        ax.plot(d["Msteps"], smooth(d["ep_s"]), color=col, ls=ls, label=lab, alpha=0.95)
        ax.plot([d["Msteps"].iloc[-1]], [greedy], marker="*", ms=8, color=col,
                mec="white", mew=0.5, ls="none", zorder=5)
    ax.axhline(60, color="k", lw=0.7, ls=":", zorder=0)
    ax.text(330, 61.0, "60 s episode cap", fontsize=6.5, ha="left", va="bottom")
    ax.set_xlabel("environment steps within the milestone (millions)")
    ax.set_ylabel("episode length (s)")
    ax.set_xlim(0, 640)
    ax.set_ylim(0, 88)
    ax.legend(loc="upper left", ncol=3, frameon=False, handlelength=1.6,
              columnspacing=1.0, borderpad=0.0, labelspacing=0.3)
    ax.text(0.70, 0.45, "$\star$ deterministic evaluation of the final checkpoint",
            transform=ax.transAxes, ha="right", va="center", fontsize=6.5)
    save(fig, "fig_ladder")


# ------------------------------------------------------- fig: three comparisons
def fig_experiments():
    fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.15))

    # (a) generator A/B, cold start on the pitch-free plant
    ax = axes[0]
    for run, lab, col in [("ab_cpg_cold_s0", "oscillator", C["orange"]),
                          ("ab_f_cold_s0", "Fourier", C["blue"])]:
        d = load(run)
        ax.plot(d["Msteps"], smooth(d["ep_s"], 61), color=col, label=lab)
    ax.set_title("(a) generator, cold m3")
    ax.set_xlabel("M steps")
    ax.set_ylabel("episode length (s)")
    ax.set_ylim(0.6, 2.3)
    ax.legend(loc="lower right", frameon=True, framealpha=0.93, edgecolor="none", handlelength=1.4)

    # (b) drive bandwidth bracket, cold m2, truncated to the shortest arm
    ax = axes[1]
    for run, lab, col in [("m2drv_d12_s0", "12 Hz (idealised)", C["grey"]),
                          ("m2drv_d3_s0", "3 Hz (retuned)", C["green"]),
                          ("m2drv_d08_s0", "0.8 Hz (as built)", C["red"])]:
        d = load(run)
        d = d[d["Msteps"] <= 20.2]
        ax.plot(d["Msteps"], smooth(d["ep_s"], 41), color=col, label=lab)
    ax.set_title("(b) drive bandwidth, cold m2")
    ax.set_xlabel("M steps")
    ax.set_xlim(0, 20.5)
    ax.set_ylim(-2, 72)
    ax.legend(loc="upper left", frameon=True, framealpha=0.93, edgecolor="none", handlelength=1.4)

    # (c) ankle arms, cold m3 on the measured plant
    ax = axes[2]
    for run, root, lab, col in [
        ("ankle2_m3_rigid_s0", "runs", "welded", C["grey"]),
        ("ankle2_m3_bar_comp_s0", "runs_dl", "carbon strut", C["green"]),
        ("ankle2_m3_bar_s0", "runs", "tension-only rod", C["purple"]),
        ("ankle2_m3_k350_s0", "runs", "spring, $k=350$", C["olive"]),
    ]:
        d = load(run, root)
        ax.plot(d["Msteps"], smooth(d["ep_s"], 41), color=col, label=lab)
    ax.set_title("(c) ankle, cold m3")
    ax.set_xlabel("M steps")
    ax.set_xlim(0, 52)
    ax.set_ylim(-0.5, 19)
    ax.legend(loc="upper left", frameon=True, framealpha=0.93, edgecolor="none", handlelength=1.4,
              borderpad=0.25, labelspacing=0.25)
    fig.tight_layout(w_pad=1.4)
    save(fig, "fig_experiments")


# ------------------------------------------------------------------ fig: drive
def fig_drive():
    f = np.array([0.8, 1.1, 1.4, 2.0, 2.5, 2.9])
    g = np.array([0.71, 0.60, 0.53, 0.38, 0.30, 0.28])
    ph = np.array([-48.0, -61.0, -71.0, -86.0, -94.0, -104.0])
    fc, td = 0.8, 0.025
    ff = np.logspace(np.log10(0.3), np.log10(6.0), 400)
    gm = 1.0 / np.sqrt(1 + (ff / fc) ** 2)
    pm = -np.degrees(np.arctan(ff / fc)) - 360.0 * ff * td

    fig, axes = plt.subplots(1, 2, figsize=(5.6, 2.0), sharex=True)
    for ax, meas, mod, ylab in ((axes[0], g, gm, "closed-loop gain"),
                                (axes[1], ph, pm, "phase (deg)")):
        ax.axvspan(0.5, 4.0, color=C["blue"], alpha=0.09, lw=0)
        ax.semilogx(ff, mod, color=C["grey"], lw=0.9,
                    label="0.8 Hz pole $+$ 25 ms delay")
        ax.semilogx(f, meas, "o", ms=3.2, color=C["red"], label="measured")
        ax.set_xlabel("excitation frequency (Hz)")
        ax.set_ylabel(ylab)
        ax.set_xlim(0.3, 6.0)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"{v:g}"))
        ax.xaxis.set_minor_formatter(mticker.NullFormatter())
        ax.set_xticks([0.5, 1, 2, 4])
    axes[0].set_ylim(0, 1.05)
    axes[0].legend(loc="lower left", frameon=True, framealpha=0.93, edgecolor="none", handlelength=1.5)
    axes[1].set_ylim(-200, 0)
    axes[1].text(0.52, -186, "learnable gait\nfrequency band", fontsize=6.5,
                 color=C["blue"], va="bottom")
    fig.tight_layout(w_pad=1.6)
    save(fig, "fig_drive")


if __name__ == "__main__":
    os.makedirs(PREVIEW, exist_ok=True)
    fig_ladder()
    fig_experiments()
    fig_drive()
