# Fil rouge, DASH-01

Purpose of this file: the thread of the argument, chapter by chapter. Ideas to string together, not prose.
Style rules for the thesis itself: nominal sentences where possible, no editorializing, no em dashes, no reader address.
Two further bans, added after the aphorism sweep. No gnomic maxims: a general truth in the present tense with no number, scope or citation attached.
No essentialist predication: "X is what Y is made of", "pays for itself", "is a deliverable". Test: delete the sentence, and check whether anything downstream loses an input.
Repair ladder, highest rung you can pay for: replace with the measurement; scope it to the population the evidence covers; downgrade the modality and name the test that would settle it; mark it "in my view"; cut.

Convention for status tags used below:
`[done]` written in the current .tex, `[partial]` written but incomplete or unverified, `[new]` to write, `[open]` decision still open.

---

## Target structure and file mapping

Requested shape, against the current files:

| Ch | Title | Current source | Action |
|----|-------|----------------|--------|
| 1 | Introduction and context | `Chapters/ch1.tex` | rewrite around the speed objective |
| 2 | Background and literature review | `Chapters/ch2.tex` | add definitions block, add RL-specific axes |
| 3 | The robot and its digital twin | `Chapters/ch3.tex` sec. 3.1 to 3.6, 3.10, 3.11 | split out of the current monolithic ch3 |
| 4 | Reinforcement learning: attempts and architecture | `Chapters/ch3.tex` sec. 3.7 to 3.9 | split out, promote to its own chapter |
| 5 | Results | `Chapters/ch4.tex` | keep, add the run video |
| 6 | Discussion | `Chapters/ch5.tex` | reorient toward "what to change to reach the target" |
| 7 | Conclusion and future work | `Chapters/ch6.tex` | keep |
| A | Appendix | `Chapters/append.tex` | keep |

Split mechanics: `ch3.tex` currently 2639 lines. Cut at `\subsection{Toy problem}` (line 1149). Deployment and hardware experiments (sec. 3.10, 3.11) stay with the robot chapter, since they are plant work rather than learning work.

---

## Cross-chapter narrative thread

One sentence per chapter, to be checked for consistency at the end:

1. Objective: high running speed on a cheap custom biped.
2. Field context: where stability comes from, what each family demands of the hardware, why learning at the gait-parameter level is the candidate for this plant.
3. The plant, as built and as measured: every assumed parameter replaced by a number.
4. The controller: five action spaces, one curriculum, the measured verdict on each.
5. What the robot and the policies actually do.
6. Distance from the objective, and the ranked levers that close it.
7. Recap and directions.

The recurring motif: **the binding constraint moves from the algorithm to the plant.** Introduced in ch2 (each control family demands something of the hardware), demonstrated in ch3 (every measurement pessimistic), confirmed in ch4 (pitch wall identical for RL and for a 21-gain scripted controller), quantified in ch6.

---

# Chapter 1: Introduction and context

Goal: state the objective, the platform, and the honest scope.

Ideas to string:

- Context: REHAssist, DASH-01, two legs, six quasi-direct-drive actuators, parallel 4-bar knee, passive ankle, student budget, single-board computer.
- Objective as stated at kickoff: maximum running speed, ambition of the bipedal speed record.
- Objective as it survived the year: record pace moving faster than one master thesis (new records at a monthly cadence), hence reframing from "record contender" to "measured demonstrator plus reusable method". State this in chapter 1, not as a late concession.
- The problem addressed: RL locomotion results exist on research platforms; reproduction on a new, imperfectly known, low-cost robot is a different problem, dominated by modelling fidelity, actuator bandwidth and instrumentation.
- Starting point: partially finished mechanical design. Work begins at hardware selection for the non-mechanical subsystems and at modelling.
- The five side quests, as the project's spine:
  1. finish the robot: battery, sensor and actuator selection, compute;
  2. learn RL and the sim2real problem, on a toy plant, while the robot did not exist;
  3. model the robot at usable fidelity;
  4. characterise the physical robot to bound sim2real risk;
  5. produce a policy that works.
- Sensor scope note: IMU plus proprioception only. Foot impact sensors dropped for time, not for evidence. Literature prior suggested foot feedback helps. Never measured here. Hardware provision left in place (4 analog inputs on the sensor hat).
- Contributions, short list: actuator database and figure of merit, cell and pack database, CAD to MJCF pipeline with loop closure, measured plant table, capability analysis, action-space and curriculum design, failure catalogue, deployment stack.
- Reading map: one paragraph, chapter by chapter.

Open:
- `[open]` Title alignment. Current title claims the speed record. Either keep and let ch1 reframe explicitly, or retitle toward "framework and measured envelope".

---

# Chapter 2: Background and literature review

