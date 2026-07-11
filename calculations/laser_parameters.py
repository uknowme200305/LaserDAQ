import numpy as np


class LaserParameters:

    def __init__(
        self,
        current,
        power,
        voltage
    ):

        self.current = np.array(current, dtype=float)
        self.power = np.array(power, dtype=float)
        self.voltage = np.array(voltage, dtype=float)

    # ======================================================
    # Maximum Optical Power
    # ======================================================

    def max_power(self):

        return float(
            np.max(self.power)
        )

    # ======================================================
    # Operating Current
    # ======================================================

    def operating_current(self):

        idx = np.argmax(
            self.power
        )

        return float(
            self.current[idx]
        )

    # ======================================================
    # Forward Voltage
    # ======================================================

    def forward_voltage(self):

        idx = np.argmax(
            self.power
        )

        return float(
            self.voltage[idx]
        )

    # ======================================================
    # Differential Resistance
    # ======================================================

    def differential_resistance(self):

        if len(self.current) < 2:

            return 0.0

        n = min(
            5,
            len(self.current)
        )

        x = self.current[-n:]

        y = self.voltage[-n:]

        slope, intercept = np.polyfit(
            x,
            y,
            1
        )

        # Convert V/mA to Ohms
        return float(
            slope * 1000
        )

    # ======================================================
    # Threshold Current
    # ======================================================
    def best_linear_fit(self):

        if len(self.current) < 8:
            return None

        window = 6

        best_r2 = -1

        best_slope = 0
        best_intercept = 0

        for i in range(len(self.current) - window + 1):

            x = self.current[i:i + window]
            y = self.power[i:i + window]

            slope, intercept = np.polyfit(
                x,
                y,
                1
            )

            y_fit = slope * x + intercept

            ss_res = np.sum(
                (y - y_fit) ** 2
            )

            ss_tot = np.sum(
                (y - np.mean(y)) ** 2
            )

            if ss_tot == 0:
                continue

            r2 = 1 - ss_res / ss_tot

            if slope > 0 and r2 > best_r2:

                best_r2 = r2
                best_slope = slope
                best_intercept = intercept

        return (
            best_slope,
            best_intercept,
            best_r2
        )

    def threshold_current(self):

        fit = self.best_linear_fit()

        if fit is None:
            return 0.0

        slope, intercept, _ = fit

        return float(
            -intercept / slope
        )

    # ======================================================
    # Slope Efficiency
    # ======================================================

    def slope_efficiency(self):

        fit = self.best_linear_fit()

        if fit is None:
            return 0.0

        slope, _, _ = fit

        return float(
            slope
        )

    # ======================================================
    # Calculate Everything
    # ======================================================

    def calculate(self):

        return {

            "threshold_current":
                round(
                    self.threshold_current(),
                    3
                ),

            "slope_efficiency":
                round(
                    self.slope_efficiency(),
                    3
                ),

            "forward_voltage":
                round(
                    self.forward_voltage(),
                    3
                ),

            "differential_resistance":
                round(
                    self.differential_resistance(),
                    3
                ),

            "maximum_power":
                round(
                    self.max_power(),
                    3
                ),

            "operating_current":
                round(
                    self.operating_current(),
                    3
                )

        }