#!/usr/bin/env python

# Written by Gregory Brancq
# June 2018
# Public domain software

"""
Program to check which unison configuration using and launch the synchronisation
"""
    

import os
import subprocess
import socket

addressCorres = dict()
addressCorres["192.168.0.1"] = "portable_room"
addressCorres["10.42.0.1"]   = "portable"
addressCorres["192.168.0.2"] = "home"
addressCorres["10.42.0.146"] = "home_desk"

addressConfig = dict()
addressConfig["home"] = "room_server_sata"
addressConfig["home_desk"] = "dockstation_server_sata"
addressConfig["portable"] = "server_dockstation_sata"
addressConfig["portable_room"] = "server_room_sata"


def getIp():
    #print([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def checkAddress(ad):
    """Check if address pings"""
    print("Check address "+ad)
    runCmd="ping -w 1 "+str(ad)
    procPopen = subprocess.Popen(runCmd, shell=True)
    procPopen.wait()
    if (procPopen.returncode == 0) :
        return True
    return False


def runSync(cfg):
    print("Run sync "+cfg)
    unisonCfgFile=os.path.join(os.getenv("HOME"), ".unison", cfg+".prf")
    if os.path.isfile(unisonCfgFile) :
        runCmd="unison-gtk "+str(cfg)
        procPopen = subprocess.Popen(runCmd, shell=True)
        procPopen.wait()
    else :
        print("Your config "+unisonCfgFile+" doesn't exist")




def main():
    myIp=getIp()
    print "My IP="+str(myIp)
    remoteIp=addressCorres[myIp]
    print "My remote ip="+str(remoteIp)
    if checkAddress(remoteIp) :
        cfg=addressConfig[remoteIp]
        print "My config="+str(cfg)
        runSync(cfg)



if __name__ == '__main__':
    main()
