# -*- codeing: utf-8 -*-
import paho.mqtt.client as mqtt
import struct


gUSV_speed = 0.0
gUSV_angle = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/ctrl")
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global gUSV_speed, gUSV_angle
    print("Data received.")
    data = msg.payload
    
    try:
        gUSV_speed, gUSV_angle, magic_code = struct.unpack("!ffB", data) 
        
        print("Topic: ", msg.topic+'\nBoat : %f, %f' % (gUSV_speed, gUSV_angle))
        
    except:
        
        pass
        
    
client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

#Ali
#client.connect("47.100.209.79", 1883, 60)
#Beijing lab.
#client.connect("114.251.25.35", 1883, 60)
#Iot Test
client.connect("139.196.113.149", 1883, 60)
#client.connect("test.mosquitto.org", 1883, 60)
#client.connect("iot.eclipse.org", 1883, 60)
#client.connect("iot.eclipse.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
