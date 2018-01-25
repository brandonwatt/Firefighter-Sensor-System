import time
import RPi.GPIO as GPIO  

# Use board based pin numbering  
def beacon():
    GPIO.setmode(GPIO.BOARD)

    GPIO.setwarnings(False)

    IRled = 11
    counter = 0
    GPIO.setup(IRled, GPIO.OUT)

    GPIO.output(IRled, 1)

    p = GPIO.PWM(IRled, 2)

    p.start(50)

    while True:
        try:
            offtime = 0

        except KeyboardInterrupt:
            
            GPIO.cleanup()
            
            break
    p.stop()
    GPIO.cleanup()

if __name__ == '__main__':
    beacon()

