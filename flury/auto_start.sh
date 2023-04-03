#! /usr/bin/bash
DATE=$(date)
BOOL=$1 #t = test, f = flurry

#XAMPP    
echo -e "\n$DATE \n\nStarting XAMPP...\n"
sudo /opt/lampp/lampp start

#FREE PORT 
echo $(sudo fuser -k 1883/tcp)

#Mosquitto MQTT
echo -e "\nStarting Mosquitto MQTT...\n"
gnome-terminal -e "mosquitto -c /home/shah/flurry/mosquitto/moq.conf" -t "Mosquitto MQTT Broker"
sleep 1

#Restart Camflow to connect to MQTT
echo -e "\nRestarting Camflow service...\n"
echo $(sudo systemctl restart camflowd.service)

#Mosquitto Subscriber Monitor
#echo -e "\nStarting Mosquitto Subscriber Monitor...\n"
#gnome-terminal -e "mosquitto_sub -h localhost -t camflow/provenance/#" -t "Mosquitto Subscriber Monitor"

#Custom MQTT Monitor
#gnome-terminal -e "python3 mqtttest.py" -t "Custom MQTT Monitor"

<<'comment'

#Clear
echo -e "\nClearing Terminal...\n"
echo $(clear)

if [ $BOOL == "t" ]; then
    sleep 1
    echo $(sudo ./testsample.sh)
elif [ $BOOL == "f" ]; then
    sleep 1
    echo -e "\nStarting Flurry App...\n"
    gnome-terminal -e "python3 ../webserver.py" -t "Flurry Application"
    #sleep 1
    #gnome-terminal -e "python3 ../mqtttest.py" -t "Custom MQTT Monitor"
    #echo $(sudo ./custom_monitor.sh)
    #gnome-terminal -e "./custom_monitor.sh" -t "Flurry App"
fi
comment
