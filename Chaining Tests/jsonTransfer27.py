# Brandon Watt, Vlad Psarev, and Brian Hess
# 4/20/17
# TCES 482 Senior Project III
# File Transfer Client
# A basic client based program meant to send information in JSON format over
# an ad-hoc network to a server based program, which will read that information.

import socket
import json
import RPi.GPIO as GPIO
import time

import subprocess
import IAQSensorSerial

#from MPU9250 import *
import farts_mpu9250_driver
from multiprocessing import *


SELFHOST = '192.168.42.3'
ID = 'Firefighter 3'


# The IP address of the device that is the final destination of the message.
# This IP should be the IP of the command device.
DEST = '192.168.42.1'

# A list of IPs of devices that this device will attempt to connect to.
HOSTS = {'192.168.42.1', '192.168.42.2', '192.168.42.3', '192.168.42.4', '192.168.42.5'}
# A dictionary holding the list of device IPs along with whether or not the can be connected too.
CONN = {'192.168.42.1':False, '192.168.42.2':False, '192.168.42.3':False, '192.168.42.4':False, '192.168.42.5':False}
# The port used for making the connection.
PORT = 50007

# The number of seconds the device will wait to generate a new message.
WAIT = 2

# The IP address used by the client function, not used in current program.
HOST = '192.168.42.1'

GPIO.setmode(GPIO.BOARD)

HazardLed = 13

GPIO.setwarnings(False)
GPIO.setup(HazardLed, GPIO.OUT)


mpu9250 = farts_mpu9250_driver.MPU9250()

socket.setdefaulttimeout(2)

# Relay messages recieved from other devices along the network or, send
# out a message from this device.
def relay(servPipe, msgPipe):
    
    # If there is a message to send or not.
    toSend = False

    # The number of messages from other devices this device has relayed.
    count = 0
    
    while True:
        try:
            # Relay a message recieved from another device.
            # The device will prioritizes relaying messages over sending it's own out.
            if servPipe.poll() and count < len(HOSTS):
                msg = servPipe.recv()
                toSend = True

                # Incriment the number of messages relayed.
                count += 1

                # Remove a self generated message from the pipe.
                if msgPipe.poll():
                    msgPipe.recv()

            # If there are no messages to relay or (count) messages have been
            # relayed, send a message from this device.
            elif msgPipe.poll():
                msg = msgPipe.recv()
                toSend = True
                count = 0

            # If there is nothing to send.
            else:
                toSend = False

            # If there is a message to send and it is not blank.
            if toSend and not msg == '':
                
                print('In relay: {0}'.format(msg))
                
                msgList = msg.split(';')
                #print('In relay, msgList: ', msgList)
                #timestamp = msgList[0]
                primDest = msgList[1]
                #print(primDest)
                #IPid = msgList[2]
                #id = msgList[3]
                #data = msgList[4]
                recieved = msgList[5]


                # Attempt to send the message to the desired destination.
                # If the destination can be reached, send the message to it
                # and don't send the message anywhere else.
                try:
                    d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # Attempt connection with host.
                    d.connect((DEST, PORT))

                    # Connection was successful, record it and add it too
                    # the list of devices recieving the message.
                    CONN[primDest] = True
                    
                    msg += ',' + DEST

                    d.sendall(msg)
                    d.shutdown(socket.SHUT_RDWR)
                    d.close()
                    print('Message sent to destination')

                # If the desired destination cannot be reached, send the message to all other
                # devices that can be reached in the hopes that they can send it to the destination.
                except socket.error:
                    print("Could not get message to it's desired destination")
                    
                    CONN[DEST] = False

                    
                    recvList = recieved.split(',')
                    print('In relay, recieved list: {0}'.format(recvList))
                    
                    # Go through the list of possible connected decives.
                    for host in HOSTS:
                        # If that the device hasn't recived the message.
                        if not host in recvList and not host == DEST: 
                            try:
                                c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                # Attempt connection with host.
                                c.connect((host, PORT))

                                # Connection was successful, record it and add it too
                                # the list of devices recieving the message.
                                CONN[host] = True
                                c.shutdown(socket.SHUT_RDWR)
                                msg += ',' + host
                                c.close()
                                    
                            except socket.error:
                                print('Failed connecting to {0}'.format(host))
                                CONN[host] = False
                            
                    # Send the message to all the devices you can connect to.
                    for host in HOSTS:
                        if CONN[host]:
                            try:
                                c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                c.connect((host, PORT))
                                c.sendall(msg)
                                c.shutdown(socket.SHUT_RDWR)
                                c.close()
                            except socket.error:
                                print('Reconnecting to {0} failed, removing from connections.'.format(host))
                                CONN[host] = False

                                div = msg.split(host)
                                msg = div[0] + div[1]
                                print(msg)

                            
        except KeyboardInterrupt:
            break

    c.shutdown(socket.SHUT_RDWR)
    c.close()


# A basic client socket meant to send messages to other devices.
# Not used in the current main program.
def client(recvPipe):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #h = socket.gethostbyname('raspberrypi')
    #i = socket.gethostbyaddr(HOST)

    #print(h)
    
    connection = False

    while not connection:
        try:
            c.connect((HOST, PORT))
            c.sendall('message')
            connection = True
        except socket.error:
            print('Failed, trying again')
            time.sleep(0.5)


    while True:
        try:
            msg = recvPipe.recv()

            print(msg)
        
            #jmsg = json.loads(msg)

            c.sendall(msg)

        except socket.error:
            print('Socket error, closing down.')
            break

    c.shutdown(socket.SHUT_RDWR)

