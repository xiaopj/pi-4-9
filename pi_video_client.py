# -*- coding:utf-8 -*-
from socket import *
import os
import redis_store
#list_info[0]=pi_video_id list_info[1]=pi_video_name
def main(list_info):
    print(list_info)
    # 建立套接字
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    # 接收用输入的服务器端的ip和端口
    # tcp_ip = input("请输入ip:")
    # tcp_port = int(input("请输入端口:"))
    tcp_ip="10.112.99.91"
    tcp_port=9999
    # 连接服务器
    tcp_socket.connect((tcp_ip, tcp_port))
    # 输入要下载的文件名
    #file_name = input("请输入要下载的文件名:")
    file_name=list_info[0]+"|"+list_info[1]
    # 将文件名发送至服务器端
    tcp_socket.send(file_name.encode())
    
    # 创建一个空文件
    file_name=list_info[1]
    fp = open(file_name, "wb")
    # 用与计算读取的字节数
    time = 0
    #解码在视频接收前的信息
    #re_list[0]为文件是否存在信息 re_list[1]为文件大小信息
    pre_message = tcp_socket.recv(1024).decode()
    re_list=pre_message.split('|')
    filesize=int(re_list[1])
    print("this ?")
    while True:
        # 接收服务器端返回的内容
        print(re_list[0])
        if re_list[0]=="video_file_have":
            recvd_size = 0  # 定义已接收文件的大小
            print ('start receiving...')
            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = tcp_socket.recv(1024)
                    recvd_size += len(data)
                else:
                    data = tcp_socket.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print ('end receive...')
            #判断视频文件的完整性
            print("laiheee")
            if os.path.getsize(file_name)==int(re_list[1]):
                re_inf="true"
                print("下载的文件完整，开始写入数据库")
                input_line=pi_line_message(pre_message)
                #数据库写入
                key_id=redis_store.redis_store()
                str_id=key_id.id_select_key()
                store=redis_store.redis_store(str_id,input_line)
                store.other_video_insert()
            else:
                re_inf="false"
                print("下载的文件不完整")

        elif re_list[0]=="no_file":
            # 关闭文件
            fp.close()
            # 删除刚刚创建的文件
            os.remove(file_name)
            print("没有您要下载的文件")
            re_inf="false" 
        break
    #视频是否成功互传判断
    print("re_inf"+re_inf)
    if re_inf=="true":
        tcp_socket.send("true".encode())
    else:
        tcp_socket.send("false".encode())
    # 关闭套接字
    tcp_socket.close()
    return re_inf

def pi_line_message(str):
    list_mes=str.split("|")
    list_mes.pop(0)
    list_mes.pop(0)
    print (list_mes)
    return list_mes

if __name__ == '__main__':
    list=['1','ws.mp4']

    main(list)
