---
layout: default
title: Using GPIO
parent: Examples
nav_order: 7
---

# Using GPIO (Reading digital and analog)
{: .no_toc }

1. TOC
{:toc}
---

## Reading Digital Signals
You can read digital signals on pins 1-8 (and encoder A,B,Z pins) using 
```python
from odrive_helpers import digital_read
digital_read(od, pin_num)
```
Ensure that your pin is set to digital input in `odrivetool` with  
```
odrvX.config.gpioX_mode = GPIO_MODE_DIGITAL_PULL_UP 
odrvX.save_configuration()
```
Anytime that you change the GPIO mode for a pin, you need to ensure that you save the new configuration so the change
goes into effect. You can read more about changing GPIO modes [here](https://docs.odriverobotics.com/v/latest/pinout.html).

## Reading Analog Signals
You can read analog signals on pins 1-5 using
```python
from odrive_helpers import analog_read
analog_read(od, pin_num)
```
Ensure that your pin is set to analog input in `odrivetool` with  
```
odrvX.config.gpioX_mode = GPIO_MODE_ANALOG_IN 
odrvX.save_configuration()
```