Goal: not a chronological list of papers. A multidimensional frame in which DASH-01's own choices become a position rather than an opinion.

## 2.0 Definitions [new]

Requested addition. Vocabulary block, placed before the history so the history can use the words.

- Purpose statement: "stable" as an overloaded word in this field, with at least six inequivalent meanings.
- The ladder of stability definitions, each with its inequality, its assumption and its cost:
  - **Static stability**: centre of mass projection inside the support polygon. Assumption: quasi-static motion, flat feet, flat ground.
  - **ZMP stability**: zero moment point inside the support polygon. Buys dynamic walking. Still assumes a non-degenerate contact patch, so unavailable with point feet.
  - **Orbital / periodic stability**: spectral radius of the linearised Poincaré map below one. The stability object is a limit cycle, not a state. Natural language for hybrid dynamics with impacts.
  - **Capturability**: existence of a reachable foot placement bringing the reduced model to rest. N-step capturable. The capture point as the natural target of a foot-placement controller.
  - **Viability**: current state inside the set from which locomotion can continue. The weakest rung of the ladder, and the one that assumes least. Failure defined as leaving the viability kernel rather than as falling.
  - **Robustness**: size of the disturbance set tolerated. Push impulse, terrain error, model error, delay, sensor noise. The definition an RL practitioner is implicitly optimising.
  - **Task-level performance**: velocity, cost of transport, terrain range, agility. Not stability at all, but usually what the reward encodes.
- Companion definitions in the same block: underactuation, base degrees of freedom, unilateral contact, friction cone, centre of pressure, flight phase, stance and swing, gait phase, cadence, duty factor, cost of transport, basin of attraction, reduced model / template, sim2real gap, domain randomisation, action space, curriculum.
- Definitions used by this thesis, stated explicitly: failure as episode termination on body contact or on leaving the viability proxy; "stability margin" measured as survivor count and seed variance, not as a scalar reward; the free-topple time of the inverted pendulum as the reference timescale.
- Sentence linking the block forward: each historical family answers "where does the stability come from", using one of these definitions.

## 2.1 What makes bipedal locomotion hard [done, keep]

Existing text is sound. Keep the three-consequence structure and the running-versus-walking distinction.

- Underactuation: six leg motors, twelve degrees of freedom, six base degrees with no motor. Ballistic centre of mass in flight. Structural echo: the curriculum releases base degrees one at a time, and the failing milestone names the uncontrolled mode.
- Unilateral and saturating inputs: push not pull, friction cone, centre of pressure confined to the contact patch, point foot as a degenerate patch. Foot placement as the principal input, discrete and workspace-bounded.
- Short timescales: `sqrt(h/g)` about 310 ms for this robot, contacts of tens of milliseconds, correction to be planned and mechanically executed inside that window. Actuator bandwidth as a first-class constraint. Forward hook to the measured 0.8 Hz drive pole.
- Running as bounce rather than vault: falling centre of mass at mid-stance, aerial phase, different reduced model. Frameworks built for walking do not extend by raising the commanded speed.
- Reduced models introduced once and reused: inverted pendulum, SLIP, capture point.

## 2.2 Historical narrative [done, keep as the spine]

Keep the "six answers to one question" structure. It is the narrative axis. Add the survey anchors.

- Static and ZMP, geometry-based. Slow motion, large flat feet, kinematic gait generation, trajectory then inverse kinematics then joint servoing. Honda, HRP, ASIMO family.
- Passive dynamics: stability from the mechanism. Lowest cost of transport of the six families (Collins et al. 2005), near-zero control authority.
- SLIP and series elasticity: stability from elasticity, correct template for running, spring rate fixed in hardware.
- Foot placement, Raibert lineage: one decision per step, near model-free, running with point feet.
- Hybrid zero dynamics: stability as a certified limit cycle, proof against the model.
- Optimisation-based control: MPC and whole-body, constraints first-class, demands high-bandwidth torque control.
- Learned control: stability from experience over a distribution, no contact model needed, reward becomes the specification.
- Closing observations, both already written and worth keeping: the families are complementary rather than sequential; over fifty years the stability burden transfers from the controller to the robot and to the model.

## 2.3 Analytical axes [new, the main addition]

The point of the rewrite: the historical account is the narrative, the axes are the analysis. Not "classical then MPC then RL", which is too linear and hides the actual research question.

Axes to treat, each in a short subsection with one figure or table:

