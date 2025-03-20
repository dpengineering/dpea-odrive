"""
Run this program in a terminal setting to tune your odrive motors.
The program will return the tuned values for pos_gain, vel_gain, and vel_integrator_gain.
This has not been extensively tested, thus do not over-rely on the values returned here. Use as a starting point.
"""
import sys

sys.path.append("/home/soft-dev/Documents/dpea-odrive")

from dpea_odrive.odrive_helpers import *
from odrive.utils import start_liveplotter
from time import sleep
import matplotlib
matplotlib.use('TkAgg')  # Use a backend that doesn't require a GUI

if __name__ == "__main__":
    od = find_odrive()

    assert od.config.enable_brake_resistor is True, "Check for faulty brake resistor."

    ax = ODriveAxis(od.axis0)
    ax.set_gains()

    if not ax.is_calibrated():
        print("calibrating...")
        ax.calibrate()
        print("Done Calibrating")
    else:
        print("Motor Already Calibrated.")

    try:
        ax.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        print("Now Attempting to Tune Motor")
        ax.set_vel_integrator_gain(0)
        while input("Is System Stable? [y/n]") == "n":
            ax.set_gains(ax.get_pos_gain() / 2, ax.get_vel_gain() / 2, ax.get_vel_integrator_gain() / 2)

        print("Attempting vel_gain Tuning.")
        sleep(1)
        while input("Is Motor Vibrating? [y/n]") == "n":
            ax.set_vel_gain(ax.get_vel_gain() * 1.3)

        ax.set_vel_gain(ax.get_vel_gain() * .5)
        print("Attempting pos_gain Tuning.")
        start_liveplotter(lambda: [ax.axis.encoder.pos_estimate, ax.axis.controller.input_pos])
        sleep(5)
        print("Pay Attention For Any Overshoot")
        ax.set_relative_pos(1)
        ax.wait_for_motor_to_stop()
        ax.set_relative_pos(-1)
        while input("Is There Overshoot? [y/n]") == "n":
            ax.set_pos_gain(ax.get_pos_gain() * 1.3)
            ax.set_relative_pos(1)
            sleep(1)
            ax.set_relative_pos(-1)
            sleep(1)
        ax.set_pos_gain(ax.get_pos_gain() / 1.3)

        ax.set_vel_integrator_gain(.5 * 10 * ax.get_vel_gain())
        print("Done Calibrating")

    finally:
        ax.idle()
        print(f"Pos Gain: {ax.get_pos_gain()}, Vel Gain: {ax.get_vel_gain()}, Vel Int Gain: {ax.get_vel_integrator_gain()}")
        dump_errors(od)
        od.clear_errors()
        print("DONE")
