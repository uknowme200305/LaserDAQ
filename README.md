# LaserDAQ

**LaserDAQ** is a Python-based desktop application for controlling and characterizing semiconductor lasers using laboratory instruments.

The software provides a unified graphical interface to perform electrical, optical, and thermal characterization of laser diodes. It supports both **simulation mode** for development/testing and **hardware mode** for real laboratory measurements.

---

## Features

- Device scanning
- Connect / Disconnect instruments
- Manual instrument control
- Current sweep (L-I)
- Voltage sweep (V-I)
- Live plotting using PyQtGraph
- Laser parameter calculations
- CSV export
- PDF report generation
- Simulation mode for offline development

---

## Supported Instruments

| Instrument | Status |
|------------|--------|
| Maiman SF6100 Laser Driver | ✅ |
| Gentec Maestro Power Meter | ✅ |
| Newport TEC3700 Temperature Controller | ✅ |
| Avantes Spectrometer | ✅ Simulator / 🚧 Hardware Driver |
| DataRay Beamage 4M | 🚧 Planned |

---

## Technologies Used

- Python 3
- PyQt5
- Qt Designer
- PyQtGraph
- NumPy
- PySerial
- ReportLab
- Matplotlib

---

## Folder Structure

```text
LaserDAQ/

├── drivers/
├── simulators/
├── calculations/
├── utils/
├── tests/
├── Reports/
├── Logs/
├── assets/

├── main_V1B.py
├── config.py
├── laser_characterization_V1.ui

├── requirements.txt
├── README.md
└── .gitignore
```

---
## First-Time Setup

On Windows:

1. Double-click `setup.bat`
2. Wait for the installation to complete.
3. Double-click `run.bat` to launch LaserDAQ.

No manual package installation is required.

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/LaserDAQ.git
cd LaserDAQ
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it.

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running

```bash
python main_V1B.py
```

---

## Current Development Status

### Completed

- SF6100 Driver
- Maestro Driver
- TEC3700 Driver
- Avantes Simulator
- CSV Export
- PDF Report Generation
- Laser Parameter Calculations
- Live L-I Plot
- Live V-I Plot
- Optical Spectrum (Simulation)

### In Progress

- Avantes Hardware Driver
- Beamage Simulator
- Beamage Driver
- Executable Packaging

---

## Version Roadmap

### Version 0.3

- Avantes Simulator
- GUI Integration

### Version 0.4

- Beamage Support

### Version 1.0

- Complete Hardware Support
- Executable Release
- Laboratory Validation

---

## License

This project is currently under development.

---

## Author

**Sarthak Sinha**

Delhi Technological University (DTU)

Electronics and Communication Engineering

2023–2027