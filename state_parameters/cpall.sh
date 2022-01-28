#!/bin/bash

for STATE in QLD ACT VIC NT WA SA NSW
do 
	echo "$STATE"
	cp TAS_low.json ${STATE}_low.json
	cp TAS_high.json ${STATE}_high.json
	cp TAS_baseline.json ${STATE}_baseline.json
done

