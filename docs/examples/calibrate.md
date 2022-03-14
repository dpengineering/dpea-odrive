---
layout: default
title: Calibrating
parent: Examples
nav_order: 2
---

# Calibrating an ODrive Motor
{: .no_toc }

1. TOC
{:toc}
---

```python
from odrive_helpers import *

od = find_odrive()

assert od.config.enable_brake_resistor is True, "Check for faulty brake resistor."

# axis0 and axis1 correspond to M0 and M1 on the ODrive
# You can also set the current limit and velocity limit when initializing the axis
ax = ODriveAxis(od.axis0, current_lim=10, vel_lim=10)

# Basic motor tuning, for more precise tuning,
# follow this guide: https://docs.odriverobotics.com/v/latest/control.html#tuning
ax.set_gains()

if not ax.is_calibrated():
    print("calibrating...")
    ax.calibrate_with_current_lim(10)

print("Current Limit: ", ax.get_current_limit())
print("Velocity Limit: ", ax.get_vel_limit())

dump_errors(od)
```