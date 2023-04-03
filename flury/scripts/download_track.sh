#echo -e "Set Camflow Tracking (wget)"
#echo $(sudo camflow --track-file /bin/wget true) 

#Download file
echo -e "\n$date \nCreating Sample(wget)"
echo $(wget https://camflow.org/#recording) 

#echo -e "Disable Camflow Tracking (wget)"
#echo $(sudo camflow --track-file /bin/wget false) 
