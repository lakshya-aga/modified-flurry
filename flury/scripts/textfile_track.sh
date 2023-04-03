#! /usr/bin/bash
#date=$(date)

#Create sample file
echo -e "\n$date \nCreating Sample"
echo $(echo -e "Sample" > sample.txt) 

echo -e "Set Camflow Tracking (sample.txt)"
echo $(sudo camflow --track-file sample.txt true) 

echo -e "Remove Tracked File"
echo $(rm sample.txt)