1. **Dynamic model complexity.** Kinematics, static equilibrium, ZMP, LIPM, centroidal, full rigid-body, full dynamics with contacts, learned. Central trade-off: model fidelity against computational tractability.
2. **Stability concept.** Reuse the ladder of 2.0. Historical drift from static to viability and robustness.
3. **Where the intelligence sits.** Fully model-based stack, model-based plus online optimisation, hierarchical learning (RL emits a task or motion, model-based layer executes), end-to-end RL. Statement to include, cited to Hu et al. 2023 and Gu et al. 2025 rather than asserted: RL has not replaced model-based control, and most working systems are hybrids.
4. **Actuation interface.** Position, velocity, torque, impedance and admittance. What each commands, what each hides. Position servo: simple, robust, but poor contact-force authority and actuator dynamics folded into the plant. Torque: direct access to the physical dynamics, prerequisite for momentum and force control. Impedance as the intermediate category, and the one this thesis ends up in.
5. **Bandwidth and temporal hierarchy.** Task 1 to 10 Hz, gait and MPC 10 to 100 Hz, whole-body 100 to 1000 Hz, current loop 1 to 20 kHz. The distinction: **command-loop rate is not actuator bandwidth.** Measured here as a 200 Hz policy against a 0.8 Hz drive pole. This is the axis on which DASH-01's central finding sits, so it earns its own subsection rather than a remark.
6. **Contact treatment.** Fixed contact assumption, planned discrete contacts, contact-aware optimisation with friction cones, learned contact behaviour. Increasing relevance from flat walking to running and rough terrain.
7. **Source of the gait.** Hand-authored trajectories, analytic generation (LIPM, HZD, passive), trajectory optimisation, motion imitation, RL with reference, reference-free RL.
8. **Prior placement**, already written and to keep: shape prior versus structural prior, and the four places to put the periodicity prior (reward, reference, generator, action space). DASH-01 in the action-space column.

Deliverable for this section: the era-by-axis table. Columns: era or approach, model, stability concept, planning, controller, actuation interface, adaptability. Rows: early humanoid, ZMP, LIPM, HZD, whole-body control, MPC, RL plus whole-body, end-to-end RL. This table is the section's contribution, since it lets DASH-01 be placed by row and column rather than by adjective.

Survey anchors to read and cite `[new]`, to be added to `References.bib`:
- Hurmuzlu, Genot and Brogliato 2004, Automatica 40(10) 1647-1664. Hybrid-systems foundation, impacts, periodic-orbit stability.
- Grizzle et al. 2014, Automatica 50(8) 1955-1988. Control-theoretic structure of 3D walking, underactuation, Poincare stability. Priority read.
- Hu et al. 2023, IET CIM 5(3) e12080, doi 10.1049/cim2.12080. Three-way classification: model-based, stability-criterion-based, learning-based.
- Gu et al. 2025, arXiv 2501.02116. Model-based to RL and imitation transition. Priority read.
- Bao et al., DRL for bipedal locomotion survey. Decomposition into end-to-end, hierarchical, reference-based, reference-free, sim2real.
- Kim et al. 2025, reality-gap study. Experimental separation of dynamics randomisation, history, delay, noise, perturbation, architecture.
- Rudin et al., massively parallel training and game-inspired terrain curriculum.
- Li et al., curricular hindsight RL, multi-axis adaptive curriculum on a quadruped.
- Xie et al. 2020, sim2real end-to-end RL on Cassie.

## 2.4 RL for locomotion: the specific lineage and the three trade-offs [partial, extend]

Existing subsection covers the lineage. Add the three trade-off subsections the thesis actually lives on.

Lineage, keep:
- Periodically parameterised action spaces: PMTG, oscillator CPG-RL, clock and phase rewards (Cassie, 100 m record).
- Truncated Fourier series gait generators predate this work by more than a decade (RoboCup humanoids, particle swarm; Fourier plus RL; rhythmic DMPs). The basis is not the contribution. The contribution is placement plus the measured comparison.
- The one unambiguous constraint from the mid-project review: no published system runs with per-cycle-only parameter updates and no intra-cycle feedback path. Every working system keeps a per-step observation-to-action channel. This is why the reflex and residual channels exist.

**Trade-off A: sim2real gap.**
- Sources, ranked as measured here rather than as usually listed: actuator dynamics and drive bandwidth, mass and inertia error, contact and friction model, latency, sensor noise, unmodelled compliance.
- Standard toolkit: domain randomisation, curricula over randomisation, observation history in place of privileged state, explicit sensor and delay models, actuator networks.
- The framing to adopt: domain randomisation as robustness training over a distribution of plants, not as noise injection.
- Position of this thesis: measurement first, randomisation around the measurement. Ablation showing which components carried the cost.
- The counter-lesson: randomisation around an optimistic plant does not recover the plant error. No policy has run on hardware here, so state it as an inference from the plant-correction table, not as a transfer result.

