import sys

sys.path.append("/home/soft-dev/Documents/dpea-odrive")

from odrive_helpers import *
from odrive.utils import start_liveplotter
from time import sleep

if __name__ == "__main__":
    od = find_odrive()

    assert od.config.enable_brake_resistor is True, "Check for faulty brake resistor."

    ax = ODriveAxis(od.axis0)
    if not ax.is_calibrated():
        print("calibrating...")
        ax.calibrate()
    ax.set_gains()

    start_liveplotter(lambda: [ax.axis.encoder.pos_estimate, ax.axis.controller.input_pos])
    times = []
    try:
        while True:
            start_time = time()
            ax.set_pos(1)
            sleep(.01)
            while abs(ax.get_vel()) > .1:
                pass

            ax.set_pos(0)
            sleep(.01)
            while abs(ax.get_vel()) > .1:
                pass

            elapsed_time = time() - start_time
            print(f"End Time: {elapsed_time}")
            times.append(elapsed_time)

    finally:
        ax.idle()
        dump_errors(od)
        print("DONE")
        print(f"Average Time: {sum(times) / len(times)}")
