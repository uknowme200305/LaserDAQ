import serial


class SF6100:

    def __init__(self, port):

        self.port = port
        self.ser = None

    def connect(self):

        try:

            self.ser = serial.Serial(
                port=self.port,
                baudrate=115200,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1
            )

            return True

        except Exception as e:

            print(f"Connection Failed: {e}")

            return False

    def disconnect(self):

        if self.ser and self.ser.is_open:
            self.ser.close()

    def send_raw(self, command):

        if not self.is_connected():
            raise ConnectionError(
                "SF6100 not connected"
            )

        command += "\r"

        self.ser.write(command.encode())

        response = self.ser.readline()

        if not response:
            raise TimeoutError(
                "SF6100 did not respond"
            )

        return response.decode().strip()
        
    def get_parameter(self, parameter):

        command = f"J{parameter}"

        return self.send_raw(command)
    
        # ==================================================
        # Device Identification
        # ==================================================

        def identify(self):
            """
            Returns the Device Model / Version ID.
            Used by the hardware scanner.
            """
            return self.get_parameter("0702")

        def get_serial_number(self):
            """
            Returns the device serial number.
            """
            return self.get_parameter("0701")


    def set_parameter(self, parameter, value):

        command = f"P{parameter} {value}"

        return self.send_raw(command)
    
    def enable(self):

        return self.set_parameter(
            "0700",
            "0008"
        )


    def disable(self):

        return self.set_parameter(
            "0700",
            "0010"
        )
    
    def set_current(self, current_amp):

        value = int(
            current_amp / 0.01
        )

        hex_value = f"{value:04X}"

        return self.set_parameter(
            "0300",
            hex_value
        )
    
    def read_current(self):

        response = self.get_parameter(
            "0307"
        )

        return response
    
    def read_voltage(self):

        response = self.get_parameter(
            "0407"
        )

        return response
    
    def is_connected(self):

        return (
            self.ser is not None
            and self.ser.is_open
        )