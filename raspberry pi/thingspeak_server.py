import core_communication as talk
import RPi.GPIO as GPIO
import time


def output_states(*pins):
    """
    Outputs the states of the pins.
    """
    result = ""
    for pin in pins:
        result += str(GPIO.input(pin))
    return result


def react(command):
    """
    Acts according to command.
    """
    if command == "red":
        val = not GPIO.input(RED)
        GPIO.output(RED, int(val))
    elif command == "yellow":
        val = not GPIO.input(YELLOW)
        GPIO.output(YELLOW, int(val))
    elif command == "green":
        val = not GPIO.input(GREEN)
        GPIO.output(GREEN, int(val))
    elif command == "all on":
        GPIO.output(RED,1)
        GPIO.output(YELLOW,1)
        GPIO.output(GREEN,1)
    elif command == "all off":
        GPIO.output(RED,0)
        GPIO.output(YELLOW,0)
        GPIO.output(GREEN,0)
    elif command == "flash":
        for i in range(10):
            react("red")
            react("green")
            react("yellow")
            time.sleep(1)
    else:
        pass
        
 
RED = 11
YELLOW = 13
GREEN = 15
command_downloader = talk.WebServerCommunication()
states_uploader = talk.WebServerCommunication(3875, "7IW3BGP1IT0FOGYQ")

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup([RED, GREEN, YELLOW], GPIO.OUT)
    while True:
        if len(command_downloader.command("list_all")) > 0:
            react(command_downloader.command("get"))
            print states_uploader.command("put", output_states(RED, YELLOW, GREEN))
