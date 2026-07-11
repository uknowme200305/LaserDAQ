import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from simulators.sf6100_sim import SF6100Simulator
from simulators.maestro_sim import MaestroSimulator


# --------------------------------
# Create Devices
# --------------------------------

laser = SF6100Simulator()

maestro = MaestroSimulator(
    laser
)

# --------------------------------
# Connect Devices
# --------------------------------

laser.connect()

maestro.connect()

laser.enable()

print("\nVirtual Laser Lab\n")

# --------------------------------
# Sweep Current
# --------------------------------

for current in range(0, 110, 10):

    laser.set_current(current)

    measured_current = laser.read_current()

    voltage = laser.read_voltage()

    power = maestro.read_power()

    print(
        f"Set Current = {current:3d} mA | "
        f"Measured Current = {measured_current:6.2f} mA | "
        f"Voltage = {voltage:5.2f} V | "
        f"Power = {power:6.2f} mW"
    )