"""
=========================================================
Device Factory

Creates either simulated devices or real hardware devices
depending on config.py.

Author : Sarthak Sinha
Version : 1.0
=========================================================
"""

from config import *

# --------------------------------------------------------
# Simulators
# --------------------------------------------------------

from simulators.avantes_sim import AvantesSimulator
from simulators.sf6100_sim import SF6100Simulator
from simulators.maestro_sim import MaestroSimulator
from simulators.tec3700_sim import TEC3700Simulator


# --------------------------------------------------------
# Real Drivers
# --------------------------------------------------------

from drivers.sf6100 import SF6100
from drivers.maestro import Maestro
from drivers.tec3700 import TEC3700


class DeviceFactory:

    def __init__(self, mode="simulation",detected_devices=None):

        self.mode = mode
        self.detected_devices = detected_devices or {}
        self.avantes = None
        self.sf6100 = None
        self.maestro = None
        self.tec = None

        self.create_devices()

    # =====================================================
    # Create Devices
    # =====================================================

    def create_devices(self):

        if self.mode == "simulation":

            print(f"Starting in {self.mode.capitalize()} Mode")

            self.sf6100 = SF6100Simulator()

            self.maestro = MaestroSimulator(
                self.sf6100
            )

            self.tec = TEC3700Simulator(
                self.sf6100
            )
            self.avantes = AvantesSimulator(
                self.sf6100,
                self.tec
            )
            
        elif self.mode == "hardware":

            print(f"Starting in {self.mode.capitalize()} Mode")

            sf6100_info = self.detected_devices.get(
                "SF6100",
                {}
            )

            sf6100_port = sf6100_info.get("port") or SF6100_PORT

            self.sf6100 = SF6100(
                port=sf6100_port
            )

            maestro_info = self.detected_devices.get("Maestro", {})

            maestro_port = (
                maestro_info.get("port")
                or MAESTRO_PORT
            )

            self.maestro = Maestro(
                port=maestro_port
            )

            tec_info = self.detected_devices.get("TEC3700", {})

            tec_port = (
                tec_info.get("port")
                or TEC3700_PORT
            )

            self.tec = TEC3700(
                port=tec_port
)
        else:

            raise ValueError(
                f"Unknown startup mode: {self.mode}"
            )