#!/bin/sh -f

# command to launch to open terminal with good configuration
#env SEQUANS_VPN=1 roxterm --hide-menubar --geometry=100x30+350+280 --title='OPEN VPN Sequans' -e sequans


cd ~/Greg/work/config/vpn/sequans
#more password
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

