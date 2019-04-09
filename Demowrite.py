# -*- coding:utf-8 -*-
import paho.mqtt.publish as publish
import time
import socket
ip=socket.gethostbyname(socket.getfqdn(socket.gethostname()))
HOST=ip
HOST = "10.28.145.192"
PORT = 61613
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("test")

def on_message(client, userdata, msg):
    print(msg.topic+" "+msg.payload.decode("utf-8"))

if __name__ == '__main__':
    client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    # client = mqtt.Client(client_id)    # ClientId不能重复，所以使用当前时间
    # client.username_pw_set("admin", "123456")  # 必须设置，否则会返回「Connected with result code 4」
    # client.on_connect = on_connect
    # client.on_message = on_message
    # client.connect(HOST, PORT, 60)
    # client.publish("test", "你好 MQTT", qos=0, retain=False)  # 发布消息

    #publish.single("Server_topic_pi1", "pi_video_server", qos = 1,hostname=HOST,port=PORT, client_id=client_id,auth = {'username':"admin", 'password':"password"})
    #publish.single("Server_topic_pi2", "Message_video_start ws.mp4 1", qos = 1,hostname=HOST,port=PORT, client_id=client_id,auth = {'username':"admin", 'password':"password"})
    publish.single("Server_topic_pi1", "pi_video_client 1 testthree.mp4", qos = 1,hostname=HOST,port=PORT, client_id=client_id,auth = {'username':"admin", 'password':"password"})
    #publish.single("Server_topic_pi2", "pi_video_server", qos = 1,hostname=HOST,port=PORT, client_id=client_id,auth = {'username':"admin", 'password':"password"})
