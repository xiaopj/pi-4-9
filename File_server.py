import socket
import threading
import time
import sys
import os
import struct
import redis_store
from Demoread import string_num_add
#全局变量
i=0
server_key='server:1'
ip=socket.gethostbyname(socket.getfqdn(socket.gethostname()))
HOST=ip
print(HOST)
def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, 6666))
        s.listen(10)
    except socket.error as msg:
        print (msg)
        sys.exit(1)
    print ('Waiting connection...')

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()
#解析树莓派的id和拍摄的第几个视频id
def open_pi(pi_informatin):
    list=pi_informatin.split('|')
    print("touwenjianchaifen")
    return list

def deal_data(conn, addr):
    print( 'Accept new connection from {0}'.format(addr))
    #conn.settimeout(500)
    conn.send(('Hi, Welcome to the server!').encode())
    # 树莓派id和视频id
    pi_information = conn.recv(1024)
    pi_send_inf= open_pi(pi_information.decode())

    global i,server_key
    i=i+1
    new_filename=''
    #开始接收视频
    while 1:
        fileinfo_size = struct.calcsize('128sl')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.decode().strip('\00')
            new_filename = os.path.join('./', 'new_' + fn)
            print ('file new name is {0}, filesize if {1}'.format(new_filename,filesize))

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(new_filename, 'wb')
            print ('start receiving...')

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print ('end receive...')
            #对传过来的视频做完整性判断
            print(pi_send_inf[3])
            if int(pi_send_inf[3])==os.path.getsize(new_filename):
                print("lai le ")
                input_line=[]
                #input_line.append(i)
                server_key=redis_store.redis_store().server_select_key()
                print(server_key)
                input_line.append(server_key.split(':')[1])
                input_line.append(new_filename)
                input_line.append(os.path.dirname(os.path.realpath(__file__)))
                input_line.append(pi_send_inf[3])
                input_line.append(pi_send_inf[0])
                input_line.append(pi_send_inf[1])
                input_line.append(pi_send_inf[2])
                input_line.append(pi_send_inf[4])
                input_line.append(pi_send_inf[5])
                data_handle(input_line)
                conn.send("video_upload_success".encode())
                print('视频成功上传服务器')
            else:
                print("视频文件在传输过程中出现损坏!")
                conn.send(("video_upload_failed").encode())
        conn.close()
        break
    #write_file(new_filename,i,pi_id,pi_video_id)
    #将视频信息写入数据库
    

#数据库操作，将收到的视频写入数据库
def data_handle(input_line):
    print("put video line information to redis server.. ")
    global server_key
    print(server_key)
    print(input_line)    
    video=redis_store.redis_store(server_key,input_line)   
    video.server_insert()
    #server:num+1 键值加一
    #server_key=string_num_add(server_key)
    print("ok")

if __name__ == '__main__':
    socket_service()