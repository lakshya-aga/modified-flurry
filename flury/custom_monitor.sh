#Custom suscriber to Paho
echo -e "\n\nStarting Custom MQTT monitor\n\n"
#echo $(python3 /home/shah/flurry/custom_mqtt_monitor.py)
gnome-terminal -e "python3 /home/shah/flurry/custom_mqtt_monitor.py" -t "Custom MQTT Monitor"

