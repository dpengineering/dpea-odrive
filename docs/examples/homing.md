---
layout: default
title: Homing
parent: Examples
nav_order: 5
---

# Homing an ODrive Motor
{: .no_toc }

1. TOC
{:toc}
---
Sometimes, your motor setup will not be able to spin indefinitely. You may be constrained by walls that your motor has
to move within. In this case, it is useful to home your motor position so that you have a relative starting position
when your application starts up for the first time. You can either use a dedicated switch/sensor to trigger the home 
position, or you can _softly_ rotate your motor into a wall until it cannot move anymore. Both methods are highlighted
below as `ax.home_with_endstop` and `ax.home_without_endstop` respectively.

```python
from odrive_helpers import *

od = find_odrive()
assert od.config.enable_brake_resistor is True, "Check for faulty brake resistor."

ax = ODriveAxis(od.axis0)
ax.set_gains()
if not ax.is_calibrated():
    print("calibrating...")
    ax.calibrate()

print("homing")
# ax.home_with_endstop(1, .5, 2)  # Home with velocity 1 to sensor on GPIO Pin 2, then offset .5 rotations
ax.home_without_endstop(1, .5)  # Home with velocity 1 until wall is hit, then offset .5 rotations
print("Current Position in Turns = ", round(ax.get_pos(), 2))  # should be at 0.0

dump_errors(od)
```