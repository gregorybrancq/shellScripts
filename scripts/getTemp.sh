#!/bin/sh -f

echo "\n Date : " `date`
#sudo smartctl -A /dev/sda | grep Temperature_Celsius
echo "\nTemperature du 1er disque"
sudo hddtemp /dev/sda

echo "\nTemperature du 2eme disque"
sudo hddtemp /dev/sdb
echo "\nTemperature du 3eme disque"
sudo hddtemp /dev/sdc
echo "\nTemperature du CPU"
sudo sensors | grep "CPU Temperature"
echo "\nTemperature de la Carte Mere"
sudo sensors | grep "MB Temperature"
echo "\nVitesse du Ventilo CPU"
sudo sensors | grep "CPU FAN Speed"
echo "\nVitesse du Ventilo Chassis"
sudo sensors | grep "CHASSIS1 FAN Speed"
echo "\nTemperature du Core 0"
sudo sensors | grep "Core 0"
echo "\nTemperature du Core 1"
sudo sensors | grep "Core 1"
echo "\nTemperature ambiante"
sudo sensors | grep "temp1"

