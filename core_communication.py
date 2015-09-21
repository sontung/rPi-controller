"""
This is the code for communicating with the Pipi through bluetooth. It uses PySerial
as a main way to setup a serial connection between this app and the Pipi (or the bluetooth
module). To connect successfully, one must find his/her correct port for outgoing bluetooth.
"""
import serial


class Communication:
    def __init__(self):
        self.serial_port = None # Bluetooth serial port

    def specify_port(self, port):
        """
        Specify the COM bluetooth port.
        :param port:
        :return:
        """
        self.serial_port = port

    def connect(self):
        """
        Connect to the specified port.
        :return:
        """
        self.connection = serial.Serial(self.serial_port)

    def disconnect(self):
        """
        Disconnect the port.
        :return:
        """
        self.connection.close()

    def command(self, val):
        """
        Send command to bluetooth module.
        :param val:
        :return:
        """
        self.connection.write(val)