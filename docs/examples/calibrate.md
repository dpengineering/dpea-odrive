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
from dpea_odrive.odrive_helpers import *
od = find_odrive()

assert od.config.enable_brake_resistor is True, "Check for faulty brake resistor."

# axis0 and axis1 correspond to M0 and M1 on the ODrive
# You can also set the current limit and velocity limit when initializing the axis
ax = ODriveAxis(od.axis0, current_lim=10, vel_lim=10)

# Basic motor tuning, for more precise tuning,
# follow this guide: https://docs.odriverobotics.com/v/0.5.6/control.html#control-doc
ax.set_gains()

if not ax.is_calibrated():
    print("calibrating...")
    ax.calibrate_with_current_lim(10)

print("Current Limit: ", ax.get_current_limit())
print("Velocity Limit: ", ax.get_vel_limit())

dump_errors(od)
```
## Startup Calibration - Motor
At some point, you will most likely want your ODrive motor to be pre-calibrated on startup. What this means
is that you don't have to run through the calibration sequence everytime you turn on your ODrive. To do this,
read through [this guide](https://discourse.odriverobotics.com/t/skip-calibration-startup-procces/3787/2) first. In short,
you will need to
1. Calibrate your motor and encoder normally.
2. Toggle on auto calibration
3. Save the configuration onto the ODrives permanent memory
type in the following into `odrivetool`.

```python
<odrv>.<axis>.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
<odrv>.<axis>.motor.config.pre_calibrated = True
<odrv>.<axis>.config.startup_encoder_offset_calibration = True
<odrv>.<axis>.config.startup_closed_loop_control = True
<odrv>.save_configuration()
```
## Encoder Calibration

**Importantly**, there are two ways to calibrate your encoder. You can either do the normal offset calibration everytime
or do an index calibration which seeks a specific part of your encoder. You can only do an index encoder calibration if
you have an encoder with a Z signal, which most of our encoders have. For more info, refer to the [ODrive encoder info 
page](https://docs.odriverobotics.com/v/0.5.6/encoders.html). We should always try to calibrate our encoders using index
calibration when we can.

To calibrate an encoder using its index (Z) signal, we first need to disengage the motor from anything other than the 
encoder to ensure that there is no load on the motor. Then we execute the following in `odrivetool` --
```python
<axis>.requested_state = AXIS_STATE_MOTOR_CALIBRATION
<axis>.encoder.config.use_index = True
<axis>.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
```

If you would like the encoder to calibrate with its index on boot, add the following -- 
```python
<axis>.motor.config.pre_calibrated = True
<axis>.encoder.config.pre_calibrated = True
<axis>.config.startup_encoder_index_search = True
<odrv>.save_configuration()
```

Now on every reboot the motor will turn in one direction until it finds the encoder index. 
If your motor has problems reaching the index location due to the mechanical load, you can increase 
`<axis>.motor.config.calibration_current`.
