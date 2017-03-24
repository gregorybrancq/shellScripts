#!/bin/bash -f

# Program to backup Android phone directory

# Detect phone
# Mount phone
# Sync directories
# Umount phone

progName=$(basename "$0")

# Phone
nexus4Name="Nexus4"
nexus4Mtp="Nexus 4/5/7/10 (.*), Google Inc (for LG Electronics/Samsung)"
nexus4Mount="/media/nexus4"
nexus4Sdcard="Espace de stockage interne partagé/"
nexus4Backup="$HOME/Greg/Informatique/Nexus4/Backup"

idol3Name="Idol3"
idol3Mtp="OneTouch Idol 3 small (MTP)"
idol3Mount="/media/idol3"
idol3Backup="$HOME/Greg/Informatique/Idol3/Backup"

# Global variables
androidName=""
mountDir=""
srcDir=""
backupDir=""
res=""

# lock
lockDir="/var/lock"
lockFile=$lockDir/$progName.lock
lockFd=200


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

    eexit "No Android detected.\nCheck if MTP mode is well activated."
}


# Synchronisation
sync() {
    echo "Sync src=$srcDir dest=$backupDir"
    res=`rsync -ra --progress --stats "$srcDir" "$backupDir"`
}


# Mount android phone
mount() {
    echo "Mount function"

    ps aux | grep gvfsd-mtp | grep -v "grep"
    if [ $? -eq 0 ]; then
        echo "Kill automatic mtp mount point"
        pkill -9 gvfsd-mtp
    fi

    # Check if the mount point is not already mounted
    ls $mountDir
    if [ -d "$srcDir" ]; then
        umount
    fi

    echo "Mount to $mountDir"
    jmtpfs $mountDir

    # Check if no error during mount
    sleep 1
    ls $mountDir | grep "error"
    if [ $? -ne 1 ]; then
        umount
        eexit "Android mount error ($mountDir).\nCheck if MTP mode is well activated."
    fi

}


# Umount android phone
umount() {
    echo "Umount $mountDir"
    sleep 1
    fusermount -u $mountDir
}


lock() {
    local fd=${2:-$lockFd}

    # create lock file
    eval "exec $fd>$lockFile"

    # acquire the lock
    flock -n $fd \
        && return 0 \
        || return 1
}


eexit() {
    local error_str="$@"

    rm -f $lockFile
    echo $error_str
    zenity --info --text="$error_str"
    exit 1
}


#
# Main script
#

main() {
    exec 200>$lockFile
    lock $progName \
        || eexit "Only one instance of $progName can run at one time."
    
    detect
    if [ $? -eq 1 ]; then
        
        mount
        sync
        umount
    
        if [ "$res" != "" ]; then
            zenity --info --text="Congratulations !!!\n\nBackup directory = $backupDir.\n\n$res"
        fi
    
    fi

    rm -f $lockFile
}

main

