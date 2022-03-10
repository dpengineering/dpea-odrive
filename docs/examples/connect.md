---
layout: default
title: Connecting
parent: Examples
nav_order: 1
---

# Connecting to ODrive
{: .no_toc }

1. TOC
{:toc}
---

```python
from odrive_helpers import *

od_xy = find_odrive(serial_number="12345ABC")
od_z = find_odrive(serial_number="67890DEF")

assert od_xy.config.enable_brake_resistor is True, "Check for faulty brake resistor."
assert od_z.config.enable_brake_resistor is True, "Check for faulty brake resistor."

# axis0 and axis1 correspond to M0 and M1 on the ODrive
x_axis = ODriveAxis(od_xy.axis0)
y_axis = ODriveAxis(od_xy.axis1)
z_axis = ODriveAxis(od_z.axis0)

dump_errors(od_xy)
dump_errors(od_z)
```