**Trade-off B: learning efficiency and dimensionality reduction.**
- The raw problem: torque sequences in `R^(n_joint x T)`.
- The structured problem: 10 to 50 gait-morphology parameters, `R^(n_fourier)`.
- The prior being asserted: successful locomotion approximately periodic, band-limited, bounded.
- What the reduction buys: exploration removed rather than answers imposed. Contrast with a shape prior, which shrinks the reachable set.
- The cost: reachable set bounded by the number of harmonics; stability not guaranteed by smoothness; the need for a fast feedback channel outside the generator.
- Sample-budget context to state honestly: modern results use `1e8` to `1e9` transitions with thousands of parallel environments. A curriculum optimal at that budget is not necessarily optimal at this project's budget. Sample efficiency as the actual research variable here.

**Trade-off C: curriculum design.**
- State of the art axes: command range, terrain, disturbance, domain randomisation. Usually applied to an already fully dynamic robot.
- The recent shift: fixed hand-scheduled curricula to performance-adaptive curricula, keeping success rate near 0.7 to 0.9; one difficulty scalar to a difficulty vector.
- What this thesis does differently: the curriculum changes the **controllability of the robot**, and not only the difficulty of the environment. Check against the 2.4C survey before claiming novelty. Constraint release on base degrees of freedom is a continuation strategy on the plant itself.
- What this thesis does not yet do, and should say so: binary rather than continuous constraint release, hand-scheduled rather than performance-gated advance, single difficulty axis rather than a vector.
- The known danger to state: a strongly constrained plant lets the policy learn that a suppressed mode does not exist. Release then produces immediate failure. Mitigation: disturbances before release.

## 2.5 Platforms, and where DASH-01 sits [done, keep]

- Series-elastic research bipeds (ATRIAS, Cassie, Digit): purpose-built spring-mass systems, high bus voltage, record holders, institutional cost.
- MIT Cheetah lineage: quasi-direct drive commanded in torque mode. The pattern nearly every recent platform adopted, humanoids included.
- Hobby-class humanoids: position-controlled smart servos, confined to static walking, for a structural reason and not a budget one.
- DASH-01 between groups two and three. Three defining bets: parallel 4-bar knee moving actuator mass proximally, passive ankle spring replacing two motors, six motors doing the work of ten.
- The servo-mode question `[partial, needs rewrite]`: default landed on servo position mode after torque mode and position mode both bit. Why MIT-style command mode (position, velocity, Kp, Kd, feedforward torque in one frame) gives torque-control properties at a slow outer loop without the servo-mode ceiling. Cubemars driver documentation as the practical cause.
- `[open]` How to write the period of being wrong about the drive mode. Proposed convention, to apply everywhere in the thesis: state the measured premise, state the decision taken on it, state the later measurement that overturned it, in that order, in one paragraph. Record the failure as a datum, with no self-commentary. Apply the same convention to the torque-control abandonment in chapter 4.

## 2.6 Gap and research questions [new]

Closing section of the chapter, so chapter 4 has something to test.

- The gap: published structured-action-space results come from platforms with high-bandwidth torque control. What survives on a low-bandwidth, position-servo, low-cost plant is not documented.
- The reframed research question, stronger than "why RL": **at what level should learning sit, given this robot's actuator dynamics and available control bandwidth?** `RL -> q_d -> servo` and `RL -> tau -> actuator` are different learning problems, because the first forces the policy through the closed-loop servo dynamics.
- Hypotheses, to be answered in chapter 5 and revisited in chapter 6:
  - H1, dimensionality reduction: Fourier gait morphology converges in fewer environment steps than joint-level action spaces.
  - H2, control authority: gait morphology plus phase-dependent impedance gives a sufficient basin of attraction without direct residual joint control.
  - H3, robustness: the structured controller degrades less across the sim2real boundary than an unconstrained one.
- Honest scoping sentence: H1 answered by the attempt sequence, H2 answered partially, H3 answered only in simulation, since no policy has run on the hardware.

---

# Chapter 3: The robot and its digital twin

Goal: finish the robot, build the twin, replace every assumption with a measurement. The chapter that makes chapter 4's results interpretable.

## 3.1 Build completion and hardware selection

- Starting state: partial mechanical design, nothing electrical.
- **Actuators.** Selection criterion: torque density, cheap, close in specification to Sonceboz. The actuator map and figure of merit `K_m = K_t/sqrt(R)`, winding-invariant, with explicit electrical reference frames. Database: 140 actuators, 121 motors, 121 gearboxes, 9 drives, 8 vendors.
- Cubemars driver as the practical cost: undocumented internal loops, mode switching not achievable in the time available.
- **What the selection got wrong** `[done]`: the post-hoc audit. Actuator choice Pareto-optimal in class by the figure of merit. Error located at the drive interface, not at the actuator.
- **Battery.** Pack map tool, roughly 430 cells, 54 BMS modules, 110 packs, duration-stamped current tiers, pack synthesiser. As-built: 13S2P, 480 Wh, 250 A peak. The error found by the audit: peak current rating quoted without a duration.
- **Compute.** Raspberry Pi 3B. Rationale: small policy, multi-core so time-critical work can be pinned, real-time kernel possible, CAN via a commercial SPI hat. Contrast with BeagleBone: single core, slower, PRU usable but expensive in development time.
- **Sensors.** IMU on the hat at 200 Hz, provenance-labelled noise figures. Four analog inputs available. Foot impact sensors provisioned and never implemented, so the literature prior about foot feedback remains untested here.

