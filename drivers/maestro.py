import serial


class Maestro:

    def __init__(
        self,
        port,
        baudrate=115200,
        timeout=1
    ):

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        self.ser = None

        self.device_name = "Maestro"
        self.firmware = "Unknown"

    # ==================================================
    # Connection
    # ==================================================

    def connect(self):

        self.ser = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=self.timeout
        )

        return self.is_connected()

    def disconnect(self):

        if self.ser and self.ser.is_open:
            self.ser.close()

    def is_connected(self):

        return (
            self.ser is not None
            and self.ser.is_open
        )

    # ==================================================
    # Low-Level Communication
    # ==================================================

    def send_command(self, command):

        if not self.is_connected():
            raise ConnectionError(
                "Maestro is not connected."
            )

        full_command = "*" + command + "\r"

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        self.ser.write(full_command.encode())

        response = self.ser.readline()

        if not response:
            raise TimeoutError(
                f"No response for command: {command}"
            )

        return response.decode().strip()

    # ==================================================
    # Device Information
    # ==================================================

    def ping(self):

        return self.send_command("KPA")

    def identify(self):

        self.firmware = self.send_command("VER")

        return self.firmware

    def get_status(self):

        return self.send_command("STS")

    # ==================================================
    # Measurements
    # ==================================================

    def read_power(self):

        response = self.send_command("CVU")

        try:

            return float(response)

        except ValueError:

            raise ValueError(
                f"Invalid power reading: {response}"
            )

    # ==================================================
    # Settings
    # ==================================================

    def set_wavelength(self, wavelength_nm):

        wavelength = int(wavelength_nm)

        command = f"PWC{wavelength:05d}"

        return self.send_command(command)

    # ==================================================
    # Generic Measurement
    # ==================================================

    def get_measurement(self):

        return {

            "power": self.read_power()

        }