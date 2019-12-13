#!/bin/sh -f

echo ; date | cut -f 2 ; echo '##### @IP Publique #####' ; wget http://checkip.dyndns.org/ -O - -o /dev/null | cut -d: -f 2 | cut -d\< -f 1 ; echo '##### @IP Privée eth #####' ; ifconfig | grep Masque | cut -d i -f 2

sleep 100
