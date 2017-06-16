#!/bin/bash

#performing daemon reload
sudo systemctl daemon-reload

#restart the network system service
sudo service networking restart
