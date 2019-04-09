# -*- coding: utf-8 -*-
import cv2
from datetime import datetime,timedelta
import os
import File_client

class video_shoot(object):
    # 初始化的参数为视频拍摄时间，和视频的名字
    #设置视频默认拍摄的时间为1min
    #video_time=1
    def __init__(self,key,video_id,video_name,video_minutes):
        self.key=key
        self.video_minutes=video_minutes
        self.video_name=video_name
        self.video_id=video_id
        #设置的树莓派编号
        self.pi=1
        #默认视频大小
        self.video_size=0
        self.begin_time=0
        self.end_time=0
        self.flag=1
    #开始拍摄视频
    def begin_video(self):
        print("sdas")
        now = datetime.now()
        self.begin_time=datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
        time_end = now + timedelta(minutes=int(self.video_minutes))
        end = datetime.strftime(time_end, '%Y-%m-%d %H:%M:%S')
        self.end_time=end
        print(now)
        # 通过cv2中的类获取视频流操作对象cap
        cap = cv2.VideoCapture(0)
        # 调用cv2方法获取cap的视频帧（帧：每秒多少张图片）
        fps = cap.get(cv2.CAP_PROP_FPS)
         
        # 获取cap视频流的每帧大小
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        print(size)

        # 定义编码格式mpge-4
        #fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')
        #定义编码格式XVID
        fourcc = cv2.VideoWriter_fourcc(*'mpeg')
        # 定义视频文件输入对象
        outVideo = cv2.VideoWriter(self.video_name, fourcc, fps, size)

        # 获取视频流打开状态
        if cap.isOpened():
            rval, frame = cap.read()
            print('ture')
        else:
            rval = False
            print('False')

        tot = 1
        c = 1
        # 循环使用cv2的read()方法读取视频帧
        while rval  :
            now2 = datetime.now()
            print(now2)
            if  datetime.strftime(now2,'%Y-%m-%d %H:%M:%S')<=end:
                rval, frame = cap.read()
                cv2.imshow('test', frame)
                # 每间隔20帧保存一张图像帧
                # if tot % 20 ==0 :
                #   cv2.imwrite('cut/'+'cut_'+str(c)+'.jpg',frame)
                #   c+=1
                tot += 1
                print('tot=', tot)
                # 使用VideoWriter类中的write(frame)方法，将图像帧写入视频文件
                outVideo.write(frame)
                cv2.waitKey(1)
            else:

                break
        #释放资源
        #(int)self.video_id+=1
        self.video_size=os.path.getsize(self.video_name)
        cap.release()
        outVideo.release()
        cv2.destroyAllWindows()

    #将视频的信息写入到树莓派拍摄的视频信息文件video_information中
    #文件头第一行为视频信息的字段 pi_id  video_id  video_minutes  pi_sr  pi_space(b)  time_begin  time_end
    def write_file(self):
        #获取到视频文件的大小
        self.video_size=os.path.getsize(self.video_name)
        file_object = open('video_information.txt', 'a')
        print(os.path.getsize('video_information.txt'))
        if os.path.getsize('video_information.txt')==0:
            print("sdas")
            file_object.write('pi_id  video_id  video_minutes  pi_sr  pi_space(b)  time_begin  time_end\n')
        line_input=[]
        line_input.append(self.pi)
        line_input.append(self.video_name)
        line_input.append(self.video_minutes)
        #文件路径信息
        #print( os.path.realpath(__file__))
        #print (os.path.dirname(os.path.realpath(__file__)))
        line_input.append('./')
        line_input.append(self.video_size)
        line_input.append(self.begin_time)
        line_input.append(self.end_time)
        file_object.write(str(line_input)+'\n')
        file_object.close()
    
    #返回视频名字
    def file_name(self):
        return self.video_name
    
    #pi_id video_name video_id  video_minutes  pi_sr  pi_space(b)  time_begin  time_end flag
    #返回视频的完整信息
    def video_information(self):
        line_input=[]
        line_input.append(self.pi)
        line_input.append(self.video_name)
        #line_input.append(self.video_id)
        #与视频key值一致
        line_input.append(self.key.split(':')[1])
        line_input.append(self.video_minutes)
        #文件路径信息
        #print( os.path.realpath(__file__))
        #print (os.path.dirname(os.path.realpath(__file__)))
        line_input.append(os.path.dirname(os.path.realpath(__file__)))
        line_input.append(self.video_size)
        line_input.append(self.begin_time)
        line_input.append(self.end_time)     
        line_input.append(self.flag)
        print("line")
        print(line_input)
        return line_input
if __name__ == '__main__':
    video_shoot("pi：001","1","test.mp4","1").begin_video()