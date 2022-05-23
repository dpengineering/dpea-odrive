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
mode in odrivetool with,

```python
<odrv>.config.gpio3_mode = GPIO_MODE_ANALOG_IN
<odrv>.save_configuration()
```

TBD



At the moment, please refer to the [guide on ODrive Docs](https://docs.odriverobotics.com/v/latest/analog-input.html) to
implement analog input mapping.