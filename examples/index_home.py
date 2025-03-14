import sys
from time import time, sleep
sys.path.append("/home/softdev/Desktop/dpea-odrive/src/")

from dpea_odrive.odrive_helpers import *
from odrive.enums import AxisState

odrv0 = find_odrive("207935A1524B")

"""
Performs an encoder index search to align the encoder index mark on the motor axis.

This function initiates an index search sequence on an ODrive motor axis by first asserting
that the encoder is configured to use index search and that the motor is calibrated. It then
sets the axis into the encoder index search state and monitors the encoder's velocity over a 
predefined timeout period. After the timeout, it collects a series of velocity readings to 
compute an average absolute velocity.

The search is deemed successful if the average velocity is below a defined threshold (0.01), 
indicating that the motor has effectively stopped moving. If the average velocity exceeds this 
threshold, the function reverses the search direction and returns False.

Returns:
    bool: True if the index search is successful (motor nearly stopped), otherwise False.

Raises:
    AssertionError: If the encoder configuration is not set to use index search or if the motor
                    is not calibrated.
"""
def perform_index_search(axis):
    # Search parameters
    INDEX_SEARCH_TIMEOUT = 2.5  # Max time to detect movement

    assert axis.encoder.config.use_index is True, "Set Odrive encoder config to utilize index search"
    assert axis.motor.is_calibrated is True, "Calibrate motor before performing index search"

    axis.requested_state = AxisState.ENCODER_INDEX_SEARCH  # Start INDEX_SEARCH
    start_time = time()

    # Wait for index search to finish
    while time() - start_time < INDEX_SEARCH_TIMEOUT:
        vel = axis.encoder.vel_estimate
        print(f"Velocity: {vel:.3f}")

    vel_readings = [axis.encoder.vel_estimate for _ in range(30)]
    avg_vel = abs(sum(vel_readings)/len(vel_readings))
    print(f"Average velocity: {avg_vel:.3f}")

    if avg_vel < 0.01:
        print("Index search successful.")
        return True
    else:
        print("Index search failed: Motor still moving.")
        axis.config.calibration_lockin.accel *= -1 # reverse direction of search
        return False


if __name__ == "__main__":
    # Attempt index search, retry once if needed
    if not perform_index_search(odrv0.axis1):
        print("Retrying index search in opposite direction...")
        perform_index_search(odrv0.axis1)






