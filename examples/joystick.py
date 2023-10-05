import sys

sys.path.append("/home/soft-dev/packages/RaspberryPiCommon")
sys.path.append("/home/soft-dev/Documents/dpea-odrive")

from dpea_odrive.odrive_helpers import *
from time import sleep
from pidev.Joystick import Joystick
from threading import Thread
from odrive.utils import start_liveplotter

joy = Joystick(0, False)


def print_info(ax: ODriveAxis):
    print(f"Curr State: {ax.axis.current_state}")
    print(f"Input Mode = {ax.axis.controller.config.input_mode}")
    print(f"Control Mode: {ax.axis.controller.config.control_mode}")


def joy_action(ax: ODriveAxis):
    pos = 0
    mode = 0
    while True:
        x_val = joy.get_axis("x")
        vel = 0 if -.2 < x_val < .2 else 20 * x_val

        if x_val < -.2:
            pos -= 1
        elif x_val > .2:
            pos += 1

        if mode % 3 == 0:
            ax.set_pos_filter(pos, 12)
        elif mode % 3 == 1:
            ax.set_pos(pos)
        else:
            ax.set_vel(vel)

        if joy.get_button_state(0):
            mode += 1
            pos = ax.get_pos()

        sleep(.1)


def start_joy_thread(ax):
    Thread(target=joy_action, args=(ax,), daemon=True).start()


if __name__ == "__main__":
    od = find_odrive()

    assert od.config.enable_brake_resistor is True, "Check for faulty brake resistor."

    ax0 = ODriveAxis(od.axis0)
    if not ax0.is_calibrated():
        print("calibrating...")
        ax0.calibrate()
    ax0.set_gains()

    try:
        start_liveplotter(lambda: [ax0.axis.encoder.pos_estimate, ax0.axis.controller.input_pos, ])
        start_joy_thread(ax0)
        while True:
            sleep(10)
    finally:
        ax0.idle()
        dump_errors(od)
        print("DONE")
