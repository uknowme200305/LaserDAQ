import sys
import random
from datetime import datetime
from simulators.sf6100_sim import SF6100Simulator
from simulators.maestro_sim import MaestroSimulator
from simulators.tec3700_sim import TEC3700Simulator
from calculations.laser_parameters import LaserParameters
from utils.device_scanner import DeviceScanner
from utils.pdf_export import generate_pdf
from pyqtgraph.exporters import ImageExporter
from config import *
from utils.device_factory import DeviceFactory

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QTableWidgetItem
)

from PyQt5.QtCore import QTimer
from PyQt5 import uic

import pyqtgraph as pg
import csv
from datetime import datetime
from PyQt5.QtWidgets import QFileDialog


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.laser_results = {
            "threshold_current": 0.0,
            "slope_efficiency": 0.0,
            "forward_voltage": 0.0,
            "differential_resistance": 0.0,
            "maximum_power": 0.0,
            "operating_current": 0.0
        }

        # Load UI
        uic.loadUi("laser_characterization_V1.ui", self)

        # ==========================================
        # Initial Connection Status
        # ==========================================

        status_labels = [
            self.sf6100Status,
            self.maestroStatus,
            self.newportStatus,
            self.avantesStatus,
            self.newportStatus_2
        ]

        for label in status_labels:

            label.setText("🔴 Disconnected")

            label.setStyleSheet(
                "color:red; font-weight:bold;"
            )
        # -------------------------
        # Laser Parameter Labels
        # -------------------------

        self.thresholdLabel = self.label_10
        self.slopeLabel = self.label_12
        self.seriesResistanceLabel = self.label_19
        self.peakLabel = self.peakWavelengthLabel
        self.fwhmDisplayLabel = self.fwhmLabel

        # -------------------------
        # Create L-I Plot
        # -------------------------
        self.li_plot = pg.PlotWidget()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.li_plot)

        self.liPlotWidget.setLayout(layout)

        self.li_plot.setTitle("L-I Curve")
        self.li_plot.setLabel('left', 'Power (mW)')
        self.li_plot.setLabel('bottom', 'Current (mA)')
        self.li_plot.showGrid(x=True, y=True)
        # Create curve only once
        self.li_curve = self.li_plot.plot(
            pen='y',
            symbol='o'
        )

        # -------------------------
        # Create V-I Plot
        # -------------------------

        self.vi_plot = pg.PlotWidget()

        vi_layout = QVBoxLayout()
        vi_layout.setContentsMargins(0, 0, 0, 0)

        vi_layout.addWidget(
            self.vi_plot
        )

        self.viPlotWidget.setLayout(
            vi_layout
        )

        self.vi_plot.setTitle(
            "V-I Curve"
        )

        self.vi_plot.setLabel(
            'left',
            'Voltage (V)'
        )

        self.vi_plot.setLabel(
            'bottom',
            'Current (mA)'
        )

        self.vi_plot.showGrid(
            x=True,
            y=True
        )

        self.vi_curve = self.vi_plot.plot(
            pen='c',
            symbol='o'
        )

        # -------------------------
        # Create Spectrum Plot
        # -------------------------

        self.spectrum_plot = pg.PlotWidget()

        spectrum_layout = QVBoxLayout()

        spectrum_layout.setContentsMargins(0, 0, 0, 0)

        spectrum_layout.addWidget(
            self.spectrum_plot
        )

        self.spectrumPlotWidget.setLayout(
            spectrum_layout
        )

        self.spectrum_plot.setTitle(
            "Optical Spectrum"
        )

        self.spectrum_plot.setLabel(
            'left',
            'Intensity (Counts)'
        )

        self.spectrum_plot.setLabel(
            'bottom',
            'Wavelength (nm)'
        )

        self.spectrum_plot.showGrid(
            x=True,
            y=True
        )

        self.spectrum_curve = self.spectrum_plot.plot(
            pen='m'
        )
        # -------------------------
        # Data Storage
        # -------------------------
        self.saveDataButton.clicked.connect(
            self.save_data
        )
        self.current_data = []
        self.power_data = []
        self.voltage_data = []
        self.temperature_data = []
        self.current_spectrum_wavelengths = None

        self.current_spectrum_intensities = None

        # -------------------------
        # Sweep Timer
        # -------------------------
        self.sweepTimer = QTimer()

        self.sweepTimer.timeout.connect(
            self.take_measurement
        )

        # -------------------------
        # Button Connections
        # -------------------------
        self.startSweepButton.clicked.connect(
            self.start_sweep
        )

        self.stopSweepButton.clicked.connect(
            self.stop_sweep
        )

        self.log("Laser Characterization Software Started")

        # --------------------------------
        # Create Simulated Devices
        # --------------------------------

        factory = DeviceFactory()

        self.sf6100 = factory.sf6100

        self.maestro = factory.maestro

        self.tec = factory.tec

        self.avantes = factory.avantes

        self.scanner = DeviceScanner()
        
        self.tec.set_temperature(DEFAULT_TEMPERATURE)

        

        # ==========================================
        # Connection Buttons
        # ==========================================

        self.pushButton.clicked.connect(
            self.connect_sf6100
        )

        self.pushButton_3.clicked.connect(
            self.connect_maestro
        )

        self.pushButton_5.clicked.connect(
            self.connect_tec
        )

        self.pushButton_4.clicked.connect(
            self.connect_avantes
        )

        self.pushButton_6.clicked.connect(
            self.connect_beamage
        )

        self.pushButton_2.clicked.connect(
            self.scan_devices
        )
        self.exportPDFButton.clicked.connect(
            self.export_pdf
        )
        #disconnecting avantes and beamage for now since they are not implemented yet
        
        self.pushButton_6.setEnabled(False)

    # ==========================================
    # EXPORT PLOTS
    # ==========================================

    def export_plots(self):

        li_exporter = ImageExporter(
            self.li_plot.plotItem
        )

        li_exporter.parameters()['width'] = PLOT_WIDTH

        li_exporter.export("li_curve.png")

        vi_exporter = ImageExporter(
            self.vi_plot.plotItem
        )

        vi_exporter.parameters()['width'] = PLOT_WIDTH

        vi_exporter.export("vi_curve.png")


    # ==========================================
    # EXPORT PDF
    # ==========================================


    def export_pdf(self):

        if len(self.current_data) == 0:
            self.log("No data to export.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        default_name = f"Laser_Report_{timestamp}.pdf"

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export PDF",
            default_name,
            "PDF Files (*.pdf)"
        )

        if not filename:
            return

        # Export graphs first
        self.export_plots()

        connected_devices = {

            "SF6100": self.sf6100.is_connected(),

            "Maestro": self.maestro.is_connected(),

            "TEC3700": self.tec.is_connected(),

            "Avantes": False,

            "Beamage": False

        }

        generate_pdf(

            filename,

            self.laser_results,

            self.current_data,

            self.power_data,

            self.voltage_data,

            self.temperature_data,

            "li_curve.png",

            "vi_curve.png",

            simulation_mode=SIMULATION_MODE,

            connected_devices=connected_devices

        )

        self.log(f"PDF exported: {filename}")
    # ==========================================
    # SCAN DEVICES
    # ==========================================

    def scan_devices(self):

        devices = self.scanner.scan_devices()

        # ------------------------------
        # SF6100
        # ------------------------------

        if devices["SF6100"]:

            self.sf6100Status.setText(
                "🟡 Available"
            )

            self.sf6100Status.setStyleSheet(
                "color: orange; font-weight:bold;"
            )

            self.log("SF6100 Found")

        # ------------------------------
        # Maestro
        # ------------------------------

        if devices["Maestro"]:

            self.maestroStatus.setText(
                "🟡 Available"
            )

            self.maestroStatus.setStyleSheet(
                "color: orange; font-weight:bold;"
            )

            self.log("Maestro Found")

        # ------------------------------
        # AVANTES
        # ------------------------------
        if devices["Avantes"]:

            self.avantesStatus.setText(
                "🟡 Available"
            )

            self.avantesStatus.setStyleSheet(
                "color:orange; font-weight:bold;"
            )

            self.log(
                "Avantes Found"
            )

        # ------------------------------
        # TEC
        # ------------------------------

        if devices["TEC3700"]:

            self.newportStatus.setText(
                "🟡 Available"
            )

            self.newportStatus.setStyleSheet(
                "color: orange; font-weight:bold;"
            )

            self.log("TEC3700 Found")

        self.log("Device Scan Finished")
    # ==========================================
    # CONNECT / DISCONNECT SF6100
    # ==========================================

    def connect_sf6100(self):

        # --------------------------------------
        # Disconnect
        # --------------------------------------

        if self.sf6100.is_connected():

            self.sf6100.disable()
            self.sf6100.disconnect()

            self.sf6100Status.setText("🔴 Disconnected")

            self.sf6100Status.setStyleSheet(
                "color: red; font-weight: bold;"
            )

            self.pushButton.setText("Connect SF6100")

            self.log("SF6100 Disconnected")

            return

        # --------------------------------------
        # Connect
        # --------------------------------------

        try:

            self.sf6100.connect()

            self.sf6100.enable()

            self.sf6100Status.setText("🟢 Connected")

            self.sf6100Status.setStyleSheet(
                "color: green; font-weight: bold;"
            )

            self.pushButton.setText("Disconnect SF6100")

            self.log("SF6100 Connected")

        except Exception as e:

            self.sf6100Status.setText("🔴 Disconnected")

            self.sf6100Status.setStyleSheet(
                "color: red; font-weight: bold;"
            )

            self.pushButton.setText("Connect SF6100")

            self.log(f"SF6100 Connection Failed : {e}")
        
    # ==========================================
    # CONNECT / DISCONNECT MAESTRO
    # ==========================================

    def connect_maestro(self):

        if self.maestro.is_connected():

            self.maestro.disconnect()

            self.maestroStatus.setText("🔴 Disconnected")

            self.maestroStatus.setStyleSheet(
                "color:red; font-weight:bold;"
            )

            self.pushButton_3.setText(
                "Connect Maestro"
            )

            self.log("Maestro Disconnected")

            return

        try:

            self.maestro.connect()

            self.maestroStatus.setText("🟢 Connected")

            self.maestroStatus.setStyleSheet(
                "color:green; font-weight:bold;"
            )

            self.pushButton_3.setText(
                "Disconnect Maestro"
            )

            self.log("Maestro Connected")

        except Exception as e:

            self.log(
                f"Maestro Connection Failed : {e}"
            )

    # ==========================================
    # CONNECT / DISCONNECT TEC
    # ==========================================

    def connect_tec(self):

        if self.tec.is_connected():

            self.tec.disable_output()

            self.tec.disconnect()

            self.newportStatus.setText(
                "🔴 Disconnected"
            )

            self.newportStatus.setStyleSheet(
                "color:red; font-weight:bold;"
            )

            self.pushButton_5.setText(
                "Connect TEC"
            )

            self.log("TEC3700 Disconnected")

            return

        try:

            self.tec.connect()

            self.tec.enable_output()

            self.newportStatus.setText(
                "🟢 Connected"
            )

            self.newportStatus.setStyleSheet(
                "color:green; font-weight:bold;"
            )

            self.pushButton_5.setText(
                "Disconnect TEC"
            )

            self.log("TEC3700 Connected")

        except Exception as e:

            self.log(
                f"TEC3700 Connection Failed : {e}"
            )

    # ==========================================
    # CONNECT AVANTES
    # ==========================================

    def connect_avantes(self):

        if self.avantes.is_connected():

            self.avantes.disconnect()

            self.avantesStatus.setText(
                "🔴 Disconnected"
            )

            self.avantesStatus.setStyleSheet(
                "color:red; font-weight:bold;"
            )

            self.pushButton_4.setText(
                "Connect Avantes"
            )

            self.log(
                "Avantes Disconnected"
            )

            return

        try:

            self.avantes.connect()

            self.avantesStatus.setText(
                "🟢 Connected"
            )

            self.avantesStatus.setStyleSheet(
                "color:green; font-weight:bold;"
            )

            self.pushButton_4.setText(
                "Disconnect Avantes"
            )

            self.log(
                "Avantes Connected"
            )

        except Exception as e:

            self.log(
                f"Avantes Connection Failed : {e}"
            )

    # ==========================================
    # CONNECT BEAMAGE
    # ==========================================

    def connect_beamage(self):

        self.log(
            "Beamage Driver Not Implemented Yet"
        )

    # ================================
    # SAVE DATA FUNCTION
    # ================================
    def save_data(self):

        if len(self.current_data) == 0:
            print("No data to save")
            return

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        default_name = f"LI_Sweep_{timestamp}.csv"

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Data",
            default_name,
            "CSV Files (*.csv)"
        )

        if not filename:
            return

        with open(filename, "w", newline="") as file:

            writer = csv.writer(file)

            # ============================================
            # REPORT HEADER
            # ============================================

            writer.writerow(["LASER CHARACTERIZATION REPORT"])
            writer.writerow([])

            writer.writerow([
                "Date",
                datetime.now().strftime("%Y-%m-%d")
            ])

            writer.writerow([
                "Time",
                datetime.now().strftime("%H:%M:%S")
            ])

            writer.writerow([])

            # ============================================
            # LASER PARAMETERS
            # ============================================

            writer.writerow(["CALCULATED LASER PARAMETERS"])

            writer.writerow([
                "Threshold Current (mA)",
                self.laser_results["threshold_current"]
            ])

            writer.writerow([
                "Slope Efficiency (mW/mA)",
                self.laser_results["slope_efficiency"]
            ])

            writer.writerow([
                "Forward Voltage (V)",
                self.laser_results["forward_voltage"]
            ])

            writer.writerow([
                "Differential Resistance (Ohm)",
                self.laser_results["differential_resistance"]
            ])

            writer.writerow([
                "Maximum Optical Power (mW)",
                self.laser_results["maximum_power"]
            ])

            writer.writerow([
                "Operating Current (mA)",
                self.laser_results["operating_current"]
            ])

            writer.writerow([])
            writer.writerow([])

            # ============================================
            # RAW MEASUREMENT DATA
            # ============================================

            writer.writerow(["RAW MEASUREMENT DATA"])

            writer.writerow([
                "Current (mA)",
                "Power (mW)",
                "Voltage (V)",
                "Temperature (°C)"
            ])

            for i in range(len(self.current_data)):

                writer.writerow([
                    round(self.current_data[i], 3),
                    round(self.power_data[i], 3),
                    round(self.voltage_data[i], 3),
                    round(self.temperature_data[i], 3)
                ])

        print("Data Saved:", filename)
        self.log(f"Data Saved: {filename}")

    # ================================
    # LOGGING FUNCTION
    # ================================
    def log(self, message):

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.connectionLog.appendPlainText(
            f"[{timestamp}] {message}"
        )

    # ====================================
    # UPDATE LASER PARAMETERS
    # ====================================

    def update_laser_parameters(self, results):

        self.thresholdLabel.setText(
            f"Threshold Current (Ith) = "
            f"{results['threshold_current']:.2f} mA"
        )

        self.slopeLabel.setText(
            f"Slope Efficiency = "
            f"{results['slope_efficiency']:.3f} mW/mA"
        )

        self.seriesResistanceLabel.setText(
            f"Series Resistance (Rs) = "
            f"{results['differential_resistance']:.2f} Ω"
        )
    # ====================================
    # START SWEEP
    # ====================================

    def start_sweep(self):
        # ==========================================
        # Check Device Connections
        # ==========================================

        if not self.sf6100.is_connected():

            self.log("ERROR : SF6100 not connected.")

            return

        if not self.maestro.is_connected():

            self.log("ERROR : Maestro not connected.")

            return

        if not self.tec.is_connected():

            self.log("ERROR : TEC3700 not connected.")

            return
        try:

            self.start_current = float(
                self.startCurrentInput.text()
            )

            self.stop_current = float(
                self.stopCurrentInput.text()
            )

            self.step_size = float(
                self.stepCurrentInput.text()
            )

        except ValueError:

            print("Invalid Inputs")
            return
        #log
        self.log(
        f"Sweep Started | "
        f"Start={self.start_current} mA | "
        f"Stop={self.stop_current} mA | "
        f"Step={self.step_size} mA"
        )
        # Clear old data

        self.current_data.clear()
        self.power_data.clear()
        self.voltage_data.clear()
        self.temperature_data.clear()

        self.li_curve.setData([], [])
        self.vi_curve.setData([], [])

        self.liTable.setRowCount(0)

        self.current_value = self.start_current
        self.tec.enable_output()
        

        # One point every 500 ms

        self.sweepTimer.start(SWEEP_INTERVAL_MS)

    # ====================================
    # STOP SWEEP
    # ====================================

    def stop_sweep(self):

        self.sweepTimer.stop()

        self.tec.disable_output()

        self.log("Sweep Stopped By User")

    # ====================================
    # UPDATE SPECTRUM
    # ====================================

    def update_spectrum(self):

        if not self.avantes.is_connected():
            return

        wavelengths, intensity = self.avantes.get_spectrum()

        self.current_spectrum_wavelengths = wavelengths

        self.current_spectrum_intensities = intensity

        self.spectrum_curve.setData(
            wavelengths,
            intensity
        )

        peak = self.avantes.get_peak_wavelength()

        fwhm = self.avantes.get_fwhm()

        self.peakLabel.setText(
            f"Peak Wavelength : {peak:.2f} nm"
        )

        self.fwhmDisplayLabel.setText(
            f"FWHM : {fwhm:.2f} nm"
        )
    # ====================================
    # TAKE MEASUREMENT
    # ====================================

    def take_measurement(self):

        if self.current_value > self.stop_current:

            self.sweepTimer.stop()

            self.tec.disable_output()

            # --------------------------------
            # Calculate Laser Parameters
            # --------------------------------

            laser = LaserParameters(
                self.current_data,
                self.power_data,
                self.voltage_data
            )

            self.laser_results = laser.calculate()

            results = self.laser_results

            self.update_laser_parameters(self.laser_results)
            print("\n")
            print("=" * 50)
            print("LASER PARAMETERS")
            print("=" * 50)

            for key, value in results.items():

                print(f"{key:25s}: {value}")

            print("=" * 50)

            self.log("Laser Parameters Calculated")

            self.log("Sweep Finished")

            return

        current = self.current_value
        self.sf6100.set_current(
            current
        )
        
        # --------------------------------
        # Read Devices
        # --------------------------------

        current = self.sf6100.read_current()

        voltage = self.sf6100.read_voltage()

        power = self.maestro.read_power()

        temperature = self.tec.read_temperature()
        self.update_spectrum()

        # --------------------------------
        # Store Data
        # --------------------------------

        self.current_data.append(current)
        self.power_data.append(power)
        self.voltage_data.append(voltage)
        self.temperature_data.append(temperature)

        # --------------------------------
        # Update Plot
        # --------------------------------

        self.li_curve.setData(
            self.current_data,
            self.power_data
        )

        self.vi_curve.setData(
            self.current_data,
            self.voltage_data
        )

        # --------------------------------
        # Update Table
        # --------------------------------

        row = self.liTable.rowCount()

        self.liTable.insertRow(row)

        self.liTable.setItem(
            row,
            0,
            QTableWidgetItem(
                f"{current:.2f}"
            )
        )

        self.liTable.setItem(
            row,
            1,
            QTableWidgetItem(
                f"{power:.2f}"
            )   
        )

        self.liTable.setItem(
            row,
            2,
            QTableWidgetItem(
                f"{voltage:.2f}"
            )
        )

        self.liTable.setItem(
            row,
            3,
            QTableWidgetItem(
                f"{temperature:.2f}"
            )
        )

        # --------------------------------
        # Next Current
        # --------------------------------

        self.current_value += self.step_size


# ========================================
# MAIN
# ========================================

app = QApplication(sys.argv)

window = MainWindow()

window.show()

sys.exit(app.exec_())