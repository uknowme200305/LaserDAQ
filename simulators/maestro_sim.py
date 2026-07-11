import random


class MaestroSimulator:

    def __init__(self, laser):

        self.laser = laser

        self.connected = False

        self.device_name = "Gentec Maestro Simulator"

        self.firmware = "Maestro SIM v1.0"

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
    # Device Information
    # ==================================================

    def identify(self):

        return self.firmware

    def ping(self):

        return "OK"

    def get_status(self):

        if self.connected:

            return "READY"

        return "DISCONNECTED"

    # ==================================================
    # Measurements
    # ==================================================

    def read_power(self):

        if not self.connected:

            return 0.0

        # Read optical power produced by the laser
        power = self.laser.read_optical_power()

        # Simulate power meter measurement noise
        power += random.uniform(
            -0.03,
            0.03
        )

        return round(
            max(power, 0.0),
            3
        )

    # ==================================================
    # Settings
    # ==================================================

    def set_wavelength(
        self,
        wavelength_nm
    ):

        self.wavelength = wavelength_nm

        return "OK"

    # ==================================================
    # Generic Measurement
    # ==================================================

    def get_measurement(self):

        return {

            "power": self.read_power()

        }