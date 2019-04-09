# -*- coding:utf-8 -*-
import socket
import os
import redis_store
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
    print("pi_server_start...")
    while True:
        # 利用accept获取分套接字以及客户端的地址
        client_socket,client_addr = tcp_socket.accept()
        print(client_addr)
        # 接收客户端的数据
        
        first_re= client_socket.recv(4096).decode()
        print(first_re)
        list_id=first_re.split('|')
        file_name=list_id[1] 
        # 调用函数处理用户下载的文件
        mes = file_deal(file_name)
        print("nihhhhhh")
        if mes:
            # 如果文件不为空发送
            print("sadsa")
            #将视频的信息大小信息发送给客户
            select=redis_store.redis_store("pi",list_id)
            input_line=select.id_findline()
            if input_line:
                last_message='|'.join(input_line) 
                video_size = os.path.getsize(file_name)
                pre_message="video_file_have"+"|"
                pre_message+=str(video_size)
                pre_message+="|"+last_message
                client_socket.send(pre_message.encode())
                client_socket.send(mes)
                #关闭分套接字
                print("ooook")
            else:
                mes="no_file"+"|"+"0"
                client_socket.send(mes.encode())
        else:
            mes="no_file"+"|"+"0"
            client_socket.send(mes.encode())
        #接收客户端的回传信息，判读是否需要一直开启
        re_inf=client_socket.recv(1024).decode()
        if re_inf=="true":
            client_socket.close()
            print("客户取到完整视频")
            break
        else:
            print("客户没有获取到完整的视频")
            print("等待用户重新连接...")
if __name__ == "__main__":
    start()
