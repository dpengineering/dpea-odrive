---
layout: default
title: Position Control
parent: Examples
nav_order: 3
---

# Controlling Position of a Motor
{: .no_toc }

1. TOC
{:toc}
---
## Connecting and Calibrating
```jupyterpython
from odrive_helpers import *
from time import sleep

od = find_odrive()
assert od.config.enable_brake_resistor is True, "Check for faulty brake resistor."

ax = ODriveAxis(od.axis0)
ax.set_gains()
if not ax.is_calibrated():
    print("calibrating...")
    ax.calibrate()
```
## Simple Position Control

```
#USING SIMPLE POSITION CONTROL
ax.set_vel_limit(5)
ax.set_pos(5)
ax.wait_for_motor_to_stop()
print("Current Position in Turns = ", round(ax.get_pos(), 2))
ax.set_relative_pos(-5)
ax.wait_for_motor_to_stop()
print("Current Position in Turns = ", round(ax.get_pos(), 2))
sleep(3)
```

## Trapezoidal Trajectory Position Control

This position control mode is useful when you do not want your motor to move at full speed to a position. Trapezoidal
Trajectory mode allows for acceleration, coasting speed, and deceleration to reach a target position. Take a look
[here](https://docs.odriverobotics.com/v/latest/control-modes.html#trajectory-control) to see why it's 
called **trapezoidal** trajectory mode. The order of arguments to `set_pos_traj` are as follows,

```set_pos_traj(target position, acceleration in turns/s^2, target speed in turns/s, deceleration in turns/s^2)```

```python
# USING TRAJECTORY CONTROL
ax.set_vel_limit(15)
ax.set_pos_traj(5, 1, 10, 1) # position 5, acceleration 1 turn/s^2, target velocity 10 turns/s, deceleration 1 turns/s^2
ax.wait_for_motor_to_stop()
print("Current Position in Turns = ", round(ax.get_pos(), 2))
ax.set_rel_pos_traj(-5, 1, 10, 1)
ax.wait_for_motor_to_stop()
print("Current Position in Turns = ", round(ax.get_pos(), 2))

ax.idle()  # Removes motor from CLOSED_LOOP_CONTROL, essentially 'frees' the motor

dump_errors(od)
```