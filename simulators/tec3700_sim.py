import random


class TEC3700Simulator:

    def __init__(self, laser=None):
        self.laser = laser
        self.connected = False
        # TEC Dynamics

        self.tec_response = 0.18

        # Device Information
        self.device_name = "Newport TEC3700 Simulator"
        self.firmware = "3700 SIM v1.0"

        # Operating State
        self.output_enabled = False
        self.mode = "T"

        # Temperature
        self.temperature_setpoint = 25.000
        self.temperature = 25.000

        # Laser Heating

        self.ambient_temperature = 25.0
        self.heating_gain = 0.015

        # Electrical
        self.current_setpoint = 0.000
        self.current = 0.000
        self.voltage = 0.000

        # Limits
        self.current_limit = 14.000
        self.voltage_limit = 24.000

        self.high_temp_limit = 80.000
        self.low_temp_limit = 0.000

    # ==================================================
    # Connection
    # ==================================================

    def connect(self):

        self.connected = True

        return True

    def disconnect(self):

        self.connected = False

    def is_connected(self):

        return self.connected

    # ==================================================
    # Output
    # ==================================================

    def enable_output(self):

        self.output_enabled = True

        return "OK"

    def disable_output(self):

        self.output_enabled = False

        self.current = 0.0
        self.voltage = 0.0

        return "OK"

    def output_enabled_status(self):

        return self.output_enabled

    # ==================================================
    # Device Information
    # ==================================================

    def identify(self):

        return self.firmware

    def reset(self):

        self.output_enabled = False

        self.temperature = 25.000
        self.temperature_setpoint = 25.000

        self.current = 0.0
        self.voltage = 0.0

        return "OK"

    def save_settings(self):

        return "OK"

    def recall_settings(self):

        return "OK"

    def status_byte(self):

        return "0"

    # ==================================================
    # Mode
    # ==================================================

    def set_temperature_mode(self):

        self.mode = "T"

        return "OK"

    def set_current_mode(self):

        self.mode = "Ite"

        return "OK"

    def set_resistance_mode(self):

        self.mode = "R"

        return "OK"

    def get_mode(self):

        return self.mode

    # ==================================================
    # Temperature
    # ==================================================

    def set_temperature(self, temperature):

        self.temperature_setpoint = float(temperature)

        return "OK"

    def read_temperature(self):

        # ------------------------------------------
        # Laser Heating
        # ------------------------------------------

        laser_heating = 0.0

        if self.laser is not None:

            try:

                laser_current = self.laser.read_current()

                laser_heating = (
                    laser_current *
                    self.heating_gain
                )

            except Exception:

                laser_heating = 0.0

        # ------------------------------------------
        # Desired Temperature
        # ------------------------------------------

        target_temperature = (
            self.temperature_setpoint +
            laser_heating
        )

        # ------------------------------------------
        # TEC Regulation
        # ------------------------------------------

        if self.output_enabled:

            error = (
                target_temperature -
                self.temperature
            )

            self.temperature += (
                error * self.tec_response
            )

        else:

            error = (
                self.ambient_temperature -
                self.temperature
            )

            self.temperature += (
                error * 0.05
            )

        # ------------------------------------------
        # Measurement Noise
        # ------------------------------------------

        self.temperature += random.uniform(
            -0.015,
            0.015
        )
        # Update laser junction temperature
        if self.laser is not None:

            self.laser.set_junction_temperature(
            self.temperature
            )

        return round(
            self.temperature,
            3
        )

    def read_setpoint(self):

        return round(
            self.temperature_setpoint,
            3
        )

    # ==================================================
    # Current
    # ==================================================

    def set_current(self, current):

        self.current_setpoint = float(current)

        return "OK"

    def read_current(self):

        if not self.output_enabled:

            return 0.0

        if self.mode == "Ite":

            self.current = self.current_setpoint

        else:

            error = abs(
                self.temperature_setpoint
                - self.temperature
            )

            self.current = min(
                error * 0.45,
                self.current_limit
            )

        self.current += random.uniform(
            -0.01,
            0.01
        )

        return round(
            self.current,
            3
        )

    def read_current_setpoint(self):

        return round(
            self.current_setpoint,
            3
        )

    # ==================================================
    # Voltage
    # ==================================================

    def read_voltage(self):

        if not self.output_enabled:

            return 0.0

        self.voltage = abs(
            self.current
        ) * 1.55

        self.voltage += random.uniform(
            -0.05,
            0.05
        )

        self.voltage = min(
            self.voltage,
            self.voltage_limit
        )

        return round(
            self.voltage,
            3
        )

    # ==================================================
    # Limits
    # ==================================================

    def set_current_limit(self, limit):

        self.current_limit = float(limit)

        return "OK"

    def read_current_limit(self):

        return self.current_limit

    def set_voltage_limit(self, limit):

        self.voltage_limit = float(limit)

        return "OK"

    def read_voltage_limit(self):

        return self.voltage_limit

    def set_high_temperature_limit(self, value):

        self.high_temp_limit = float(value)

        return "OK"

    def read_high_temperature_limit(self):

        return self.high_temp_limit

    def set_low_temperature_limit(self, value):

        self.low_temp_limit = float(value)

        return "OK"

    def read_low_temperature_limit(self):

        return self.low_temp_limit

    # ==================================================
    # Status
    # ==================================================

    def get_status(self):

        if not self.output_enabled:

            return "OUTPUT OFF"

        if self.temperature > self.high_temp_limit:

            return "HIGH TEMP"

        if self.temperature < self.low_temp_limit:

            return "LOW TEMP"

        return "READY"

    # ==================================================
    # Miscellaneous
    # ==================================================

    def beep(self):

        print("BEEP")

        return "OK"

    def local(self):

        return "OK"

    # ==================================================
    # Generic Measurement
    # ==================================================

    def get_measurement(self):

        return {

            "temperature": self.read_temperature(),

            "setpoint": self.read_setpoint(),

            "current": self.read_current(),

            "voltage": self.read_voltage()

        }