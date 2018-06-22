#!/usr/bin/env python

# Written by Gregory Brancq
# June 2018
# Public domain software

import os
import subprocess


"""
Program to check which unison configuration using and launch the synchronisation
"""
    
addressConfig = dict()
addressConfig["home"] = "room_server_sata"
addressConfig["home_desk"] = "dockstation_server_sata"
addressConfig["home_vpn"] = "office_server_sata"
addressConfig["portable"] = "server_dockstation_sata"
addressConfig["portable_room"] = "server_room_sata"



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
    adCfgKeys = addressConfig.keys()
    for adCfgKey in ["home", "home_desk", "portable_room", "portable", "home_vpn"] :
        if checkAddress(adCfgKey) :
            runSync(addressConfig[adCfgKey])
            break



if __name__ == '__main__':
    main()
