#!/bin/bash

while true; do
    echo "$(date)"
    python inxwords.py -nw --loop -d 1 -y /home/botuser/bin/data/inxwords.yaml
    echo "$(date)"
    sleep 60
done
