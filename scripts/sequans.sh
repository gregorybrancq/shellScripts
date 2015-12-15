#!/bin/sh -f

cd ~/Greg/work/config/vpn/sequans
more password
sudo ./connect-France.sh

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

