---
layout: default
title: Getting Started
nav_order: 2
has_children: false
---

# Getting Started
{: .no_toc }

1. TOC
{:toc}
---

## 🤖 ODrive: Powering DPEA Projects

**ODrive motors** are central to a variety of exhibits within the DPEA. They are a powerful, high-performance alternative to traditional **stepper** and **DC motors**, making them essential for driving our most demanding and precise projects.

---

### **Key Advantages of ODrive**

ODrive controllers excel in applications requiring high dynamic performance and precise control because they drive **brushless DC (BLDC) motors**. Unlike open-loop stepper or basic DC motors, the ODrive system provides:

* **Torque and Speed Control:** Excellent at both high speeds and when maximum torque is needed, ensuring smooth and reliable motion.
* **High Precision:** Utilizes feedback from high-resolution **encoders** to maintain exact position, velocity, or torque, even under changing loads.
* **Energy Efficiency:** BLDC motors driven by ODrive are generally more efficient than brushed or stepper alternatives, crucial for battery-powered or continuous-use exhibits.

---

### **Examples of ODrive Integration in DPEA Exhibits**

ODrive motors are used in projects where strength, smoothness, and fine control are paramount. Some examples include:

* **High-Speed or High-Torque Actuators:** Driving robotic arms or kinetic sculptures that require rapid, powerful, and repeatable movements.
* **Precision Gimbals and Camera Sliders:** Achieving the ultra-smooth, slow, and precise motion necessary for professional-grade film equipment and automated photography setups.
* **Balancing and Stability Platforms:** Providing the quick, corrective torque needed for systems like inverted pendulums or dynamic stability demonstrators.

## Using this Library in Python
After you have followed the [Getting Started section in ODrive Docs](https://docs.odriverobotics.com/v/0.5.6/getting-started.html)
and have successfully controlled your motor using `odrivetool`, it is time to start using the
[odrive_helpers](https://github.com/dpengineering/dpea-odrive/blob/main/odrive_helpers.py) library.

We can install this library using a `pip install`: 
```
pip3 install dpea-odrive 
```


This library will allow you to automate the process of using `odrivetool` by bundling many of the commands into Python.
For example, to move the motor one revolution in `odrivetool` we would need to do the following,
``` 
odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
odrv0.axis0.controller.input_pos = 1
```

But, using the `odrive_helpers` library we would simply need to run commands such as
```python
axis0.calibrate()
axis0.set_pos(1)
```

To experiment with the `odrive_helpers` library, run `ipython3` and follow along the various 
[examples](/dpea-odrive/examples/examples) in the sidebar.

## Kivy GUI
After you have tested each example, let us finish by making a Kivy GUI. Your goal with this GUI is to have the following --
* A button that toggles between moving the motor 5 rotations clockwise and counterclockwise
* A slider that controls the velocity of the motor
* A second slider that controls the acceleration of the motor (i.e. two sliders to handle ramped velocity)
  * Consider changing your velocity slider to use ramped velocity and retrieve the acceleration value from the second slider.
* If using a constrained motor setup (ex. lead screw with endstops), then add a button that homes the motor. You can
  home the motor using an endstop sensor/switch or until a wall is hit. Refer to the homing example for more info.
* Another screen that controls the motor with trapezoidal trajectory control. Have text boxes 
  for acceleration, target position, and deceleration plus a submit button to send the command to the motor.
* Another screen which utilizes a GPIO pin to move the motor when a sensor or switch is activated.




