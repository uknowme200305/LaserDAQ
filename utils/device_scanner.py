"""
device_scanner.py

Version 1

Scans for available laboratory instruments.

Simulation Mode:
Always reports simulated devices as available.

Hardware Mode:
Later this file will search COM ports and identify
real instruments.
"""
from config import SIMULATION_MODE



class DeviceScanner:

    def __init__(self):

        pass

    # ==========================================
    # Scan Devices
    # ==========================================

    def scan_devices(self):

        devices = {

            "SF6100": False,
            "Maestro": False,
            "TEC3700": False,
            "Avantes": False,
            "Beamage": False

        }

        # --------------------------------------
        # Simulation Mode
        # --------------------------------------

        if SIMULATION_MODE:

            devices["SF6100"] = True
            devices["Maestro"] = True
            devices["TEC3700"] = True
            devices["Avantes"] = True

            return devices

        # --------------------------------------
        # Hardware Mode
        # --------------------------------------

        #
        # This section will be implemented later.
        #
        # Example:
        #
        # import serial.tools.list_ports
        #
        # ports = serial.tools.list_ports.comports()
        #
        # for port in ports:
        #
        #     ...
        #

        return devices