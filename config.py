"""
=========================================================
Laser Characterization Software
Configuration File
=========================================================

Modify this file to switch between Simulation Mode
and Real Hardware Mode.

Author : Sarthak Sinha
Version : 1.0
"""

# =========================================================
# SOFTWARE INFORMATION
# =========================================================

SOFTWARE_NAME = "Laser Characterization Software"

SOFTWARE_VERSION = "1.0"

LAB_NAME = "Photonics Laboratory"

ORGANIZATION = "Delhi Technological University"


# =========================================================
# SIMULATION / HARDWARE MODE
# =========================================================

# True  -> Use Simulators
# False -> Use Real Instruments

SIMULATION_MODE = True


# =========================================================
# COMMUNICATION PORTS
# =========================================================

SF6100_PORT = "COM3"

MAESTRO_PORT = "COM4"

TEC3700_PORT = "COM5"

AVANTES_PORT = "USB"

BEAMAGE_PORT = "USB"


# =========================================================
# DEFAULT SAVE LOCATION
# =========================================================

DEFAULT_SAVE_DIRECTORY = "Reports"


# =========================================================
# PLOT SETTINGS
# =========================================================

PLOT_WIDTH = 1200

PLOT_HEIGHT = 800


# =========================================================
# PDF SETTINGS
# =========================================================

PDF_AUTHOR = "Sarthak Sinha"

PDF_TITLE = "Laser Characterization Report"

PDF_SUBJECT = "Semiconductor Laser Characterization"

PDF_KEYWORDS = [
    "Laser",
    "Characterization",
    "L-I",
    "V-I",
    "Semiconductor Laser"
]


# =========================================================
# DEFAULT TEC SETTINGS
# =========================================================

DEFAULT_TEMPERATURE = 25.0


# =========================================================
# SWEEP SETTINGS
# =========================================================

DEFAULT_START_CURRENT = 0

DEFAULT_STOP_CURRENT = 100

DEFAULT_STEP_SIZE = 5

SWEEP_INTERVAL_MS = 500


# =========================================================
# APPLICATION SETTINGS
# =========================================================

ENABLE_LOGGING = True

AUTO_SCAN_ON_STARTUP = False

AUTO_CONNECT = False


# =========================================================
# FUTURE FEATURES
# =========================================================

ENABLE_AVANTES = False

ENABLE_BEAMAGE = False