---
layout: default
title: Examples
nav_order: 3
has_children: true
---

# Examples
{: .no_toc }

1. TOC
{:toc}
---

```python
from odrive_helpers import *

if __name__ == "__main__":
    od = find_odrive()

    assert od.config.enable_brake_resistor is True, "Check for faulty brake resistor."

    # axis0 and axis1 correspond to M0 and M1 on the ODrive
    ax = ODrive_Axis(od.axis0)
    
    # Basic motor tuning, for more precise tuning,
    # follow this guide: https://docs.odriverobotics.com/v/latest/control.html#tuning
    ax.set_gains()

    if not ax.is_calibrated():
        print("calibrating...")
        ax.calibrate()

    print("Current Limit: ", ax.get_current_limit())
    print("Velocity Limit: ", ax.get_vel_limit())
    dump_errors(od)

```