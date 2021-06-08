#!/bin/bash

# I built ip1.txt 2020-03-22
for a in `cat ip1.txt` 
do  
	curl -s http://localhost:8000/fqdn/$a 
done | jq
