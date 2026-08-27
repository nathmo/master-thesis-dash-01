# Figure sources

Every figure in the thesis is generated from the simulation archive, so a caption number and a
plot come from the same file. Regenerate with the `running_robot` virtualenv, from that
repository's root:

```
cd /path/to/running_robot
./.venv/Scripts/python.exe /path/to/thesis/Figures/scripts/make_figs.py
./.venv/Scripts/python.exe /path/to/thesis/Figures/scripts/make_leg.py
./.venv/Scripts/python.exe /path/to/thesis/Figures/scripts/render_robot.py
```

Edit the `RUNS`, `MODEL` and `OUT` constants at the top of each script if the paths move.

| Script | Output | Reads |
|---|---|---|
| `make_figs.py` | `fig_ladder.pdf`, `fig_experiments.pdf`, `fig_drive.pdf` | `training/runs*/<run>/progress.csv` and `resolved_config.json` |
| `make_leg.py` | `fig_leg.pdf` | `training/model/dash01.xml`, stance keyframe |
| `render_robot.py` | `fig_robot.png` | `training/model/dash01.xml`, stance keyframe |

## Which run backs which claim

`make_figs.py` reads these runs. The archive keeps duplicate copies of some of them, and some
copies are resume windows rather than full histories, so `load()` prefers the copy that starts
earliest and an explicit root overrides it.

| Thesis object | Runs |
|---|---|
| Milestone ladder (Fig. 5.1, Tab. 5.1) | `m2_sprint`, `m3_stiff_hi`, `m4_stiff`, `m5_stiff`, `m6_stiff`, `m7_freq` |
| Generator A/B, cold m3 (Fig. 5.2a) | `ab_cpg_cold_s0`, `ab_f_cold_s0` |
| Drive bandwidth bracket (Fig. 5.2b) | `m2drv_d12_s0`, `m2drv_d3_s0`, `m2drv_d08_s0` |
| Ankle screen, cold m3 (Fig. 5.2c) | `ankle2_m3_rigid_s0`, `ankle2_m3_bar_comp_s0`, `ankle2_m3_bar_s0`, `ankle2_m3_k350_s0` |

Episode length is converted from control steps to seconds using each run's own
`control_decimation` against the 1 ms physics step, so the 50 Hz sprint milestone and the 200 Hz
runs are on the same axis. The star markers in `fig_ladder.pdf` are the deterministic-evaluation
survival times of Table 5.1, which are entered by hand in the `arms` list because the greedy
evaluations are not in `progress.csv`.

The Bode data in `fig_drive.pdf` is the measured sweep of Section 3.4.3, entered by hand from the
identification campaign rather than read from a run directory.