## 3.2 The digital twin

- CAD re-assembly to exportable model. The pipeline is a contribution, so it is written as a procedure.
- **URDF cannot express this robot**: serial-tree format against a hybrid serial-parallel leg. Loop closed after export, in MJCF.
- Validation of the twin, stated as a chain rather than as a claim: analytic Jacobians against finite differences; loop closure against the measured backdriven workspace, 2789 poses, 100 percent; known movements with measured torque against prediction.
- Inertia handling: manual weighing per segment to reduce the number of free parameters when calibrating the inertia matrices.
- Simulator choice: MuJoCo, CPU. Reasons: contact modelling, no recent Nvidia hardware requirement. Cluster access removed the throughput bottleneck.
- Compute backend: SCITAS cluster, ssh plus python jobs.
- "Establishing that a simulation result is real": the self-test and smoke-gate discipline, motivated by the six wrong-but-converged results catalogued later.

## 3.3 Characterisation: replacing assumptions with measurements

Framing sentence for the section: **every assumed plant parameter that was later measured moved in the pessimistic direction.** Mass +18 percent, torque -15 percent, drive bandwidth -16x, plus friction and the ankle.

- Mass: per-segment weighing, table, plus 18 percent against assumption.
- Peak torque: what the gearbox delivers rather than what the datasheet quotes, minus 15 percent.
- Drive position loop: Bode against a commanded sine, per actuator. 0.8 Hz pole, tau 199 ms, 25 ms delay. Against a 310 ms divergence time. Factor 16 against assumption. The chapter's headline measurement.
- Ankle spring: dynamometer plus deflection angle. One order of magnitude too soft. Replaced by a rigid link, then by the carbon strut.
- System identification, including what it could not resolve: link inertia tensors, 0.9 N.m gravity residual, kinematic model as the remaining suspect. Stating the un-resolvables is part of the contribution.
- Loop timing and CAN: two 1 Mbit buses, 26 percent utilisation, protocol as measured rather than as documented.
- Workspace: measured backdriven envelope, used both to validate the twin and as a runtime safety net.
- Static end-effector force map: toe-force ellipse, 19:1 anisotropy at the standing pose, strong vertically and weak in the propulsive direction. The measurement that closes the ankle question.

## 3.4 Capability analysis: the ceiling before any controller

- Purpose: a speed ceiling from first principles, so learned results are judged against physics rather than against hope.
- Method, results, limiting factors. 87 percent of feasible gaits limited at the peak-power corner of the cam.
- Sensitivity: distal mass at -0.93 (m/s)/kg against torso mass at -0.11. Factor nine. The binding design axis, and lever 2 of chapter 6.
- Ankle stiffness threshold, recovered independently by the analysis and by RL.
- The corrected ceiling on the measured plant: about 2.7 m/s burst, about 1.3 m/s thermally sustained. Against a record pace near 4 m/s. This number reclassifies the project, and it belongs here rather than in the conclusion.
- Limitations: sensitivity propagation awaiting a full re-sweep, actuator model without a coupled torque-speed envelope and therefore optimistic exactly at high speed.

## 3.5 Deployment stack

- 200 Hz daemon on stock Linux, no real-time kernel. 3 percent late ticks, half the budget spare. A/B against the SSH-load measurement that produced a wrong committed conclusion.
- CAN at runtime, the drive as deployed, the safety envelope used as an instrument.
- Web bring-up instrument, which carried most of the measurement campaign.
- Three-tier flight recorder plus pre-move guard. Built after a hardware failure, validated by reproducing it. Found a daemon-killing crash and a dead bus within its first hour.
- The incident: left leg lost to a calibration failure before any policy reached the robot. One incident, stated plainly, and the reason the pre-move guard exists.

---

# Chapter 4: Reinforcement learning

Goal: the long chapter. Every action space tried, why each failed or worked, and what the failures measure. Structured as a ladder of control authority, since that is also the ablation the thesis wants.

## 4.1 Common ground

