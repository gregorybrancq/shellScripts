#!/bin/bash
# Script pour changer le fond d'écran lors du changement de bureau.

desktop_dir="/home/greg/Wallpaper/Home/" # chemin complet du dossier des images; 
desktop_img[0]="desk_1.jpg"
desktop_img[1]="desk_2.jpg"
desktop_img[2]="desk_3.png"
desktop_img[3]="desk_4.jpg"
desktop_img[4]="desk_5.jpg"

setdesktop() {
   gsettings set org.gnome.desktop.background picture-uri "file://$desktop_dir$1"
   }

xprop -root -spy _NET_CURRENT_DESKTOP | (
   while read -r; do
      desk=${REPLY:${#REPLY}-1:1}
      setdesktop ${desktop_img[$desk]}
   done
   )

