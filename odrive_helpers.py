from time import time, sleep
import logging

import odrive
import odrive.configuration
from odrive.enums import *
import fibre

print(f"ODrive Version: {odrive.version.get_version_str()}")


def find_odrive(serial_number: str = None):
    print(f"Finding ODrive {serial_number or ''}")
    od = odrive.find_any(serial_number=serial_number)
    print(f"Connected to ODrive {format(od.serial_number, 'X')}")
    dump_errors(od)
    return od


def dump_errors(od):
    odrive.utils.dump_errors(od)


def reboot_odrive(od):
    ser_num = format(od.serial_number, 'X')
    try:
        od.reboot()
    except fibre.ObjectLostError:
        print('Rebooting.')
        return find_odrive(serial_number=ser_num)


def save_odrive_configuration(od):
    od.axis0.requested_state = AXIS_STATE_IDLE
    od.axis1.requested_state = AXIS_STATE_IDLE
    try:
        od.save_configuration()
    except fibre.ObjectLostError:
        print("Saved Configuration and Disconnected")


def backup_configuration(od, filename=None):
    logger = logging.getLogger("backup")
    logger.setLevel(logging.INFO)
    odrive.configuration.backup_config(od, filename, logger)


def restore_configuration(od, filename=None):
    logger = logging.getLogger("restore")
    logger.setLevel(logging.INFO)
    odrive.configuration.restore_config(od, filename, logger)