- Formulation: observation, action, reward, termination, episode. PPO. Training budget per milestone, roughly 600 M steps, large rather than asymptotic.
- Toy problem first: single-joint inverted pendulum, end to end through train, export and deploy, at minimum stakes. The chain debugged at one degree of freedom.
- Reward structure, and the standing statement: the reward is the specification, and the optimiser satisfies the specification rather than the intent. Evidence is the exploit catalogue of 4.6, not assertion.
- Evaluation protocol, six rules, each earned by a specific bug, with four evaluation bugs that nearly discarded or crowned the wrong policy: training aids forced off at evaluation; fixed task across curricula; at least 20 seeded episodes; paired seeds and survivor counts under bimodality; peak rather than final under one-way curricula; `curriculum.json` as ground truth on restore.
- The diagnostic to promote to a general lesson: **seed variance is the margin measurement.** 20.3 +/- 21.6 s against 5 of 5 at the cap is bimodality, not a worse mean.

## 4.2 The action-space ladder

Present as a ladder, with the same plant and reward wherever possible, so it reads as an ablation:

1. **Direct joint torque** `[done]`. Never converged. Judged undeployable on premises that later measurement partly overturned. Two failures, one on convergence and one on the reasoning behind abandonment. Write it with the convention from 2.5.
2. **Joint position targets, per step PD** `[done]`. Converged to standing. Skating. The reward-exploit catalogue starts here.
3. **Impedance and phase-dependent impedance** `[new, mostly design-level]`. Status to state honestly: designed, not run. Content: `tau = Kp(phi)(q_d - q) + Kd(phi)(qdot_d - qdot)`, mapping onto the MIT-style command frame `[q_d, qdot_d, Kp, Kd, tau_ff]`, the three levels of impedance freedom (fixed nominal profile, scalar scaling `alpha_p, alpha_d`, small Fourier correction `Delta Kp(phi)`), and the argument for coupling impedance to the gait rather than giving it an independent coefficient set. Why it was not run: drive mode never switched on the hardware, so the interface did not exist. Why it is the first item of future work.
4. **Fourier CPG** `[done]`, the architecture that works. Gait phase as the single organising coordinate, `phidot = omega`, contralateral leg at `phi + pi`, joint targets as a truncated series, analytic `qdot_d` rather than numerical differentiation, coefficients re-emitted every step, mirroring across legs, N = 3 throughout with no sweep over N. Smoothness as a penalty on `||theta_t - theta_(t-1)||^2` rather than as a hard bandwidth limit. State the alternatives not compared: action filtering, rate limits, parameter derivatives.
5. **Reflexes and residual, the bypass channels** `[done]`. The literature constraint from 2.4: no working system runs with per-cycle-only updates. Which reflexes are hard-wired (capture-point pitch reflex) and which are learned. The per-step residual channel. Framing: the prior did not vanish, it moved into the action space and stayed hand-wired at the one channel where feedback must not be blind.
6. **Explicit-oscillator CPG A/B** `[done]`. Identical plants and rewards. Verdict: tie by measurement, complementary strengths. Oscillator produced the single best controller and the only one executing the stop phase, and walls at roll. Fourier passes roll.

## 4.3 Curriculum

- As implemented: base-DOF release, one degree at a time, rigid rails, constant observation and action shape, warm start carried across plants. Continuation rather than retraining.
- What the mechanism buys: failure localised to a single degree of freedom, since the milestone that fails names the mode.
- The three rules learned the hard way: gate the advance and not only the opening; never gate a rescue ramp on the competence it rescues; diff configurations against the last working run before theorising.
- Deadlocks and bugs: the warm-start bug that silently duplicated every seed replicate; the 25 Hz gait-clock bug, where a range widened to be non-binding became the operating point because a neutral network output decodes to mid-range.
- **Comparison against state of the art** `[new]`, feeding 2.4C: fixed schedule against performance-gated advance; single axis against difficulty vector `D = [D_dof, D_terrain, D_disturbance, D_command, D_randomisation]`; binary release against continuous virtual stabilisers `F_z = -K_z(z - z_0) - D_z zdot` with `K_z -> 0`.
- What this project's curriculum has that the state of the art does not: difficulty applied to the plant's controllability rather than to the environment.
- Proposed successor design, written as future work rather than as a result: soft constraint release, disturbance ramp introduced before full release to prevent the rail exploit, advance gated on maximum recoverable impulse rather than on step count, randomisation present from stage zero rather than appended at the end.

## 4.4 The pitch wall

- The chapter's central negative result, and the one that transfers the burden to the plant.
- Symptom: failure at about 1 s, matching analytic free-topple time, across a 5x gravity sweep.
- Cross-check: a 21-gain scripted controller (capture point plus clocked gait, no learning) fails identically, and beats RL on the constrained plant. Same wall, two methods.
- Only a 12x ankle stiffening breaks it in simulation.
- Survives the drive retune to 3 Hz, so it is structural rather than bandwidth-limited.
- The interpretation to state carefully: at the wall the comparison between methods is vacuous, since an empty feasible set makes every controller drawn from it identical. RL optimises over controllers, not over physics.
- Consequence for H2: control authority is not the binding constraint at the wall, the plant is.

