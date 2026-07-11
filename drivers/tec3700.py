import serial


class TEC3700:

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

        self.device_name = "Newport TEC3700"
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
    # Low Level Communication
    # ==================================================

    def send_command(self, command):

        if not self.is_connected():
            raise ConnectionError(
                "TEC3700 is not connected."
            )

        full_command = command + "\r"

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        self.ser.write(
            full_command.encode()
        )

        response = self.ser.readline()

        if not response:

            raise TimeoutError(
                f"No response for command: {command}"
            )

        return response.decode().strip()

    # ==================================================
    # Standard SCPI Commands
    # ==================================================

    def identify(self):

        self.firmware = self.send_command(
            "*IDN?"
        )

        return self.firmware

    def reset(self):

        return self.send_command(
            "*RST"
        )

    def save_settings(self):

        return self.send_command(
            "*SAV"
        )

    def recall_settings(self):

        return self.send_command(
            "*RCL"
        )

    def status_byte(self):

        return self.send_command(
            "*STB?"
        )

    # ==================================================
    # Output Control
    # ==================================================

    def enable_output(self):

        return self.send_command(
            "TEC:Output 1"
        )

    def disable_output(self):

        return self.send_command(
            "TEC:Output 0"
        )

    def output_enabled(self):

        response = self.send_command(
            "TEC:Output?"
        )

        return response == "1"

    # ==================================================
    # Mode
    # ==================================================

    def set_temperature_mode(self):

        return self.send_command(
            "TEC:MODE:T"
        )

    def set_current_mode(self):

        return self.send_command(
            "TEC:MODE:Ite"
        )

    def set_resistance_mode(self):

        return self.send_command(
            "TEC:MODE:R"
        )

    def get_mode(self):

        return self.send_command(
            "TEC:MODE?"
        )

    # ==================================================
    # Temperature
    # ==================================================

    def set_temperature(
        self,
        temperature_c
    ):

        return self.send_command(
            f"TEC:T {temperature_c:.3f}"
        )

    def read_temperature(self):

        response = self.send_command(
            "TEC:T?"
        )

        return float(response)

    def read_setpoint(self):

        response = self.send_command(
            "TEC:SET:T?"
        )

        return float(response)

    # ==================================================
    # Current
    # ==================================================

    def set_current(
        self,
        current_amp
    ):

        return self.send_command(
            f"TEC:Ite {current_amp:.3f}"
        )

    def read_current(self):

        response = self.send_command(
            "TEC:Ite?"
        )

        return float(response)

    def read_current_setpoint(self):

        response = self.send_command(
            "TEC:SET:Ite?"
        )

        return float(response)

    # ==================================================
    # Voltage
    # ==================================================

    def read_voltage(self):

        response = self.send_command(
            "TEC:Vte?"
        )

        return float(response)

    # ==================================================
    # Status
    # ==================================================

    def get_status(self):

        return self.send_command(
            "TEC:COND?"
        )

    # ==================================================
    # Limits
    # ==================================================

    def set_current_limit(
        self,
        current_amp
    ):

        return self.send_command(
            f"TEC:LIM:Ite {current_amp:.3f}"
        )

    def read_current_limit(self):

        response = self.send_command(
            "TEC:LIM:Ite?"
        )

        return float(response)

    def set_voltage_limit(
        self,
        voltage
    ):

        return self.send_command(
            f"TEC:LIM:Vte {voltage:.3f}"
        )

    def read_voltage_limit(self):

        response = self.send_command(
            "TEC:LIM:Vte?"
        )

        return float(response)

    def set_high_temperature_limit(
        self,
        temperature
    ):

        return self.send_command(
            f"TEC:LIM:THI {temperature:.3f}"
        )

    def read_high_temperature_limit(self):

        response = self.send_command(
            "TEC:LIM:THI?"
        )

        return float(response)

    def set_low_temperature_limit(
        self,
        temperature
    ):

        return self.send_command(
            f"TEC:LIM:TLO {temperature:.3f}"
        )

    def read_low_temperature_limit(self):

        response = self.send_command(
            "TEC:LIM:TLO?"
        )

        return float(response)

    # ==================================================
    # Miscellaneous
    # ==================================================

    def beep(self):

        return self.send_command(
            "BEEP"
        )

    def local(self):

        return self.send_command(
            "LOCAL"
        )

    # ==================================================
    # Generic Measurement
    # ==================================================

    def get_measurement(self):

        return {

            "temperature": self.read_temperature(),

            "setpoint": self.read_setpoint(),

            "current": self.read_current(),

            "voltage": self.read_voltage()

        }