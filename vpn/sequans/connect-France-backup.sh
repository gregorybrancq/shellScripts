#!/bin/sh
openvpn --up update-resolv-conf --down update-resolv-conf --config France-backup.ovpn --script-security 3
