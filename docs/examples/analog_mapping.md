---
layout: default
title: Analog Mapping
parent: Examples
nav_order: 8
---

# Mapping analog input to position/velocity
{: .no_toc }

1. TOC
{:toc}
---

There are instances where we want to map analog input from a device like a potentiometer to a motor's velocity, 
position, or current. This is done by first selecting a pin you would like to have as your analog input pin. **Currently,
only pins 3 and 4 on the ODrive can be used for analog mapping.**

For this example, we are going to be utilizing analog input on GPIO Pin 3. First, ensure that Pin 3 is set to analog
mode in `odrivetool` with,

```python
<odrv>.config.gpio3_mode = GPIO_MODE_ANALOG_IN
<odrv>.save_configuration()
```

The next step is to set up an analog mapping on either Pin 3 or Pin 4. 
At the moment, please refer to the [guide on ODrive Docs](https://docs.odriverobotics.com/v/0.5.6/analog-input.html) to
implement analog input mapping.

In short, we will use `odrivetool` to configure the following --
```python
<odrv>.config.gpio3_analog_mapping.endpoint
<odrv>.config.gpio3_analog_mapping.max
<odrv>.config.gpio3_analog_mapping.min
```

If you type the lines above into `odrivetool`, you will see that the default values are None, 0, and 0
respectively. Our analog pin, pin 3 in this case, has a range of 0V to 3.3V. The ODrive maps this range of values
onto values in between our min and max values above. So if we say,
```python
<odrv>.config.gpio3_analog_mapping.endpoint = <odrv>.<axis>.controller._input_vel_property
<odrv>.config.gpio3_analog_mapping.max = 10
<odrv>.config.gpio3_analog_mapping.min = -10

<odrv>.<axis>.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
<odrv>.<axis>.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
```

Assuming your motor was already calibrate, these lines would allow your motor to be controlled by the 
analog input on Pin 3. For example if you connected a potentiometer to Pin 3, its low value at 0V would map to 
the min of -10 turns/s. The high value of 3.3V would map to 10 turns/s. And a value of 1.65V would map to 0 turns/s.

To turn off this mapping, you can simply set the analog mapping endpoint to None.
```python
<odrv>.config.gpio3_analog_mapping.endpoint = None
```

Similarly, the mapping is only active if there is a valid endpoint and the axis' requested state is 
`AXIS_STATE_CLOSED_LOOP_CONTROL`. Setting the axis state to `AXIS_STATE_IDLE` will also disable the control to the motor,
but as soon as it goes back into closed loop control the mapping will be active. 

If you are wondering how to start the ODrive in `AXIS_STATE_CLOSED_LOOP_CONTROL` on reboot, look into 
```python
<odrv>.<axis>.config.startup_closed_loop_control = True
<odrv>.save_configuration()
```