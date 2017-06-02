#!/bin/bash

#forcing wifi to be a thing
echo Trying to Boot the WiFi

sudo wpa_cli reconfigure
sudo dhclient wlan0
