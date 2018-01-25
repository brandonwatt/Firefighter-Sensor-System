# Brandon Watt, Vlad Pserav, Brian Hess
# TCES 482 Senior Project III
# Node Process
# Runs all processes necessary for a node in the
# ad-hoc network.


import jsonTransfer27
import IRBeacon
from multiprocessing import *

if __name__ == '__main__':
    
    relaySend, serverRecv = Pipe()
    msgSend, msgRecv = Pipe()
    
    relayProcess = Process(target=jsonTransfer27.relay, args=(serverRecv, msgRecv,))
    servProcess = Process(target=jsonTransfer27.server, args=(relaySend,))
    msgProcess = Process(target=jsonTransfer27.generateMsg, args=(msgSend,))
    beaconProcess = Process(target=IRBeacon.beacon)


    servProcess.start()
    relayProcess.start()
    msgProcess.start()
    beaconProcess.start()

    
    servProcess.join()
    relayProcess.join()
    msgProcess.join()
    beaconProcess.join()
