from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np;
import RPi.GPIO as GPIO  
  
# Use board based pin numbering  
GPIO.setmode(GPIO.BOARD)

# The LED pins used
leftLED = 18
rightLED = 11

width = 640 #1280
height = 480 #720

# Set threshold and maxValue
thresh = 200
maxValue = 255

def irDetect():

    # Set LED pins to output
    GPIO.setup(leftLED, GPIO.OUT)
    GPIO.setup(rightLED, GPIO.OUT)

    # Set LED pins to off so that they don't blink at startup
    GPIO.output(leftLED, 0)
    GPIO.output(rightLED,0)

    state = 0

    while True:
        # initialize the camera and grab a reference to the raw camera capture
        camera = PiCamera()
        camera.resolution = (width, height)
        camera.framerate = 16
        camera.rotation = 180
        rawCapture = PiRGBArray(camera, size=(width, height))
        
        # allow the camera to warmup 
        time.sleep(0.1)

        # camera.start_preview()

        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            
            image = frame.array
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

            # Basic threshold example
            th, dst = cv2.threshold(gray, thresh, maxValue, cv2.THRESH_BINARY);

            # apply a Gaussian blur to the image then find the brightest
            # region
            # gray = cv2.GaussianBlur(dst, (41, 41), 0)
            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(dst)
            # image = orig.copy()
            if maxLoc != (0,0) and (state == 2 or state == 3):
                
                cv2.circle(image, maxLoc, 41, (255, 0, 0), 2)
                
                if maxLoc > (0,0) and maxLoc < (250,480):
                    # if IR LED is on the left side of the camera image,
                    # turn on left LED
                    # print "LED on Left"
                    GPIO.output(leftLED, 1)
                    GPIO.output(rightLED, 0)
                elif maxLoc >= (250,0) and maxLoc <= (390,480):
                    # if IR LED is in the center of the camera image,
                    # turn on both LEDs
                    # print "LED in Center"
                    GPIO.output(leftLED, 1)
                    GPIO.output(rightLED, 1)
                elif maxLoc > (390,0) and maxLoc <= (640,480):
                    # if IR LED is on the right side of the camera image,
                    # turn on right LED
                    # print "LED on Right"
                    GPIO.output(leftLED, 0)
                    GPIO.output(rightLED, 1)
            elif state == 2 and maxLoc == (0, 0):
                state = 3  
            elif state == 1 and maxLoc == (0, 0):
                state = 2    
            elif maxLoc == (0, 0) and state == 0:
                state = 1
            else:
                state = 0
                GPIO.output(leftLED, 0)
                GPIO.output(rightLED, 0)
            
            # display the results of our newly improved method
            cv2.imshow("IR LED Detection", image)
            
            key = cv2.waitKey(1) & 0xFF
     
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)
     
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                    GPIO.cleanup()
                    break
        camera.close()
        break

if __name__ == '__main__':
    irDetect()
