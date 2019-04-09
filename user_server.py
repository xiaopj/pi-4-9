# -*- coding:utf-8 -*-
import socket
import os
import redis_store
import threading
import sys
ip=socket.gethostbyname(socket.getfqdn(socket.gethostname()))
HOST=ip
def file_deal(file_name):
    # 定义函数用于处理用户索要下载的文件
    try:
        # 二进制方式读取
        files = open(file_name, "rb")
        mes = files.read()
    except:
        print("没有该文件")
    else:
        files.close()
        return mes

def start():
    # 创建套接字
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 固定端口号
    tcp_socket.bind((HOST,9998))
    # 将主动套接字转为被动套接字
    tcp_socket.listen(128)
    print("pi server for java client start...")
    while True:
        # 利用accept获取分套接字以及客户端的地址
        client_socket,client_addr = tcp_socket.accept()
        print(client_addr)
        
        # 接收手机客户端的第一次传来的数据
        file_name= client_socket.recv(1024).decode()
        print(file_name)
         
        # 调用函数处理用户下载的文件
        mes = file_deal(file_name)
        list_filename=file_name.split(" ")
        print("nihhhhhh")
        if mes:
            # 如果文件不为空发送
            print("sadsa")
            #将视频的信息大小信息发送给客户
            select=redis_store.redis_store("pi",list_filename)
            input_line=select.name_findline()
            if input_line!=False:
                #回传视频存在判断信息 及视频文件的大小
                video_size = os.path.getsize(file_name)
                pre_message="video_file_have"+"|"
                pre_message+=str(video_size)
                pre_message+='\n'
                client_socket.send(pre_message.encode())
                client_socket.send(mes)
                #关闭分套接字
                print("ooook")

            elif input_line==False:
            	print("no_file")
            	mes="no_file"+'\n'
            	client_socket.send(mes.encode())
        else:
        	mes="no_file"
        	client_socket.send(mes.encode())
        client_socket.close()
       	break

def pi_service():
    try:
    	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	s.bind((HOST, 6667))
    	s.listen(10)
    except socket.error as msg:
    	print (msg)
    	sys.exit(1)
    print ('Waiting connection...')

    while 1: 
    	# 利用accept获取分套接字以及客户端的地址
    	conn, addr = s.accept()
    	t = threading.Thread(target=thread_satrt, args=(conn, addr))
    	t.start()
    	break

def thread_satrt(client_socket,client_addr):
    while True:
        print(client_addr)
        
        # 接收手机客户端的第一次传来的数据
        file_name= client_socket.recv(1024).decode()
        print(file_name)
         
        # 调用函数处理用户下载的文件
        mes = file_deal(file_name)
        list_filename=file_name.split(" ")
        print("nihhhhhh")
        if mes:
            # 如果文件不为空发送
            print("sadsa")
            #将视频的信息大小信息发送给客户
            select=redis_store.redis_store("pi",list_filename)
            input_line=select.name_findline()
            if input_line!=False:
                #回传视频存在判断信息 及视频文件的大小
                video_size = os.path.getsize(file_name)
                pre_message="video_file_have"+"|"
                pre_message+=str(video_size)
                pre_message+='\n'
                client_socket.send(pre_message.encode())
                client_socket.send(mes)
                #关闭分套接字
                print("ooook")

            elif input_line==False:
            	print("no_file")
            	mes="no_file"+'\n'
            	client_socket.send(mes.encode())
        else:
        	mes="no_file"
        	client_socket.send(mes.encode())
       	client_socket.close()
       	break
if __name__ == "__main__":
    #start()
    # mes=file_deal('today.mp4')
    # print(type(mes))	
    pi_service()