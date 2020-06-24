import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as paho
import time

# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client

# MQTT broker hosted on local machine
mqttc = paho.Client()

# Settings for connection
# TODO: revise host to your ip
host = "localhost"
topic = "Mbed"

t = np.arange(0,20,0.5)
data = np.arange(0.0,160.0,1.0)

i = 0

# Callbacks
def on_connect(self, mosq, obj, rc):
      print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
      print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")
      global i
      global data
      if i > 4 and i <= 164:
            data[i-5] = float(msg.payload)
            if i == 164:
                  fig, ax = plt.subplots(2, 1)
                  ax[0].plot(t, data[0::4], label="x-acc")
                  ax[0].plot(t, data[1::4], label="y-acc")
                  ax[0].plot(t, data[2::4], label="z-acc")
                  ax[0].set_xlabel('timestamp')
                  ax[0].set_ylabel('acc value')
                  ax[0].set_title('Acceleration Plot')
                  ax[0].legend()
                  ax[1].stem(t, data[3::4])
                  ax[1].set_xlabel('timestamp')
                  ax[1].set_ylabel('Tilt')
                  plt.show()
      i += 1
      
def on_subscribe(mosq, obj, mid, granted_qos):
      print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
      print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

# Publish messages from Python
num = 0
while num != 5:
      ret = mqttc.publish(topic, "Message from Python!\n", qos=0)
      if (ret[0] != 0):
            print("Publish failed")
      mqttc.loop()
      time.sleep(1.5)
      num += 1

# Loop forever, receiving messages
mqttc.loop_forever()