# -*- coding:utf-8 -*-
import socket
import os
import sys
import struct

#line_input 下标表示的含义如下
#(pi_id 0)  (video_name 1)  (video_id 2) 
#(video_minutes 3)  (pi_sr 4)  (pi_space(b) 5)  
#(time_begin 6) (time_end 7) ( flag 8)
def socket_client(line_input):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('10.28.145.192', 6666))
    except socket.error as msg:
        print (msg)
        sys.exit(1)
    
    print(s.recv(1024))
    filepath=str(line_input[1])
    while 1:
        print('begin send')

        if os.path.isfile(filepath):
            #发送树莓派的编号id 和视频id等
            pi_information=str(line_input[0])+'|'+str(line_input[2])+'|'
            pi_information+=str(line_input[1])+'|'+str(os.path.getsize(filepath))+'|'
            pi_information+=str(line_input[6])+'|'+str(line_input[7])
            s.send(pi_information.encode('utf-8'))
        
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包含文件名和文件大小
            fhead = struct.pack('128sl', os.path.basename(filepath).encode('utf-8'),os.stat(filepath).st_size)
            s.send(fhead)
            print ('client filepath: {0}'.format(filepath))

            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print ('{0} file send over...'.format(filepath))
                    break
                s.send(data)
        else:
            print("no find file")
        re_mes=(s.recv(1024)).decode()
        back_message=''
        if re_mes=='video_upload_success':
            back_message='true'
        elif re_mes=='video_upload_failed':
            back_message='false'     
        s.close()

        break
    return back_message

if __name__ == '__main__':
    line_input=['(pi_id0)','saveDir.avi','(video_id2)' 
        ,'(video_minutes3)','(pi_sr4)','(pi_space(b)5)' 
        ,'(time_begin6)','(time_end7)','( flag8)']
    socket_client(line_input)
