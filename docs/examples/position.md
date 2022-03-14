---
layout: default
title: Position Control
parent: Examples
nav_order: 4
---

# Controlling Position of a Motor
{: .no_toc }

1. TOC
{:toc}
---

```python
from odrive_helpers import *
from time import sleep

od = find_odrive()
assert od.config.enable_brake_resistor is True, "Check for faulty brake resistor."

ax = ODriveAxis(od.axis0)
ax.set_gains()
if not ax.is_calibrated():
    print("calibrating...")
    ax.calibrate()

# SETTING POSITION
ax.set_vel_limit(5)
ax.set_pos(5)
ax.wait_for_motor_to_stop()
print("Current Position in Turns = ", round(ax.get_pos(), 2))
ax.set_relative_pos(-5)
ax.wait_for_motor_to_stop()
print("Current Position in Turns = ", round(ax.get_pos(), 2))
sleep(3)

# USING TRAJECTORY CONTROL
ax.set_vel_limit(15)
ax.set_pos_traj(5, 1, 10, 1)
ax.wait_for_motor_to_stop()
print("Current Position in Turns = ", round(ax.get_pos(), 2))
ax.set_rel_pos_traj(-5, 1, 10, 1)
ax.wait_for_motor_to_stop()
print("Current Position in Turns = ", round(ax.get_pos(), 2))

ax.idle()  # Removes motor from CLOSED_LOOP_CONTROL, essentially 'frees' the motor

dump_errors(od)
```