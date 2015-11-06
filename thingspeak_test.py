import core_communication
import sys


if __name__ == "__main__":
    thingspeak = core_communication.WebServerCommunication(3875, "7IW3BGP1IT0FOGYQ")
    while True:
        _string = sys.stdin.readline()[:-1]
        try:
            command_string, optional = _string.split(" ")
        except ValueError:
            command_string = _string
            optional = ""
        print thingspeak.command(command_string, optional)
