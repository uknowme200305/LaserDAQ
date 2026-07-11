import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from simulators.sf6100_sim import (
    SF6100Simulator
)


laser = SF6100Simulator()

laser.connect()

laser.enable()

laser.set_current(50)

for i in range(10):

    print(
        "Current:",
        laser.read_current()
    )

    print(
        "Voltage:",
        laser.read_voltage()
    )

    print()