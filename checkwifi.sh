#!/bin/bash

wget -q --tries=10 --timeout=20 --spider http://google.com
if [[ $? -eq 0 ]]; then
	echo "Live"
else
	echo "Not Live"
	./restartnet.sh
fi
