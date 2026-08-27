"""Sagittal kinematic schematic of the DASH-01 leg, read out of the MJCF stance keyframe.

Every point is a joint anchor or a site position taken from mj_forward, so the proportions
are the simulated robot's rather than a sketch.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import mujoco

MODEL = "c:/Users/Nathann/Downloads/running_robot/training/model/dash01.xml"
OUT = "c:/Users/Nathann/ClawdDrive/Code/master-thesis-dash-01/Figures/fig_leg.pdf"
PREVIEW = os.path.dirname(os.path.abspath(__file__)) + "/preview/fig_leg.png"

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif"], "font.size": 8,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.02, "figure.dpi": 200,
})

m = mujoco.MjModel.from_xml_path(MODEL)
d = mujoco.MjData(m)
mujoco.mj_resetDataKeyframe(m, d, mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_KEY, "stand"))
mujoco.mj_forward(m, d)


def jointxy(name):
    jid = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_JOINT, name)
    p = d.xanchor[jid]
    return np.array([p[0], p[2]])


def bodyxy(name):
    bid = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_BODY, name)
    p = d.xpos[bid]
    return np.array([p[0], p[2]])


def sitexy(name):
    sid = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_SITE, name)
    p = d.site_xpos[sid]
    return np.array([p[0], p[2]])


J = "R\u00c3\u00a9volution"
base = bodyxy("bodyNCS-v1")
hip = jointxy("bodyNCS-v1_" + J + "-1")
cam = jointxy("HipLeftNCS-v1_" + J + "-3")
thigh = jointxy("HipLeftNCS-v1_" + J + "-5")
prod = jointxy("CamLeftNCS-v1_" + J + "-11")
knee = jointxy("ThighLeftNCS-v1_" + J + "-7")
ankle = jointxy("LegLeftNCS-v1_" + J + "-9")
anchor = sitexy("leg_anchor_L")
gid = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_GEOM, "foot_L_col")
toe = np.array([d.geom_xpos[gid][0], d.geom_xpos[gid][2]])

fig, ax = plt.subplots(figsize=(2.9, 3.4))

STRUCT = "#2d3748"
LOOP = "#c05621"
PASS = "#2f855a"
MUTED = "#718096"


def seg(a, b, col=STRUCT, lw=2.0, ls="-", z=2):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=col, lw=lw, ls=ls,
            solid_capstyle="round", zorder=z)


# torso
ax.plot([cam[0] - 0.03, thigh[0] + 0.03], [base[1], base[1]], color=STRUCT, lw=8,
        solid_capstyle="round", zorder=1, alpha=0.30)
ax.annotate("torso: battery, computer, IMU", (thigh[0] + 0.03, base[1]),
            textcoords="offset points", xytext=(6, -14), ha="left",
            fontsize=7.0, color=MUTED)

# serial chain
seg(cam, thigh, lw=2.6)
seg(thigh, knee, lw=2.6)
seg(knee, ankle, lw=2.6)
seg(ankle, toe, lw=2.6)
# closing branch of the 4-bar
seg(cam, prod, col=LOOP, lw=2.0)
seg(prod, anchor, col=LOOP, lw=2.0)
seg(anchor, knee, col=LOOP, lw=1.0, ls=":")

for p in (hip, cam, thigh, knee, prod, anchor):
    ax.plot(*p, marker="o", ms=4.2, mfc="white", mec=STRUCT, mew=1.1, zorder=4)
ax.plot(*ankle, marker="o", ms=6.5, mfc="white", mec=PASS, mew=1.7, zorder=4)
ax.plot(*toe, marker="o", ms=6, color=STRUCT, zorder=4)


def lab(p, text, dx, dy, col=STRUCT, ha="left", arrow=False, style=None):
    kw = dict(fontsize=7.2, color=col, ha=ha)
    if style:
        kw["style"] = style
    if arrow:
        kw["arrowprops"] = dict(arrowstyle="-", lw=0.6, color=col, shrinkA=1, shrinkB=3)
    ax.annotate(text, p, textcoords="offset points", xytext=(dx, dy), **kw)


lab(cam, "cam motor", -32, 34, ha="right", arrow=True)
lab(hip, "hip roll motor\n(axis into the page)", -2, 54, ha="center", arrow=True)
lab(thigh, "thigh motor", 36, 24, ha="left", arrow=True)
lab(0.5 * (prod + anchor), "pushrod:\ncloses the 4-bar", -12, 2, col=LOOP, ha="right")
lab(knee, "knee (passive)", 9, 1)
lab(ankle, "ankle\n(passive spring)", -9, -3, col=PASS, ha="right")
lab(toe, "point foot", 12, -3)

# scale bar
x0 = toe[0] + 0.30
ax.plot([x0, x0], [toe[1], toe[1] + 0.2], color=MUTED, lw=1.0)
for yy in (toe[1], toe[1] + 0.2):
    ax.plot([x0 - 0.012, x0 + 0.012], [yy, yy], color=MUTED, lw=1.0)
ax.text(x0 + 0.02, toe[1] + 0.1, "0.2 m", fontsize=7, color=MUTED, va="center")

# ground
ax.plot([toe[0] - 0.34, toe[0] + 0.30], [toe[1] - 0.025, toe[1] - 0.025],
        color="#a0aec0", lw=1.0)

ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(-0.56, 0.60)
ax.set_ylim(toe[1] - 0.10, base[1] + 0.28)
fig.savefig(OUT)
fig.savefig(PREVIEW, dpi=220)
print("thigh %.3f  shin %.3f  foot %.3f  cam-thigh spacing %.3f  stance height %.3f" % (
    np.linalg.norm(knee - thigh), np.linalg.norm(ankle - knee),
    np.linalg.norm(toe - ankle), np.linalg.norm(thigh - cam), base[1] - toe[1]))
