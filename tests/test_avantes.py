import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from simulators.avantes_sim import (
    AvantesSimulator
)
from simulators.sf6100_sim import SF6100Simulator
from simulators.tec3700_sim import TEC3700Simulator
from simulators.avantes_sim import AvantesSimulator

laser = SF6100Simulator()
laser.connect()
laser.enable()

tec = TEC3700Simulator(laser)
tec.connect()

spectrometer = AvantesSimulator(laser, tec)
spectrometer.connect()

laser.set_current(80)

def main():

    print("=" * 60)
    print("AVANTES SPECTROMETER SIMULATOR TEST")
    print("=" * 60)

    # -------------------------------------------------
    # Create Simulator
    # -------------------------------------------------

    spectrometer = AvantesSimulator()

    # -------------------------------------------------
    # Connect
    # -------------------------------------------------

    print("\nConnecting...")

    spectrometer.connect()

    print(
        "Connected:",
        spectrometer.is_connected()
    )

    # -------------------------------------------------
    # Integration Time
    # -------------------------------------------------

    spectrometer.set_integration_time(20)

    print(
        "Integration Time:",
        spectrometer.get_integration_time(),
        "ms"
    )

    # -------------------------------------------------
    # Acquire Spectrum
    # -------------------------------------------------

    wavelengths, intensities = spectrometer.get_spectrum()

    print("\nSpectrum Acquired")

    print(
        "Number of Pixels:",
        len(wavelengths)
    )

    print(
        "Wavelength Range:",
        f"{wavelengths[0]:.2f} nm",
        "to",
        f"{wavelengths[-1]:.2f} nm"
    )

    print(
        "Maximum Counts:",
        round(max(intensities), 2)
    )

    # -------------------------------------------------
    # Peak Analysis
    # -------------------------------------------------

    peak = spectrometer.get_peak_wavelength()

    fwhm = spectrometer.get_fwhm()

    print(
        "\nPeak Wavelength:",
        peak,
        "nm"
    )

    print(
        "FWHM:",
        fwhm,
        "nm"
    )

    # -------------------------------------------------
    # Print Sample Data
    # -------------------------------------------------

    print("\nFirst 10 Data Points")

    print("-" * 60)

    print(
        " Wavelength (nm)    Intensity"
    )

    print("-" * 60)

    for i in range(10):

        print(
            f"{wavelengths[i]:10.3f}"
            f"        "
            f"{intensities[i]:10.2f}"
        )

    # -------------------------------------------------
    # Plot Spectrum
    # -------------------------------------------------

    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 5))

    plt.plot(
        wavelengths,
        intensities,
        linewidth=1.5
    )

    plt.title("Simulated Avantes Spectrum")

    plt.xlabel("Wavelength (nm)")

    plt.ylabel("Intensity (Counts)")

    plt.grid(True)

    plt.tight_layout()

    plt.show()
    # -------------------------------------------------
    # Disconnect
    # -------------------------------------------------

    spectrometer.disconnect()

    print("\nDisconnected")

    print(
        "Connected:",
        spectrometer.is_connected()
    )

    print("\nTest Completed Successfully")

    print("=" * 60)


if __name__ == "__main__":

    main()