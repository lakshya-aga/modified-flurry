import paho.mqtt.client as mqtt
import time
import zlib
import base64

'''
def on_connect(client,userdata,flags,rc):
  if rc==0:
    print("client connected")
    global connected
    connected=True
  else:
    print("client not connected")

def on_message(client,userdata,message):
  decoded_msg = zlib.decompress(base64.b64decode(message.payload.decode('latin-1'))).decode('latin-1')
  print(decoded_msg)
  #print("Msg rx \n" + str(message.payload.decode("utf-8")))
  #print("Topic " +str(message.topic))

connected = False
Messagerecieved = False

addr = "localhost"
port = 1883
user = "camflow"
pw = "camflow"

client = mqtt.Client("MQTT")
client.on_message = on_message
client.username_pw_set(user, password=pw)
client.on_connect = on_connect
client.connect(addr, port=port)
client.loop_start()
client.subscribe("camflow/provenance/#")
while connected!=True:
  time.sleep(0.2)
while Messagerecieved!=True:
  time.sleep(0.2)
  
client.loop_stop()'''
message="AQAAAAAAAEC/FgIAAAAAAAUAAABhim0rj28AAAAAAAA="
decoded_msg = base64.b64decode(message).decode('latin-1')
print(decoded_msg)
