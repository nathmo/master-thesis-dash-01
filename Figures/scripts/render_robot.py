"""Two clean views of DASH-01, rendered from the MJCF the policies train against."""
import os

import numpy as np
import mujoco
from PIL import Image

MODEL_DIR = "c:/Users/Nathann/Downloads/running_robot/training/model"
MODEL = MODEL_DIR + "/dash01.xml"
TMP = MODEL_DIR + "/_render_tmp.xml"
OUT = "c:/Users/Nathann/ClawdDrive/Code/master-thesis-dash-01/Figures/fig_robot.png"

W, H = 900, 1200

spec = open(MODEL, encoding="utf-8").read()
inject = '  <visual><global offwidth="%d" offheight="%d"/></visual>\n</mujoco>' % (W, H)
spec = spec.replace("</mujoco>", inject)
open(TMP, "w", encoding="utf-8").write(spec)

m = mujoco.MjModel.from_xml_path(TMP)
d = mujoco.MjData(m)

kid = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_KEY, "stand")
if kid >= 0:
    mujoco.mj_resetDataKeyframe(m, d, kid)
else:
    mujoco.mj_resetData(m, d)
mujoco.mj_forward(m, d)

# hide the floor: this is a mechanism drawing, not a scene
for gid in range(m.ngeom):
    if m.geom_type[gid] == mujoco.mjtGeom.mjGEOM_PLANE:
        m.geom_rgba[gid] = [1, 1, 1, 0]

cams = [
    dict(azimuth=90, elevation=-4, distance=1.75, lookat=[0.03, 0.0, 0.55]),
    dict(azimuth=140, elevation=-10, distance=1.85, lookat=[0.03, 0.0, 0.55]),
]

tiles = []
r = mujoco.Renderer(m, height=H, width=W)
for c in cams:
    cam = mujoco.MjvCamera()
    cam.type = mujoco.mjtCamera.mjCAMERA_FREE
    cam.azimuth, cam.elevation, cam.distance = c["azimuth"], c["elevation"], c["distance"]
    cam.lookat[:] = c["lookat"]
    def shoot(seg):
        if seg:
            r.enable_segmentation_rendering()
        else:
            r.disable_segmentation_rendering()
        opt = mujoco.MjvOption()
        opt.geomgroup[3] = 0
        opt.geomgroup[4] = 0
        r.update_scene(d, camera=cam, scene_option=opt)
        for flag in (mujoco.mjtRndFlag.mjRND_SHADOW, mujoco.mjtRndFlag.mjRND_REFLECTION,
                     mujoco.mjtRndFlag.mjRND_SKYBOX, mujoco.mjtRndFlag.mjRND_HAZE):
            r.scene.flags[flag] = 0
        return r.render()

    rgb = shoot(False).astype(int)
    seg = shoot(True)
    mask = seg[:, :, 0] >= 0
    out = np.full_like(rgb, 255)
    out[mask] = rgb[mask]
    tiles.append(Image.fromarray(out.astype(np.uint8)))
r.close()
os.remove(TMP)


def to_white(im):
    """The renderer clears to the skybox colour; repaint the flat background white."""
    a = np.asarray(im.convert("RGB")).astype(int)
    bg = a[2, 2]
    mask = np.abs(a - bg).max(axis=2) < 30
    a[mask] = 255
    return Image.fromarray(a.astype(np.uint8))


def trim(im, tol=10):
    a = np.asarray(im.convert("RGB")).astype(int)
    mask = (255 - a).max(axis=2) > tol
    ys, xs = np.where(mask)
    if len(ys) == 0:
        return im
    pad = 14
    return im.crop((max(xs.min() - pad, 0), max(ys.min() - pad, 0),
                    min(xs.max() + pad, im.width), min(ys.max() + pad, im.height)))


for i, t in enumerate(tiles):
    t.save(os.path.dirname(os.path.abspath(__file__)) + f"/preview/raw{i}.png")
tiles = [trim(t) for t in tiles]
h = max(t.height for t in tiles)
tiles = [t.resize((int(t.width * h / t.height), h), Image.LANCZOS) for t in tiles]
gap = 60
sheet = Image.new("RGB", (sum(t.width for t in tiles) + gap, h), "white")
x = 0
for t in tiles:
    sheet.paste(t, (x, 0))
    x += t.width + gap
sheet.save(OUT)
sheet.save(os.path.dirname(os.path.abspath(__file__)) + "/preview/fig_robot.png")
print("wrote", OUT, sheet.size)