## 4.5 Sim2real work in simulation

- The drivable-demonstrator lineage: descent to the measured 0.8 Hz drive, 3x score gain over its parent.
- Diagnosis history as a result: steering asymmetry, domain-randomisation ablation, command-range fit.
- The ankle closed as a build decision: statics eliminate the soft spring, learning selects the compression-capable strut, buckling arithmetic rejects the fabricated part in favour of carbon.
- The postscript plant: rebuilt robot, carbon ankle, 3 Hz drive, velocity caps. Scripted controller completes stand, forward, backward, stand, 35 s, 3 of 3 seeds.

## 4.6 Negative results and simulation hygiene

- Reward exploits: skating, floor penetration, shuttling, suicide by penalty. Also gamed by the scripted controller's coordinate-descent tuner, which is the evidence that optimisers rather than networks are the culprit.
- Simulation artefacts that produced clean, converged, wrong results: soft joint limits, constraints inactive at settle, frame-relative safety checks, stale keyframes, a solver-version split, and an actuator velocity cap that was never present, which let a policy balance at 23 rad/s on a 22 rad/s motor.
- Evaluation bugs, four of them, each of which nearly discarded or crowned the wrong policy.
- The 6 Hz footfall chatter, surviving every post-hoc lever, awaiting a from-scratch retrain with cadence pressure from step zero.

---

# Chapter 5: Results

Goal: what exists, measured, with the video as a first-class artefact.

- Hardware delivered: 15.14 kg, 14.72 kg after the carbon-ankle rebuild. Six actuators, 13S2P 480 Wh pack, 200 Hz loop at 3 percent late ticks, two CAN buses at 26 percent, characterised IMU, full plant-correction table.
- Corrected capability: about 2.7 m/s burst, about 1.3 m/s sustained.
- RL results table as the headline: milestone ladder to a 6-DOF-free plant, 60 s without falling at 2.6 m/s, cadence-fixed variant at 2.71 m/s, about 70 percent of the pre-correction ceiling.
- Action-space verdicts, one line each, keyed to 4.2.
- Generator A/B verdict.
- Pitch wall as a measured result rather than as an anecdote.
- Rebuilt-plant mission: first full command-following sequence.
- Sim2real lineage result on the measured drive.
- **Run video** `[new]`: the deliverable the chapter currently lacks. Needs a still strip in the PDF (milestone ladder frames, scripted m2 and m3 failure stills), a caption stating plant, policy, seed and playback rate, and a QR code or short link to the recording. State clearly what the video shows: simulation, or the tethered robot, or the scripted mission. No ambiguity between simulated and physical footage.
- Figures still missing `[new]`: one learning curve per lineage, the milestone strip, the toe-force ellipse, the Bode plot of the drive, the plant-correction table as a figure.

---

# Chapter 6: Discussion

Goal per the brief: what to change on the robot to reach the target. Ranked, with the measurement that ranks it.

- Restate the distance: 1.3 m/s sustained against a 4 m/s record pace. The gap is mechanical and actuation-level: the 21-gain scripted controller hits the identical pitch wall, so no algorithm closes it on this plant.
- **Verdict on the hypotheses.** H1 supported: the structural prior turned a non-converging problem into a trainable one, and the torque attempt is the control. H2 partially supported: reflex and residual channels were necessary, so gait morphology alone was not sufficient, and the impedance level was never tested. H3 untested on hardware.
- **Ranked levers for a successor robot**, each with its number:
  1. Bus voltage before torque. 87 percent of gaits limited at the peak-power corner. Over that 87 percent, speed scales with no-load speed and is insensitive to peak torque. Scope is the sweep as run. Cost: pack mass plus a drive rated for the voltage.
  2. Distal mass. -0.93 (m/s)/kg, nine times the leverage of torso mass. Carbon shin plus a proximally mounted spring on a tendon recovers about 0.5 m/s. Cost: a composite part and a tendon route to design.
  3. Re-proportion or replace the 4-bar. Only 0.20 to 0.35 m usable out of a 1.06 m geometric span. Standing at 96 percent of reach, toe-force ellipse 19:1 anisotropic in the wrong direction. Target a flat transmission ratio over about 0.5 m, stance at about 85 percent of reach.
  4. Size the ankle for 3.5 body weights. Present passive ankle at 0.42 BW median, 8x short, failing in positive mechanical feedback.
  5. Cool the cam motor. 167 N.m demanded against 55 N.m continuous. Winding temperature is unvalidated (ch3 flags it), so state cooling as an unquantified lever plus the test that would quantify it, not as a thermal verdict.
  6. Torque-mode control as an architectural requirement from day one. Abandoned twice, once on convergence and once on assumed deployability, and the measured 0.8 Hz drive loop points back to it. No number attached, so mark it a design opinion rather than a ranked result.
