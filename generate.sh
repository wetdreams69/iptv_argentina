#!/bin/bash

echo $(dirname $0)

python3 -m pip install requests streamlink

cd $(dirname $0)/scripts/

python3 generator.py > ../playlist.m3u

echo Done!