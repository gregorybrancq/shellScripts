#!/bin/sh

# bug with eclipse and GTK3 in 16.04
#https://bugs.launchpad.net/ubuntu/+source/java-common/+bug/1552764
#export SWT_GTK3=0
# or --launcher.GTK_version 2 to the eclipse.ini file

cd /opt/eclipse/eclipse-4.5.2/
./eclipse

