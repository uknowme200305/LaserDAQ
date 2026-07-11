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

from simulators.tec3700_sim import (
    TEC3700Simulator
)

# -------------------------------------
# CREATE SIMULATOR
# -------------------------------------

tec = TEC3700Simulator()


def print_separator():

    print("-" * 60)


try:

    print_separator()
    print("CONNECTING TO TEC3700...")
    print_separator()

    tec.connect()

    print("Connected :", tec.is_connected())

    print_separator()

    print("DEVICE IDENTIFICATION")

    print(tec.identify())

    print_separator()

    print("ENABLE OUTPUT")

    tec.enable_output()

    print("Output Enabled :", tec.output_enabled_status())

    print_separator()

    print("SET TEMPERATURE")

    tec.set_temperature(30.0)

    print("Temperature Setpoint :", tec.read_setpoint(), "°C")

    print_separator()

    print("TEMPERATURE STABILIZATION")

    for i in range(20):

        temperature = tec.read_temperature()
        current = tec.read_current()
        voltage = tec.read_voltage()

        print(
            f"{i+1:02d} | "
            f"T = {temperature:.3f} °C | "
            f"I = {current:.3f} A | "
            f"V = {voltage:.3f} V"
        )

        time.sleep(0.25)

    print_separator()

    print("CURRENT LIMIT")

    tec.set_current_limit(5)

    print(
        "Current Limit :",
        tec.read_current_limit(),
        "A"
    )

    print_separator()

    print("VOLTAGE LIMIT")

    tec.set_voltage_limit(12)

    print(
        "Voltage Limit :",
        tec.read_voltage_limit(),
        "V"
    )

    print_separator()

    print("HIGH TEMPERATURE LIMIT")

    tec.set_high_temperature_limit(50)

    print(
        "High Temp Limit :",
        tec.read_high_temperature_limit(),
        "°C"
    )

    print_separator()

    print("LOW TEMPERATURE LIMIT")

    tec.set_low_temperature_limit(10)

    print(
        "Low Temp Limit :",
        tec.read_low_temperature_limit(),
        "°C"
    )

    print_separator()

    print("CURRENT MODE")

    tec.set_current_mode()

    print(
        "Mode :",
        tec.get_mode()
    )

    tec.set_current(2.5)

    print(
        "Current Setpoint :",
        tec.read_current_setpoint(),
        "A"
    )

    for i in range(10):

        current = tec.read_current()
        voltage = tec.read_voltage()

        print(
            f"{i+1:02d} | "
            f"I = {current:.3f} A | "
            f"V = {voltage:.3f} V"
        )

        time.sleep(0.25)

    print_separator()

    print("TEMPERATURE MODE")

    tec.set_temperature_mode()

    print(
        "Mode :",
        tec.get_mode()
    )

    print_separator()

    print("STATUS")

    print(
        tec.get_status()
    )

    print_separator()

    print("GENERIC MEASUREMENT")

    measurement = tec.get_measurement()

    for key, value in measurement.items():

        print(f"{key:12s}: {value}")

    print_separator()

    print("DISABLE OUTPUT")

    tec.disable_output()

    print(
        "Output Enabled :",
        tec.output_enabled_status()
    )

    print_separator()

    tec.disconnect()

    print("Disconnected")

    print_separator()

except Exception as e:

    print()
    print("TEST FAILED")
    print(e)