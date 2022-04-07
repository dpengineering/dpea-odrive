---
layout: default
title: FAQ
nav_order: 4
has_children: true
---

# FAQ
{: .no_toc }

1. TOC
{:toc}
---

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
