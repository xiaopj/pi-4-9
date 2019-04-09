# -*- coding:utf-8 -*-
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import video_shoot
import File_client  
from datetime import datetime,timedelta
import pi_video_server 
import pi_video_client 
import redis_store
import socket
#ip=socket.gethostbyname(socket.getfqdn(socket.gethostname()))
#HOST=ip
HOST ="10.28.145.192"
PORT = 61613

#将视频信息存入redis数据库的key值,pi_video_id 与key值对应
num_key="pi:1"

def client_loop():
    client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

    client = mqtt.Client(client_id)    # ClientId不能重复，所以使用当前时间
    client.username_pw_set("admin", "password")  # 必须设置，否则会返回「Connected with result code 4」
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, 60)

    client.loop_forever()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("Server_topic_pi1") #如果发布者使用不同的语言写的，只需此处的订阅主题一样

def on_message(client, userdata, msg):
    global num_key
    print('---------------------------------')
    print("topic is:"+msg.topic)
    print("msg is:"+msg.payload.decode("utf-8"))

    s=msg.payload.decode("utf-8")
    #对服务器的消息进行解析
    list_s = s.split(' ')
    print(list_s)
    s=list_s[0]
    #向服务器上传视频
    #list_s[1]=video_name,list_s[2]=video_minutes
    if s=='Message_video_start' :
        num_key=redis_store.redis_store().select_key()
        pi_video_id=num_key.split(":")[1]
        print(num_key)
        print(pi_video_id)
        print("开始上传视频...")
        test = video_shoot.video_shoot(num_key,pi_video_id,list_s[1],list_s[2])
        test.begin_video()
        #将视频写入文件
        #test.write_file()
        
        #将视频信息写入数据库
        input_line=test.video_information()
        print(input_line)
        video=redis_store.redis_store(num_key,input_line)   
        video.insert()
        print("视频信息记录完成success")
        
        #back_mes为判断视频是否成功上传服务器的信息
        print(input_line)
        back_mes=File_client.socket_client(input_line)
        print("数据库记录视频信息success")
        print("back_mess:++++++"+back_mes)
        if back_mes=='true':
            # 发布视频成功上传的消息
            client.publish('Pi1_1_topic', payload="Message_video_send_successful", qos=1)  
            print("视频上传服务器成功")
        elif back_mes=='flase':    
            # 发布视频上传失败的消息
            client.publish('Pi1_1_topic', payload="Message_video_send_failed", qos=1)          
            print("视频上传服务器失败")
    #向服务器重新上传视频
    elif  s=='Message_video_upload_failed':
        print("开始重新上传视频...")
        
        print("开始从数据库中选择最新拍摄的视频上传...")
        input_line=[]
        select_test=redis_store.redis_store()
        input_line=select_test.select()
        if input_line!=[]:
            print("!!!!")
            back_mes=File_client.socket_client(input_line)
            print("???")
            if back_mes=='true':
                # 发布视频成功上传的消息
                client.publish('Pi1_1_topic', payload="Message_video_send_successful", qos=1)  
                print("视频上传服务器成功")
            elif back_mes=='flase':    
                # 发布视频上传失败的消息
                client.publish('Pi1_1_topic', payload="Message_video_send_failed", qos=1)          
                print("视频上传服务器失败")
        else:
            print("数据库中没有视频，无法重新上传")
            client.publish('Pi1_1_topic', payload="Message_video_not_have", qos=1)
    #视频上传成功
    elif s=='Message_video_upload_success':
        print("树莓派拍摄视频，上传服务器成功")
    
    #树莓派对传视频,其中一个开启服务器
    elif s=='pi_video_server':
        print("come on")
        pi_video_server.start()
    
    #树莓派对传视频，其中一个作为客户端，下载文件,message分为三部分
    # list_s[0]=pi_video_client
    # list_s[1]=pi_video_id
    # list_s[2]=pi_video_name
    elif s=='pi_video_client':
        print("la la ")
        list_id=[]
        list_id.append(list_s[1]) 
        list_id.append(list_s[2])
        print(list_id)
        print("????")
        re_flag=pi_video_client.main(list_id)
        if re_flag=="true":
            print("视频对传成功")  
        elif re_flag=="false":
            print("视频对传失败") 

    elif s=='close':
        print("客户端掉线")
    else:
        print(s+"无效指令")
        client.publish('Pi1_1_topic', payload="unknown_order", qos=1)  # 发布消息

#字符串拆分与拼接 string+1操作     
def string_num_add(num):
    l=num.split(':')
    #print( type(l[1]))
    l[1]=':'+str(int(l[1])+1)
    num=''.join(l)
    return num

if __name__ == '__main__':
    client_loop()
