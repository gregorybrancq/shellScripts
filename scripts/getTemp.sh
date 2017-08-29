#!/bin/zsh -f

echo "\n Date : " `date`
#sudo smartctl -A /dev/sda | grep Temperature_Celsius
echo "\nTemperature du 1er disque"
sudo hddtemp /dev/sda
echo "\nTemperature du 2eme disque"
sudo hddtemp /dev/sdb
if [ "$PORTABLE" -eq "0" ]; then
    echo "\nTemperature du 3eme disque"
    sudo hddtemp /dev/sdc
    echo "\nTemperature du CPU"
    sudo sensors | grep "CPU Temperature"
    echo "\nTemperature de la Carte Mere"
    sudo sensors | grep "MB Temperature"
fi
echo "\nVitesse du Ventilo CPU"
if [ "$PORTABLE" -eq "1" ]; then
    sudo sensors | grep "fan1"
else
    sudo sensors | grep "CPU FAN Speed"
fi
if [ "$PORTABLE" -eq "0" ]; then
echo "\nVitesse du Ventilo Chassis"
    sudo sensors | grep "CHASSIS1 FAN Speed"
fi
echo "\nTemperature des Core"
sudo sensors | grep -i "core "
echo "\nTemperature ambiante"
sudo sensors | grep "temp1"
echo "\n"

