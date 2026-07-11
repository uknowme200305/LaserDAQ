import random


class SF6100Simulator:

    def __init__(self):

        self.connected = False
        self.enabled = False

        # -----------------------------
        # Laser Drive
        # -----------------------------
        self.current_setpoint = 0.0      # mA
        self.current = 0.0               # Actual current

        # -----------------------------
        # Laser Physics
        # -----------------------------
        self.threshold_current = 35.0        # mA
        self.slope_efficiency = 0.85         # mW/mA
        self.forward_voltage = 1.70          # V
        self.series_resistance = 2.0         # Ohm
        self.rolloff = 0.0015                # Thermal roll-off

        # Junction temperature (updated by TEC simulator)
        self.junction_temperature = 25.0

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
    # Laser Enable
    # ==================================================

    def enable(self):

        self.enabled = True

        return "LASER ENABLED"

    def disable(self):

        self.enabled = False

        return "LASER DISABLED"

    # ==================================================
    # Current
    # ==================================================

    def set_current(self, current):

        self.current_setpoint = float(current)

    def read_current(self):

        if not self.enabled:
            return 0.0

        self.current = (
            self.current_setpoint +
            random.uniform(-0.15, 0.15)
        )

        return round(
            self.current,
            3
        )

    # ==================================================
    # Voltage
    # ==================================================

    def read_voltage(self):

        if not self.enabled:
            return 0.0

        current_amp = self.current / 1000.0

        voltage = (
            self.forward_voltage +
            current_amp * self.series_resistance
        )

        voltage += random.uniform(
            -0.003,
            0.003
        )

        return round(
            voltage,
            3
        )

    # ==================================================
    # Optical Power
    # ==================================================

    def read_optical_power(self):

        if not self.enabled:
            return 0.0

        # Threshold increases with temperature
        ith = (
            self.threshold_current +
            0.25 *
            (
                self.junction_temperature -
                25.0
            )
        )

        if self.current <= ith:

            power = 0.0

        else:

            power = (
                self.current -
                ith
            ) * self.slope_efficiency

            # Thermal roll-off
            power *= (
                1.0 -
                self.rolloff *
                self.current
            )

        power += random.uniform(
            -0.15,
            0.15
        )

        return round(
            max(power, 0.0),
            3
        )

    # ==================================================
    # Junction Temperature
    # ==================================================

    def set_junction_temperature(
        self,
        temperature
    ):

        self.junction_temperature = float(
            temperature
        )

    def get_junction_temperature(self):

        return round(
            self.junction_temperature,
            3
        )

    # ==================================================
    # Complete Measurement
    # ==================================================

    def get_measurement(self):

        return {

            "current": self.read_current(),

            "voltage": self.read_voltage(),

            "power": self.read_optical_power(),

            "junction_temperature":
                self.get_junction_temperature()

        }