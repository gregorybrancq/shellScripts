#!/bin/sh
openvpn --up update-resolv-conf --down update-resolv-conf --config France.ovpn --script-security 3
