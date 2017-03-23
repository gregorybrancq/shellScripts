#!/bin/sh -f

# Program to backup Android phone directory

# Detect phone
# Mount phone
# Sync directories
# Umount phone

# Phone
nexus4Name="Nexus4"
nexus4Mtp="Nexus 4/5/7/10 (MTP), Google Inc (for LG Electronics/Samsung)"
nexus4Mount="/media/nexus4"
nexus4Sdcard="Espace de stockage interne partagé/"
nexus4Backup="/home/greg/Greg/Informatique/Nexus4/Backup"

idol3Name="Idol3"
idol3Mtp=""
idol3Mount="/media/idol3"
idol3Backup="/home/greg/Greg/Informatique/Idol3/Backup"

# Global variables
androidName=""
mountDir=""
srcDir=""
backupDir=""



# 
# Functions
#

# Detect the different Android phone
# return 1 for Nexus4/Idol3
# return 0 if none
detect() {
    echo "Detect function"
    jmtpfs -l | grep "$nexus4Mtp"
    if [ $? -eq 0 ]; then
        androidName=$nexus4Name
        mountDir=$nexus4Mount
        srcDir=$nexus4Mount/$nexus4Sdcard
        backupDir=$nexus4Backup
        echo "$androidName detected"
        return 1
    fi

    jmtpfs -l | grep "$idol3Mtp"
    if [ $? -eq 0 ]; then
        androidName=$idol3Name
        mountDir=$idol3Mount
        backupDir=$idol3Backup
        echo "$androidName detected"
        return 1
    fi

    echo "no Android detected"
    return 0
}

sync() {
    echo "Sync src=$srcDir dest=$backupDir"
    rsync -ra --stats "$srcDir" "$backupDir"
}


mount() {
    echo "Mount function"

    echo "Kill automatic mtp mount point"
    ps aux | grep gvfsd-mtp | grep -v "grep"
    pkill -9 gvfsd-mtp

    echo "Mount to $mountDir"
    jmtpfs $mountDir
    
}

umount() {
    echo "Umount $mountDir"
    fusermount -u $mountDir
}


#
# Main script
#

detect
varDetect=$?

if [ $varDetect -eq 1 ]; then

    mount
    sync
    umount

fi

