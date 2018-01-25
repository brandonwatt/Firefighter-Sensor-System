import serial
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

HazardLed = 13

GPIO.setup(HazardLed, GPIO.OUT)

# GPIO.output(HazardLed, 0)

p = GPIO.PWM(HazardLed, 1)

p.start(0)

ser = serial.Serial ("/dev/ttyUSB0")        #Open named port 
ser.baudrate = 9600                         #Set baud rate to 9600
## ser.timeout = 1
##
##while True:
##    try:
##        command = ser.readline()
##        print str(command)
##    except KeyboardInterrupt:
##        break
##        
##ser.close()

ser.isOpen()

print 'Enter your commands below.\nInsert "exit" to leave the application.'

input=1
while 1 :
    # get keyboard input
    input = raw_input(">> ")
        # Python 3 users
        # input = input(">> ")
    if input == 'exit':
        ser.close()
        p.stop()
        GPIO.cleanup()
        exit()
    else:
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        ser.write(input + '\r\n')
        out = ''
        SN = ''
        Conc = ''
        ConcFloat = 10.0
        Temp = ''
        Humid = ''
        rest = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read(1)

        if out != '':
            SN, Conc, Temp, Humid, rest = out.split(",", 4)
            # ConcFloat = float(Conc) / 1000.0
            print ">> Concentration (PPB): " + Conc
            print ">> Concentration (PPM): " + str(ConcFloat)
            print ">> Tempurature (C); " + Temp
            print ">> Humidity: " + Humid

            if ConcFloat >= 5.0:
                p.ChangeFrequency(ConcFloat / 5.0)
                p.ChangeDutyCycle(25)
                print ">> Potentially Hazardous Conc. of Resp. Irritant(s) Detected!" 
            else:
                p.ChangeDutyCycle(0)
        if input == 'exit':
            ser.close()
            p.stop()
            GPIO.cleanup()
            exit()
