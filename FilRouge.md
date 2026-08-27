# Introduction 
## Problem statement
the goal of the thesis is to develop RL controller for a running robot.

the global context goal was to run as fast as possible but even if it might have been achievable a year ago, the new record that keep comming out every week make this endeavor futile in the scope of only one master thesis.

To do this we had to solve a few side quest :
1) get a robot, input to max design on battery design, sensor and actuator selection along with computer (but sensors was dropped to only IMU and prioception as no time to integrate impact sensor in foot. No time to even mesure if it would have been a useful additon. come from a prior from reading litterature that suggested that impact sensor / foot feedback might help.)
2) learn about RL and the issue with sim2real gap. -> toy problem since real robot was not available yet
3) model the robot with enough fidelity for the simulation and RL training.
4) caracterizing the physical robot limit to limit the sim2real risk.
5) actually comming up with a policy that work.

## Objectives of the Project

## Methodology Overview

## Contributions
-> actuator map
-> battery map
-> tuto to go from CAD to RL model


# Background and State of the Art 7
## 2.1 What makes bipedal locomotion hard
rewrite this intro. it sucks.
## 2.2 A short history: six answers to one question
### 2.2.1 Stability from geometry: static walking and the zero-moment point
good, similar to the problem for quadrupeds since they have large stability polygons.
### 2.2.2 Stability from the mechanism: passive dynamics
good
### 2.2.3 Stability from elasticity: spring-mass templates
the SLIP model, single regime
### 2.2.4 Stability from foot placement: the hopping lineage 

### 2.2.5 Stability from a provable limit cycle: hybrid zero dynamics
### 2.2.6 Stability from re-solving the problem: optimisation-based control
### 2.2.7 Stability from experience: learned control
MPC is nice but need very accurate model, maybe RL can help to improve the stability boundary. plus it need "less" prior on what walking/running is.
regarding the prior there are different place to hide it like in the reward function or controller architecture. Theses prior restrict the exploration space but can also reduce the the performance envelope. Thus good prior aim to maximing the "juicyness" of the space to explore to maximize the density of interesting things and weeding out the unlikely / useless possibility. (this also have the advante to remove some class of sim2real issue by killing at the root some way the policy could exploit the simulation.)
### 2.2.8 Summary

### 2.3 About gait prior
most controller or architecture assume as hand tuned gait cycle.
Some controller offer some tuning like the gait frequency, the phase between the leg and such but still on the prior of the shape of the foot movement.
This work fine as far as mimicry can go but when faced with new leg architecture that start to differ from an aldready existing one, method must be found to also discover the optimal gait shape. (shape prior vs structural prior)
Our approach is based of the prior that a gait is periodic and thus can be expressed as a fourrier serie.
This is not new and was done in work that are more than a decade old.
This work well to greatly decimate the search space but it also remove stability if done incorrectly.
we thus had to integrate a reflex mechanism to stabilize it shoulda disturbance occur.
Furthermore, we also add another prior in the sense of smoothness by penalizing abrut change in the fourrier serie term.


### 2.4 What learning should buy in stability margin
Good
## 2.5 RL for locomotion: the lineage of this architecture
good
## 2.6 Existing platforms, and where DASH-01 sits 
discuss about the "choice" / default of using servo mode after torque mode and position mode bited.
and why it can / cant work. (my failure to switch the mode on the drive)
explain that this is also the reason for the MIT cheeath control mode since can have the properties of a direct torque control but with a much slower loop whitouth the drawback of position servo mode.

(how should I document / write about me being wrong for a while ? just skip it and go straight to what was the correct call ? Bruh... )

# 3 Development Methodology 
1) get a robot, input to Max design on battery design, sensor and actuator selection along with computer (but sensors was dropped to only IMU and prioception as no time to integrate impact sensor in foot. No time to even mesure if it would have been a useful additon. come from a prior from reading litterature that suggested that impact sensor / foot feedback might help.)

2) learn about RL and the issue with sim2real gap. -> toy problem since real robot was not available yet

3) model the robot with enough fidelity for the simulation and RL training.

4) caracterizing the physical robot limit to limit the sim2real risk.

5) actually comming up with a policy that work.

## 3.1 Overall methodology 
## 3.2 Hardware selection 
### 3.2.1 Motor 
talk about motor map, find cheap and close in specs to sonceboz, our prior is to maximize torque density.
got bitten by the driver board from cubemars with horrible documentation
### 3.2.2 What the actuator selection got wrong 

