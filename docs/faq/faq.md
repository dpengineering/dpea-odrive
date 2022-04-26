---
layout: default
title: FAQ
nav_order: 4
has_children: false
---

# FAQ
{: .no_toc }

1. TOC
{:toc}
---
## What order should I plug my motor wires in?
You can plug your 3-phase motor wires in any order. It is unclear whether the same motor configuration will behave
differently with a different A,B,C wire order, so it is best to choose an order and stick with it during your 
development process.

## What should I use to power up the ODrive?
We will typically have 24 Volt DC Power Supplies to provide power to your ODrive board. There is a DC power terminal
on the side of your board. Right next to the DC terminal is the USB port to communicate with your ODrive board. Check 
out [this diagram](https://docs.odriverobotics.com/v/latest/_images/ODriveBasicWiring.png) for a better understanding
of the board layout.

## Why do I need a 15A fuse?
It is important to use a 15A rated fuse on the positive wire for your DC power supply. Most DC power supplies we 
use are rated for 18A. We do not want any excess current making its way back to the power supply and breaking it, so we
have a fuse that blows before it makes its way back to the power supply. In general, you want to utilize the fuse that is
closest to your power supply amp rating without exceeding that rating.

## `odrivetool liveplotter` does not work?
Sometimes, the liveplotter will not appear on your screen. This can be fixed by typing the following
in your terminal, `sudo apt-get install python3-tk`. In case it still does not work, try out the following example from
matplotlib and note if there are any errors -- [example](https://matplotlib.org/2.0.2/examples/api/legend_demo.html).

## Common Errors
* `DC_BUS_OVER_REGEN_CURRENT`
  * Your DC power supply is receiving current that it cannot handle. 
    * Is your brake resistor physically connected to your board?
    * If you enter `odrivetool` and type in `odrvX.config.enable_brake_resistor`, does it return True?
    * ODrive's default configuration is to have the brake resistor disabled by default. Be wary of using
      `odrv0.erase_configuration()` because this will revert the ODrive back to its factory configuration
      with the brake resistor disabled. Ensure that `odrvX.config.enable_brake_resistor` is set to True if you 
      are using a brake resistor.
* `MOTOR_ERROR_CURRENT_LIMIT_VIOLATION`
  * The current sent to your motor has exceeded the current limit.
    * In `odrivetool` type in `odrvX.axisX.motor.config.current_lim`. Does your current limit seem high
    enough? If not, try increasing the current limit in small increments until you no longer receive
    the error.
* `CONTROLLER_ERROR_OVERSPEED` & `CONTROLLER_ERROR_SPINOUT_DETECTED`
  * Your motor has exceeded its velocity limit and moved faster/farther than it was supposed to.
    * In `odrivetool` type in `odrvX.axisX.controller.config.vel_limit` to see your chosen motor's 
    velocity limit. Does this value make sense? 
    * Be careful when using normal position control instead of trapezoidal trajectory control as your
    motor will move as fast as it can as opposed to having a smooth acceleration.
    * As a last result, you can also change the margin of error/tolerance that the controller uses to
    determine if your motor is too fast by accessing `odrvX.axisX.controller.config.vel_limit_tolerance`.