# Generates a message to be sent out to other devices.
# The message contains a timestamp of when the data was taken, the final destination of
# the message, the IP address of the device that sent it, the name of the device that sent it,
# the data the device collected, and a list of IPs of the devices that have recieved the message.
def generateMsg(sendPipe):

    lastMsg = time.time()

    p = GPIO.PWM(HazardLed, 1)

    p.start(0)

    mod = True    
    while True:
        try:
            # Only send a message once per second.
            if time.time() - lastMsg >= WAIT:
                # Build the message

                timeStamp = str(time.ctime())
                
                msg = timeStamp + ';' + DEST + ';' + SELFHOST + ';' + ID + ';'

                # Add the data to the message
                #accelX = mpu9250.readAccelX()['xAccel']
                #accelY = mpu9250.readAccelY()['yAccel']
                #accelZ = mpu9250.readAccelZ()['zAccel']
                
                #accelDict = {'x':accel['x'], 'y':accel['y'], 'z':accel['z']}
            
                #accel = {'x':1.06, 'y':0.00, 'z':2.3}

                #con, temp, humid = IAQSensorSerial.sensorRead()

                #if mod:
                #    con += 5000
                
                #accel = 'x:{0}, y:{1}, z:{2}, '.format(accelX, accelY, accelZ)
                #air = 'ConPPB:{0}, Temp:{1}, Humid:{2}'.format(con, temp, humid)
                #data = accel + air + ';'
                data = 'Data;'
                
                #ConcFloat = float(con) / 1000.0
                #if ConcFloat >= 5.0:
                #    p.ChangeFrequency(ConcFloat / 5.0)
                #    p.ChangeDutyCycle(25)
                #    print(">> Potentially Hazardous Conc. of Resp. Irritant(s) Detected!") 
                #else:
                #    p.ChangeDutyCycle(0)
                
                msg += data

                # Start the list of devices that have recieved the message
                msg += SELFHOST

                #print('In generate: ',  msg)
                
                sendPipe.send(msg)
                
                lastMsg = time.time()

                mod = not mod
        except KeyboardInterrupt:
            IAQSensorSerial.sensorRead('exit')
            p.stop()
            break

# Waits for sockets to connect to the deivce,
# then collects the message from that socket and sends it too
# the relay system.
def server(sendPipe):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 50007))
    s.listen(5)

    out = file('multiPiPassing3.txt', 'a')
    out.write(str(time.ctime())+'\n')
    
    while True:
        try:
            conn, addr = s.accept()
            print('Connected with {0}'.format(addr))
            
            data = conn.recv(1024)

            msg = str(data)
            
            #jmsg = json.dumps(data)
            out.write(msg +'\n')
            print(msg)

            # Don't send a message to the relay function if the message is empty.
            if not msg == '':
                sendPipe.send(msg)

            conn.shutdown(socket.SHUT_RDWR)
            #conn.close()        
            #airQuality = json.loads(data)

            #print(airQuality)

            #conn.shutdown(socket.SHUT_RD)
        except socket.error as err:
            print('Server Connection Failed: {0}'.format(err))
            
        except KeyboardInterrupt:
            break;

    print('Server closed')
    s.shutdown(socket.SHUT_RDWR)
    s.close()

def commandServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 50007))
    s.listen(5)

    out = file('multiPiPassing3.txt', 'a')
    out.write(str(time.ctime())+'\n')
    out.write('Running as command: \n')


    msgQueue = Queue()


    msgWriter = Process(target=reporterProcess, args=(out, msgQueue, ))
    msgWriter.start()
    msgWriter.join()

    while True:
        try:
            conn, addr = s.accept()            

            msgHandler = Process(target=commandProcess, args=(conn, msgQueue, ))
            msgHandler.start()
            msgHandler.join()
            
        
        except KeyboardInterrupt:
            break;

    print('Server closed')
    s.shutdown(socket.SHUT_RDWR)
    s.close()


def commandProcess(conn, msgQueue):

    data = conn.recv(1024)

    msg = str(data)

    msgQueue.put(msg)

    conn.shutdown(socket.SHUT_RDWR)


def reporterProcess(fout, msgQueue):

    while True:

        if not msgQueue.empty():
            msg = msgQueue.get()
            fout.write(msg + '\n')
            print(msg)

if __name__ == '__main__':

    #output = subprocess.check_output("sudo iwlist wlan0 scan essid RPi | egrep -o level=?-[0-9]*[[:space:]]", shell=True)
    #print(output)

    #p1 = subprocess.Popen(["sudo", "iwlist", "wlan0", "scan", "essid", "RPi"], stdout=subprocess.PIPE) #stdout=subprocess.PIPE 
    #p2 = subprocess.Popen(["egrep", "-o", "level=?-[0-9]*[[:space:]]"], stdin=p1.stdout, stdout=subprocess.PIPE) #stdout=subprocess.PIPE
    #p1.stdout.close()
    #output = p2.communicate()
    #out = p1.communicate()
    #print(output)
    
    relaySend, serverRecv = Pipe()
    msgSend, msgRecv = Pipe()
    
    relayProcess = Process(target=relay, args=(serverRecv, msgRecv,))
    servProcess = Process(target=server, args=(relaySend,))
    msgProcess = Process(target=generateMsg, args=(msgSend,))

    servProcess.start()
    relayProcess.start()
    msgProcess.start()

    servProcess.join()
    relayProcess.join()
    msgProcess.join()
