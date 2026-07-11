"""
=========================================================
Avantes Spectrometer Simulator

Simulates an Avantes USB Spectrometer.

Provides realistic semiconductor laser spectra for
software development and GUI testing.

Author : Sarthak Sinha
Version : 1.0
=========================================================
"""

import random
import numpy as np


class AvantesSimulator:

    def __init__(self, sf6100, tec):

        self.connected = False

        # -------------------------------------------------
        # References to other simulated devices
        # -------------------------------------------------

        self.sf6100 = sf6100
        self.tec = tec

        # -------------------------------------------------
        # Measurement Settings
        # -------------------------------------------------

        self.integration_time = 10.0      # ms

        # -------------------------------------------------
        # Spectrometer Configuration
        # -------------------------------------------------

        self.num_pixels = 2048

        self.start_wavelength = 850.0
        self.stop_wavelength = 1050.0

        # -------------------------------------------------
        # Laser Characteristics
        # -------------------------------------------------

        self.nominal_center = 980.0       # nm

        self.fwhm = 2.5                   # nm

        self.max_peak_counts = 55000

        self.background = 150

        self.noise_level = 80

        # -------------------------------------------------

        self.wavelengths = self._generate_wavelength_axis()

        self.intensities = np.zeros(self.num_pixels)

    # =====================================================
    # Connection
    # =====================================================

    def connect(self):

        self.connected = True

        return True

    def disconnect(self):

        self.connected = False

    def is_connected(self):

        return self.connected

    # =====================================================
    # Integration Time
    # =====================================================

    def set_integration_time(self, integration_time_ms):

        self.integration_time = float(integration_time_ms)

    def get_integration_time(self):

        return self.integration_time

    # =====================================================
    # Measurement
    # =====================================================

    def start_measurement(self):

        if not self.connected:

            raise ConnectionError(
                "Avantes Spectrometer not connected."
            )

        self.intensities = self._generate_spectrum()

    def get_spectrum(self):

        self.start_measurement()

        return (

            self.wavelengths,

            self.intensities

        )

    # =====================================================
    # Peak Wavelength
    # =====================================================

    def get_peak_wavelength(self):

        if len(self.intensities) == 0:

            return 0.0

        index = np.argmax(self.intensities)

        return round(

            float(self.wavelengths[index]),

            3

        )

    # =====================================================
    # FWHM
    # =====================================================

    def get_fwhm(self):

        if np.max(self.intensities) <= 0:

            return 0.0

        half_max = np.max(self.intensities) / 2

        indices = np.where(

            self.intensities >= half_max

        )[0]

        if len(indices) < 2:

            return 0.0

        left = indices[0]

        right = indices[-1]

        width = (

            self.wavelengths[right]

            - self.wavelengths[left]

        )

        return round(

            float(width),

            3

        )

    # =====================================================
    # Complete Measurement
    # =====================================================

    def get_measurement(self):

        wavelengths, intensities = self.get_spectrum()

        return {

            "wavelengths": wavelengths,

            "intensities": intensities,

            "peak_wavelength":
                self.get_peak_wavelength(),

            "fwhm":
                self.get_fwhm()

        }

    # =====================================================
    # Generate Wavelength Axis
    # =====================================================

    def _generate_wavelength_axis(self):

        return np.linspace(

            self.start_wavelength,

            self.stop_wavelength,

            self.num_pixels

        )

    # =====================================================
    # Generate Spectrum
    # =====================================================

    def _generate_spectrum(self):

        # --------------------------------------------
        # Laser Current
        # --------------------------------------------

        current = self.sf6100.read_current()

        # --------------------------------------------
        # Laser Enabled?
        # --------------------------------------------

        if (

            not self.sf6100.enabled

            or

            current <= self.sf6100.threshold_current

        ):

            peak = 0

        else:

            peak = (

                (current -

                 self.sf6100.threshold_current)

                *

                self.sf6100.slope_efficiency

                *

                900

            )

            peak = min(

                peak,

                self.max_peak_counts

            )

        # --------------------------------------------
        # Integration Time Scaling
        # --------------------------------------------

        peak *= (

            self.integration_time

            / 10.0

        )

        peak = min(

            peak,

            65535

        )

        # --------------------------------------------
        # Temperature Shift
        # --------------------------------------------

        temperature = self.tec.read_temperature()

        center = (

            self.nominal_center

            +

            0.30 *

            (temperature - 25)

        )

        center += random.uniform(

            -0.02,

            0.02

        )

        # --------------------------------------------
        # Gaussian Width
        # --------------------------------------------

        sigma = self.fwhm / 2.355

        spectrum = (

            peak

            *

            np.exp(

                -((

                    self.wavelengths

                    - center

                ) ** 2)

                /

                (

                    2

                    *

                    sigma ** 2

                )

            )

        )

        # --------------------------------------------
        # Background
        # --------------------------------------------

        spectrum += self.background

        # --------------------------------------------
        # Detector Noise
        # --------------------------------------------

        noise = np.random.normal(

            0,

            self.noise_level,

            self.num_pixels

        )

        spectrum += noise

        # --------------------------------------------
        # Prevent Negative Values
        # --------------------------------------------

        spectrum = np.clip(

            spectrum,

            0,

            None

        )

        return spectrum