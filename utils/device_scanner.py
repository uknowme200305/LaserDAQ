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

import serial.tools.list_ports

from drivers.sf6100 import SF6100
from drivers.tec3700 import TEC3700
from drivers.maestro import Maestro



class DeviceScanner:

    def __init__(self, mode="simulation"):

        self.mode = mode

    # ==========================================
    # Scan SF6100
    # ==========================================

    def _scan_sf6100(self, devices, ports, used_ports):

        

        for port in ports:

            if port.device in used_ports:
                continue
            try:

                print(f"Checking {port.device} for SF6100...")

                driver = SF6100(port.device)

                if not driver.connect():
                    continue

                try:

                    response = driver.identify()

                    if response.startswith("K0702"):

                        print(f"SF6100 detected on {port.device}")

                        devices["SF6100"]["available"] = True
                        devices["SF6100"]["port"] = port.device
                        used_ports.add(port.device)

                        return

                finally:

                    driver.disconnect()

            except Exception as e:
                print(f"{port.device}: {e}")

    # ==========================================
    # Scan TEC3700
    # ==========================================
    def _scan_tec3700(self, devices, ports, used_ports):

        

        for port in ports:
            
            if port.device in used_ports:
                continue
            try:

                print(f"Checking {port.device} for TEC3700...")

                driver = TEC3700(port.device)

                if not driver.connect():
                    continue

                try:

                    response = driver.identify()

                    print(response)

                    response_upper = response.upper()

                    if (
                        "NEWPORT" in response_upper
                        and "3700" in response_upper
                    ):

                        print(
                            f"TEC3700 detected on {port.device}"
                        )

                        devices["TEC3700"]["available"] = True
                        devices["TEC3700"]["port"] = port.device
                        used_ports.add(port.device)

                        return

                finally:

                    driver.disconnect()

            except Exception as e:
                print(f"{port.device}: {e}")


    # ==========================================
    # Scan Maestro
    # ==========================================

    def _scan_maestro(self, devices, ports, used_ports):

        

        for port in ports:

            if port.device in used_ports:
                continue

            try:

                print(f"Checking {port.device} for Maestro...")

                driver = Maestro(port.device)

                if not driver.connect():
                    continue

                try:

                    response = driver.identify()

                    print(response)

                    response_upper = response.upper()

                    #
                    # Accept any valid firmware/version response
                    #
                    if response.strip():

                        print(
                            f"Maestro detected on {port.device}"
                        )

                        devices["Maestro"]["available"] = True
                        devices["Maestro"]["port"] = port.device
                        used_ports.add(port.device)

                        return

                finally:

                    driver.disconnect()

            except Exception as e:
                print(f"{port.device}: {e}")

    # ==========================================
    # Scan Devices
    # ==========================================

    def scan_devices(self):

        devices = {

            "SF6100": {
                "available": False,
                "port": None
            },

            "Maestro": {
                "available": False,
                "port": None
            },

            "TEC3700": {
                "available": False,
                "port": None
            },

            "Avantes": {
                "available": False,
                "port": None
            },

            "Beamage": {
                "available": False,
                "port": None
            }

        }

        # --------------------------------------
        # Simulation Mode
        # --------------------------------------

        if self.mode == "simulation":

            devices["SF6100"]["available"] = True
            devices["Maestro"]["available"] = True
            devices["TEC3700"]["available"] = True
            devices["Avantes"]["available"] = True

            return devices

        

        # --------------------------------------
        # Hardware Mode
        # --------------------------------------

        ports = list(serial.tools.list_ports.comports())
        used_ports = set()

        self._scan_sf6100(devices, ports, used_ports)

        self._scan_tec3700(devices, ports, used_ports)

        self._scan_maestro(devices, ports, used_ports)

        return devices