- **Levers for this robot, in order of what unblocks what**: ONNX export plus Pi inference; current-mode control with the PD closed on the Pi at 200 Hz; carbon ankle strut; from-scratch cadence retrain; then the phase-dependent impedance experiment, which the first two make possible.
- **Method-level lessons**, kept from the current chapter 5 and trimmed to the ones that generalise:
  - Optimisers exploit objectives. Evidence: PPO and the scripted controller's coordinate-descent tuner gamed the same objective identically, so it is not a neural-network property.
  - The margin advantage of learning rests on three premises, none paid in full here: an exact plant (every parameter moved), a reward pricing distance from the failure boundary (it priced survival and distance), and an asymptotic budget (600 M steps is large, not asymptotic). Diagnostic: seed variance is the margin measurement.
  - Gait priors read on two axes: a shape prior fixes the trajectory, a structural prior constrains the class. Evidence the wider space was used: cadence agreement between the learned optimum and the independent physics sweep. Mark the framing as opinion, not measurement.
  - Every assumed parameter measured later moved pessimistically: mass +18 percent, torque -15 percent, drive bandwidth -16x, plus friction and the ankle. Measure before training, and apply the measurement as the plant rather than as an optional variant.
  - Six simulation artefacts each produced a clean, converged, wrong result: soft joint limits, constraints inactive at settle, frame-relative safety checks, stale keyframes, a solver-version split, and an absent actuator velocity cap that let a policy balance at 23 rad/s on a 22 rad/s motor. Self-tests, smoke gates or measurement caught each.
  - Evaluation protocol: six rules, each earned by a specific bug, and four evaluation bugs that nearly discarded or crowned the wrong policy.
  - Instrumentation found the drive ceiling, and the flight recorder found a daemon-killing crash and a dead bus in its first hour. Cost: the measurement disturbed the measured twice (IMU on a swaying rig, loop rate under SSH load), once producing a committed wrong conclusion that only an A/B retracted.
  - Progressive validation localised the failures in this project: the base-DOF ladder to single degrees of freedom, the toy problem to one degree of freedom in the deploy chain.
- **What a successor project should do differently at the method level**: design search in simulation over bus voltage, gear ratio, distal mass, linkage proportions and ankle stiffness. Search over robots rather than over controllers for a robot already known to be the constraint.

---

# Chapter 7: Conclusion and future work

Classic recap, scientific register, no new material.

- What was set out to do, in one paragraph.
- What was delivered, in three items: a working method (modelling, training and curriculum stack producing a 2.6 m/s never-falling runner in simulation); a measured robot (every load-bearing parameter replaced by a measurement, with stated uncertainty and stated un-resolvables); an account of the distance between the two.
- Answer to the reframed research question of 2.6, in one sentence: on a plant whose actuation bandwidth is an order of magnitude below the divergence timescale, the level at which learning sits matters less than the level at which the actuator is commanded. Evidence: RL and the 21-gain scripted controller hit the identical pitch wall.
- Limitations, listed once: no policy on hardware, sprint results on privileged observations, inertia tensors and gravity residual unresolved, actuator model without a torque-speed envelope, corrected ceiling awaiting a re-sweep, robot standing on one functional leg.
- Future directions, short, pointing to chapter 6 rather than repeating it.

---

# Appendix

- Logbook.
- CAD to URDF to MJCF, step by step, with the repository link.
- Actuator review and database.
- Battery and pack review and database.
- Plant-identification protocols, per measurement.
- CAN protocol as measured.
- Reward and hyperparameter tables per lineage.
- Curriculum configuration schema.

---

# Working list

- `[new]` Add the six survey references plus Rudin, Li and Xie to `References.bib`.
- `[new]` Write 2.0 definitions block, and sweep all chapters so every use of "stable" points at one definition from it.
- `[new]` Write 2.3 axes and the era-by-axis table.
- `[new]` Extend 2.4 with the three trade-off subsections.
- `[new]` Write 2.6 gap and hypotheses, then close them in 6.
- `[todo]` Split `ch3.tex` at line 1149 into the robot chapter and the RL chapter, renumber the files, fix `\cref` labels.
- `[todo]` Record and embed the run video, plus the still strip.
- `[todo]` Rewrite the 2.1 intro paragraph flagged as weak.
- `[open]` Thesis title against the reframed objective.
- `[open]` Whether the impedance section sits in chapter 4 as a designed-not-run attempt, or in chapter 6 as future work. Current preference: chapter 4, since the brief asks for everything that was tried, and the design work was done.
- Style sweep at the end: nominal sentences, no boosters, no reader address, no em dashes, no gnomic maxims, no essentialist predication.
