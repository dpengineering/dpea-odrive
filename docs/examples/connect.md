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
## Connecting to a Single ODrive
```python
from odrive_helpers import *

od = find_odrive()

assert od.config.enable_brake_resistor is True, "Check for faulty brake resistor."

# axis0 and axis1 correspond to M0 and M1 on the ODrive
ax = ODriveAxis(od.axis0)

dump_errors(od)
```

## Connecting to Multiple ODrives
The `serial_number` for each board can be found using `odrivetool`. The serial number will be in the blue text that
says, `Connected to <serial_number> as odrv0`. Have one ODrive plugged in at a time to isolate each serial number.
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