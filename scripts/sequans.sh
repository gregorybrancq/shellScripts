#!/bin/sh -f

if [ -z "$DELL" ]
then
    cd ~/Greg/work/env/vpn/sequans
    more password
    sudo ./connect-France.sh
else
    cd ~/Perso/work/env/vpn/sequans
    more password
    sudo ./connect-France.sh
fi

#set procPid=`ps -C openvpn -o pid=`
#set status=$?
#
#if ($status == "1") then
#    cd ~/Config/OpenVPN/sequans
#    more password
#    sudo ./connect-France.sh
#else
#    sudo kill -9 $procPid
#endif

