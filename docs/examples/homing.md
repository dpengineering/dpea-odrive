---
layout: default
title: Homing
parent: Examples
nav_order: 3
---

# Homing an ODrive Motor
{: .no_toc }

1. TOC
{:toc}
---

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