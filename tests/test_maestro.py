import sys
import os
import time

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from drivers.maestro import Maestro


# -------------------------------------
# CHANGE THIS TO YOUR PORT
# -------------------------------------

PORT = "COM4"


def print_separator():

    print("-" * 50)


try:

    maestro = Maestro(PORT)

    print_separator()
    print("CONNECTING TO MAESTRO...")
    print_separator()

    maestro.connect()

    print("Connected :", maestro.is_connected())

    print_separator()

    print("PING")

    try:
        print(maestro.ping())
    except Exception as e:
        print(e)

    print_separator()

    print("FIRMWARE")

    try:
        print(maestro.identify())
    except Exception as e:
        print(e)

    print_separator()

    print("STATUS")

    try:
        print(maestro.get_status())
    except Exception as e:
        print(e)

    print_separator()

    print("POWER READINGS")

    readings = []

    for i in range(10):

        try:

            power = maestro.read_power()

            readings.append(power)

            print(
                f"{i+1:02d} : {power:.6f} W"
            )

        except Exception as e:

            print(e)

        time.sleep(0.2)

    print_separator()

    if len(readings) > 0:

        average = sum(readings) / len(readings)

        print(f"Average Power : {average:.6f} W")

        print(f"Maximum Power : {max(readings):.6f} W")

        print(f"Minimum Power : {min(readings):.6f} W")

    print_separator()

    maestro.disconnect()

    print("Disconnected")

    print_separator()

except Exception as e:

    print()

    print("TEST FAILED")

    print(e)