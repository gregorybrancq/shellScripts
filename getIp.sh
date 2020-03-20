#!/bin/sh -f

echo '##### @IP Publique #####'
wget http://checkip.dyndns.org/ -O - -o /dev/null | cut -d: -f 2 | cut -d\< -f 1 ; 

echo '##### @IP Privée eth #####'
ifconfig | grep netmask | cut -d i -f 2

