"""
Example program of using ODrive's built-in watchdog to handle cutting current to the motor when communication is lost.
"""
import sys

sys.path.append("/home/soft-dev/Documents/dpea-odrive")

from dpea_odrive.odrive_helpers import *
from odrive.utils import start_liveplotter
from odrive.enums import AXIS_ERROR_WATCHDOG_TIMER_EXPIRED
from time import sleep

if __name__ == "__main__":
    od = find_odrive()

    assert od.config.enable_brake_resistor is True, "Check for faulty brake resistor."

    ax = ODriveAxis(od.axis0)
    if not ax.is_calibrated():
        print("calibrating...")
        ax.calibrate()
    ax.set_gains()
    # Example from odrive repo:
    # https://github.com/odriverobotics/ODrive/blob/48433c61c6a00a1edae33a37674966aad3bcabb0/tools/odrive/tests/test_runner.py#L181
    ax.axis.config.enable_watchdog = False
    ax.axis.error = 0
    ax.axis.config.watchdog_timeout = .5  # if watchdog hasn't been fed in over .5 seconds, motor idles
    ax.axis.watchdog_feed()
    ax.axis.config.enable_watchdog = True

    try:
        while True: # the 'action' loop, part of code that is talking to the motor and continuously feeding watchdog
            ax.set_vel(2)
            ax.axis.watchdog_feed()  # feed the watchdog to reset the watchdog_timeout.
            sleep(.1)

    finally:
        # ax.axis.config.enable_watchdog = False
        ax.idle()
        if ax.axis.error == AXIS_ERROR_WATCHDOG_TIMER_EXPIRED:
            ax.axis.error = 0
        dump_errors(od)
        print("DONE")
