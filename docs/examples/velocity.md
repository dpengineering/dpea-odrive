---
layout: default
title: Velocity Control
parent: Examples
nav_order: 5
---

# Connecting to ODrive
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

# SETTING VELOCITY
print("Current Position in Turns = ", round(ax.get_pos(), 2))
ax.set_vel_limit(5)  # Sets the velocity limit to be X turns/s
ax.set_vel(3)  # Starts turning the motor X turns/s
sleep(5)
print("Encoder Measured Velocity = ", round(ax.get_vel(), 2))
ax.set_vel(0)  # Stops motor
sleep(1)
print("Current Position in Turns = ", round(ax.get_pos(), 2))
ax.set_pos(0)
ax.wait_for_motor_to_stop()
print("Current Position in Turns = ", round(ax.get_pos(), 2))
sleep(3)

# SETTING RAMPED VELOCITY
ax.set_vel_limit(10)  # Sets the velocity limit to be X turns/s
print("Speeding Up")
ax.set_ramped_vel(5, 1)  # Starts accelerating motor to X turns/s
sleep(10)
print("Slowing Down")
ax.set_ramped_vel(0, 1)  # Stops motor
ax.wait_for_motor_to_stop()
print("Current Position in Turns = ", round(ax.get_pos(), 2))

ax.idle()  # Removes motor from CLOSED_LOOP_CONTROL, essentially 'frees' the motor

dump_errors(od)
```