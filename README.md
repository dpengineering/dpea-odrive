# dpea-odrive

## DISCLAIMER
This library is meant to replace [RPI_ODrive](https://github.com/dpengineering/RPi_ODrive)
and be used for the 2022-2023 school year.

## About
dpea-odrive is a helper library for DPEA projects that use the ODrive motor controller. You can think
of this library as a wrapper to existing odrive functions to streamline the programming processs. For
more detailed information, consider visiting the below links and digging around.
 - [ODrive Getting Started Page](https://docs.odriverobotics.com/v/latest/getting-started.html)
 - [Official ODrive Github Repo](https://github.com/odriverobotics/ODrive)

## Usage
To get your ODrive up and running, please navigate to the following site --
* [DPEA ODrive Getting Started](https://dpengineering.github.io/dpea-odrive/)

## Common Errors
* `DC_BUS_OVER_REGEN_CURRENT`
  * Your DC power supply is receiving current that it cannot handle. 
    * Is your break resistor physically connected to your board?
    * If you enter `odrivetool` and type in `odrvX.config.enable_brake_resistor`does it return True?
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
