#!/bin/bash

#sending IP address to Scott's email
echo "Sending email"

_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "jiglive IP address is %s\n" "$_IP"
fi

echo "jiglive IP address is "  "$_IP" | ssmtp blinkin1@vt.edu
echo "jiglive IP address is "  "$_IP" | ssmtp mapp7640@vt.edu
