import sys
import RPi.GPIO as GPIO


if __name__ == "__main__":
    query = sys.argv
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    if query[1] == "lights":
        GPIO.setup([11, 13, 15], GPIO.OUT)
        sys.stdout.write(str(GPIO.input(11))+str(GPIO.input(13))+str(GPIO.input(15)))
    else:
        pass
