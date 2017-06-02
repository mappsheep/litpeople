#!/bin/bash

#starting the system network service
echo 'Starting the network service'
sudo service networking start

#turning on broadcast reciever
echo 'Making sure "if" confiuguration is up'
sudo ifup wlan0

#this selects interface desingated in /etc/network/interface
echo 'Selecting WiFi interface'
sudo wpa_cli reconfigure

#requesting an IP Address from DNS server
echo 'Acquiring an IP address'
sudo dhclient wlan0
