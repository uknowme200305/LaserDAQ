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

    def __init__(self):

        self.mode = "Simulation" if SIMULATION_MODE else "Hardware"
        self.avantes = None
        self.sf6100 = None
        self.maestro = None
        self.tec = None

        self.create_devices()

    # =====================================================
    # Create Devices
    # =====================================================

    def create_devices(self):

        if SIMULATION_MODE:

            print("Starting in Simulation Mode")

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
            
        else:

            print("Starting in Hardware Mode")

            self.sf6100 = SF6100(
                port=SF6100_PORT
            )

            self.maestro = Maestro(
                port=MAESTRO_PORT
            )

            self.tec = TEC3700(
                port=TEC3700_PORT
            )