### 3.2.3 Battery pack 
talk about the battery map tool.

### 3.2.4 Compute
raspberry pi that was layout around, the policy is small. Its possible to have a real time kernel running there and its a multi core computer. this allow to pin time critical to one core. Unlike beagle bone which are much slower and have only one core ( and a special integrated MCU that can be used for time critical application witch much more work to develop code for it.)

the raspberry can be interfaced to the CAN bus with a commercial hat that have CAN to SPI.

### 3.2.5 Sensors
impact sensor that where never implemented, should work with the sensor hat has it has 4 analog input
we also have an IMU on that hat. it work at 200 Hz

## 3.3 Robot modelling
CAD to URDF pipeline to have the matrix correct, how to validate it (know movement on the robot, measure torque and check against prediction)
refine with weigthing each segmebt manually to reduce Dof when calibrating innertia matrix with real value.

## 3.4 Simulation
mujoco, CPU only as isaac required recent nvidia hardware and contact modelling is apparently not as good as mujoco.
once I had access to EPFL cluster, not much of a bottle neck anymore.
### 3.4.1 URDF cannot describe this robot 
URDF work only for serial robot. this one is hybrid serial parralel and thus we need to close the loop later.
### 3.4.2 Compute backend 
scitas cluster, ssh and python job. nothing fancy
### 3.4.3 Establishing that a simulation result is real 

### 3.5 Plant identification: replacing assumptions with measurements
get bode for each actuator to track a sine, measure workspace of real robot.
validate against simulation to kill some of the potential failure of sim2real

### 3.5.1 Mass 
manually weighting each segment. show table with data

### 3.5.2 Peak torque is what the gearbox delivers, not what the datasheet quotes

### 3.5.3 The drive’s position loop is 0.8 Hz
in Servo mode. in MIT mode its not a limitation anymore.

### 3.5.4 The ankle spring 
measured manually with a dynamometer and the angle deflection, it was a mangnitude order not stiff enough and thus was replaced with a rigid link for now.

### 3.5.5 System identification: including what it could not resolve 

### 3.5.6 Loop timing and CAN 
### 3.5.7 The CAN protocol, as measured 
## 3.6 Achievable gait: actuator and mass-distribution limits 
### 3.6.1 Method 
### 3.6.2 Results 
### 3.6.3 Limiting factors 
### 3.6.4 Sensitivity to mass distribution 
### 3.6.5 Ankle stiffness 
### 3.6.6 The corrected ceiling
### 3.6.7 Limitations 
## 3.7 Toy problem: one joint, end to end 
## 3.8 RL policy design and validation 
### 3.8.1 Attempt 1: direct joint torque 
### 3.8.2 Attempt 2: joint position targets (PD) 
### 3.8.3 Attempt 3: a central pattern generator tuned by the policy 
### 3.8.4 Reflexes: what is learned and what is hard-wired 
### 3.8.5 The pitch-balance wall 
### 3.8.6 The cadence problem and a cautionary bug 
### 3.8.7 Results 
### 3.8.8 Which of these results survive the plant correction 
### 3.8.9 Validation status and known gaps 
### 3.8.10 A second generator: explicit-oscillator CPG versus the Fourier series 
### 3.8.11 The ankle, revisited as a build decision 
### 3.8.12 The drivable-demonstrator lineage: closing on the measured plant 
### 3.8.13 A scripted baseline: 21 gains win at m2 and hit the same wall at m3 
### 3.8.14 Postscript: the rebuilt robot, and a cap that was never there 
## 3.9 Negative results 
## 3.10 Deployment 
### 3.10.1 Linux without a real-time kernel 
### 3.10.2 CAN at runtime: the bus with nothing on it 
### 3.10.3 The drive as deployed 
### 3.10.4 The safety envelope as an instrument 
### 3.10.5 Hardware validation: the flight recorder and the pre-move guard 
## 3.11 Hardware experiments 
### 3.11.1 Static end-effector force map 
# 4 Results
## 4.1 Hardware 
## 4.2 RL experiments 
# 5 Discussion 
## 5.1 Successes 
## 5.2 Failures 
## 5.3 Lessons learned 
# 6 Conclusion and Future Work 
## 6.1 Summary of Findings 
## 6.2 Challenges and Limitations 
## 6.3 Suggestions for Future Research 
# 7 Appendix 
## 7.1 logbook 
## 7.2 URDF from CAD: step by step
link to the repo
## 7.3 actuator review

## 7.4 battery review