class ODrive_Axis(object):

    def __init__(self, axis, current_lim=10, vel_lim=10):
        self.axis = axis
        self.home = axis.encoder.pos_estimate
        self.axis.motor.config.current_lim = current_lim  # defaults to 10 Amps
        self.axis.controller.config.vel_limit = vel_lim  # defaults at 10 turns/s
        self.end = float('inf')

    # 'frees' the motor from closed loop control
    def idle(self):
        self.axis.requested_state = AXIS_STATE_IDLE

    # enters full calibration sequence (calibrates motor and encoder)
    def calibrate(self, state=AXIS_STATE_FULL_CALIBRATION_SEQUENCE):
        self.axis.requested_state = state
        start = time()
        sleep(5)  # Gives time for motor to switch out of idle state
        while self.axis.current_state != AXIS_STATE_IDLE:
            sleep(0.5)
            if time() - start > 15:
                print("could not calibrate, try rebooting odrive")
                return False
        return True

    def calibrate_with_current_lim(self, curr_lim):
        original_curr = self.get_current_limit()
        self.set_current_limit(curr_lim)
        self.calibrate()
        self.set_current_limit(original_curr)

    # enters encoder offset calibration
    def calibrate_encoder(self):
        return self.calibrate(AXIS_STATE_ENCODER_OFFSET_CALIBRATION)

    def is_calibrated(self):
        return self.axis.motor.is_calibrated and self.axis.encoder.is_ready

    # sets the current allowed during the calibration sequence
    # Higher currents are needed when the motor encounters more resistance to motion
    # NOTE: this function does not seem to work consistently, please use calibrate_with_current if encountering
    # issues with low current during calibration
    def set_calibration_current(self, calib_current):
        self.axis.motor.config.calibration_current = calib_current

    # returns the allowed calibraiton current. By default it is 5 amps (3 phase not DC)
    def get_calibration_current(self):
        return self.axis.motor.config.calibration_current

    def set_gains(self, pos_g=20, vel_g=.16, vel_int_g=.32):
        self.set_pos_gain(pos_g)
        self.set_vel_gain(vel_g)
        self.set_vel_integrator_gain(vel_int_g)

    def set_current_limit(self, val):
        self.axis.motor.config.current_lim = val

    def get_current_limit(self):
        return self.axis.motor.config.current_lim

    # sets the motor's velocity limit. Default starts slow at 100
    def set_vel_limit(self, vel):
        self.axis.controller.config.vel_limit = vel

    # sets the motor to a specified velocity. Does not go over the velocity limit
    def set_vel(self, vel):
        if self.axis.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.axis.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
        self.axis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL

        self.axis.controller.input_vel = vel

    # returns the velocity measured from the encoder
    def get_vel(self):
        return self.axis.encoder.vel_estimate

    # returns the velocity limit
    def get_vel_limit(self):
        return self.axis.controller.config.vel_limit

    # Uses ramped velocity control where the speed, vel [turns/s], will be gradually reached
    # with acceleration, accel [turns/s^2].
    def set_ramped_vel(self, vel, accel):
        assert accel >= 0, "Acceleration must be positive"
        if self.axis.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.axis.controller.config.input_mode = INPUT_MODE_VEL_RAMP
        self.axis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL

        self.axis.controller.config.vel_ramp_rate = accel
        self.axis.controller.input_vel = vel

    # sets the home to the current_position
    def set_home(self):
        self.home = self.get_raw_pos()

    # sets the home pos to a specified position
    def set_home_to(self, pos):
        self.home = pos

    def get_home(self):
        return self.home

    # sets the desired position relative to the encoder
    def set_raw_pos(self, pos):
        if self.axis.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.axis.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
        self.axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL

        self.axis.controller.input_pos = pos

    # returns the current position directly from the encoder
    def get_raw_pos(self):
        return self.axis.encoder.pos_estimate

    # sets the desired position relative to the home position
    def set_pos(self, pos):
        self.set_raw_pos(pos + self.home)

    # returns the current position relative to the home
    def get_pos(self):
        return self.axis.encoder.pos_estimate - self.home

    # sets the desired position relative to the current position
    def set_relative_pos(self, pos):
        self.set_raw_pos(pos + self.get_raw_pos())

    # sets position using the trajectory control mode
    def set_pos_traj(self, pos, accel, vel, decel, inertia=0):
        # BUG: trajectory control not working when invoked after a velocity control, this line is used to
        # uselessly revert back to position control
        self.set_relative_pos(0)

        self.axis.trap_traj.config.accel_limit = accel
        self.axis.trap_traj.config.vel_limit = vel
        self.axis.trap_traj.config.decel_limit = decel
        self.axis.controller.config.inertia = inertia
        assert accel >= 0 and vel >= 0 and decel >= 0 and inertia >= 0, "Values must be positive"
        if self.axis.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
        self.axis.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ
        self.axis.controller.input_pos = pos + self.home

    def set_rel_pos_traj(self, rel_pos, accel, vel, decel, inertia=0):
        self.set_pos_traj(rel_pos + self.get_raw_pos() - self.home, accel, vel,
                          decel, inertia)

    # sets the current sent to the motor
    def set_current(self, curr):  # this is now torque control
        if self.axis.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.axis.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
        self.axis.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL

        self.axis.controller.input_torque = curr

    def set_torque(self, torque):
        self.set_current(torque)

    # Sets the position gain value
    def set_pos_gain(self, val):
        self.axis.controller.config.pos_gain = val

    # returns the position gain value
    def get_pos_gain(self):
        return self.axis.controller.config.pos_gain

    # sets the velocity proportional gain value
    def set_vel_gain(self, val):
        self.axis.controller.config.vel_gain = val

    # returns the velocity proportional gain value
    def get_vel_gain(self):
        return self.axis.controller.config.vel_gain

    # sets the velocity integrator gain value. Usually this is 0
    def set_vel_integrator_gain(self, val):
        self.axis.controller.config.vel_integrator_gain = val

    # returns the velocity integrator gain value. Usually this is 0
    def get_vel_integrator_gain(self):
        return self.axis.controller.config.vel_integrator_gain

    # checks if the motor is moving. Need to use a threshold speed. by default it is 0 turns/second
    def is_busy(self, speed=0.1):
        sleep(
            .5)  # allows motor to start moving, specifically for position control
        if (abs(self.get_vel())) > speed:
            return True
        else:
            return False

    # method to home ODrive using where the chassis is mechanically stopped
    # length is expected length of the track the ODrive takes
    # set length to -1 if you do not want the ODrive to check its homing
    # direction = 1 or -1 depending on which side of the track you want home to be at
    # use direction = 1 if you want the track to be of only positive location values
    def home(self, current1, current2, length=-1, direction=1):
        self.set_current(current1 * -1 * direction)
        print('here')
        sleep(1)
        print('there')
        while self.is_busy():
            pass

        sleep(1)

        self.set_home()
        print(self.get_pos())

        sleep(1)

        if not length == -1:
            self.set_current(current2 * 1 * direction)
            sleep(1)
            while self.is_busy():
                pass

            # end pos should be length
            if abs(self.get_pos() - length) > 50:
                print('ODrive could not home correctly')
                # maybe throw a more formal error here
                return False

        self.set_pos(0)
        print('ODrive homed correctly')
        return True

    # homes the motor by having it move towards one side with a constant velocity. Once it can no longer move, it considers this its home
    # The direction can be specified either by the sign of the velocty passed in or through the direction parameter
    # If the length of the track is known, it can be passed in. If this is done, after moving to one side, the motor will move to the other to find if the homing was successful.
    def home_with_vel(self, vel=.5, length=-1, direction=1):
        self.set_vel(vel * -1 * direction)
        print('here')
        sleep(1)
        print('there')
        while self.is_busy():
            pass

        sleep(1)

        self.set_home()
        print(self.get_pos())

        sleep(1)

        if not length == -1:
            self.set_vel(vel * 1 * direction)
            sleep(1)
            while self.is_busy():
                pass

            print(self.get_pos())

            # end pos should be length
            if abs(self.get_pos() - length) > 50:
                print('ODrive could not home correctly')
                # maybe throw a more formal error here
                return False

        print('ODrive homed correctly')
        return True

    def home_with_endstop(self, vel, offset, min_gpio_num):
        self.axis.controller.config.homing_speed = vel  # flip sign to turn CW or CCW
        self.axis.min_endstop.config.gpio_num = min_gpio_num
        self.axis.min_endstop.config.offset = offset
        self.axis.min_endstop.config.enabled = True
        self.axis.requested_state = AXIS_STATE_HOMING

        sleep(1)
        while self.is_busy():
            sleep(1)

        self.set_home()
        self.axis.error = 0
        self.axis.min_endstop.config.enabled = False

    def home_without_endstop(self, vel, offset):
        self.axis.controller.config.homing_speed = vel  # flip sign to turn CW or CCW
        self.set_ramped_vel(self.axis.controller.config.homing_speed, 1)
        while self.is_busy():
            sleep(1)

        self.set_pos_traj(self.get_pos() + offset, 1, 2, 1)
        sleep(3)  # allows to start moving to offset position
        while self.is_busy():
            sleep(1)

        self.set_home()

    # returns phase B current going into motor
    def get_curr_B(self):
        return self.axis.motor.current_meas_phB

    # returns phase C current going into motor
    def get_curr_C(self):
        return self.axis.motor.current_meas_phC

    # Clears all the errors on the axis
    def clear_errors(self):
        self.axis.error = 0
        self.axis.encoder.error = 0
        self.axis.motor.error = 0
        self.axis.controller.error = 0
        # There is also sensorless estimator errors but those are super rare and I am not sure what the object field is called to ima just leave it
