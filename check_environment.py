"""
LaserDAQ Environment Checker

Verifies that the development environment is ready
to run LaserDAQ.
"""

import os
import sys
import importlib

print("=" * 55)
print("           LaserDAQ Environment Check")
print("=" * 55)


def check_python():

    print("\nPython")

    version = sys.version_info

    print(f"Version : {version.major}.{version.minor}.{version.micro}")

    if version.major >= 3 and version.minor >= 10:
        print("Status  : OK")
    else:
        print("Status  : Upgrade Recommended")


def check_package(package):

    try:

        importlib.import_module(package)

        print(f"{package:<20} OK")

    except ImportError:

        print(f"{package:<20} MISSING")


def check_file(filename):

    if os.path.exists(filename):

        print(f"{filename:<35} FOUND")

    else:

        print(f"{filename:<35} MISSING")


def check_folder(folder):

    if os.path.isdir(folder):

        print(f"{folder:<35} FOUND")

    else:

        print(f"{folder:<35} MISSING")


check_python()

print("\nPackages")
print("-" * 55)

packages = [

    "PyQt5",

    "numpy",

    "pyqtgraph",

    "serial",

    "matplotlib",

    "reportlab"

]

for package in packages:

    check_package(package)

print("\nFiles")
print("-" * 55)

check_file("main_V1B.py")

check_file("config.py")

check_file("laser_characterization_V1.ui")

check_file("requirements.txt")

print("\nFolders")
print("-" * 55)

check_folder("drivers")

check_folder("simulators")

check_folder("calculations")

check_folder("utils")

check_folder("tests")

check_folder("Reports")

check_folder("Logs")

check_folder("assets")

print("\nConfiguration")
print("-" * 55)

try:

    from config import SIMULATION_MODE

    print("Configuration Loaded")

    print(f"Simulation Mode : {SIMULATION_MODE}")

except Exception:

    print("Configuration Error")

print("\nEnvironment Check Complete.")
print("=" * 55)