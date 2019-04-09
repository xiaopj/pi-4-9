# -*- coding:utf-8 -*-
import redis
import sys
import os

class redis_store(object):
	
	def __init__(self,key='',input_list=[]):
		pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
		r = redis.Redis(connection_pool=pool)		
		self.key=key
		self.list=input_list	
		self.r=r
	#树莓派数据库的插入	
	def insert(self):
		#pi_id video_name video_id  video_minutes  pi_sr  pi_space(b)  time_begin  time_end flag
		# r.hmset("user:003", {"username":"antirez","password":"P1pp0","age":"34"})
		if self.list!=[]:
			#print("ssss"+self.key)
			print(self.list)
			self.r.hmset(self.key, {"pi_id":self.list[0],
				"video_name":self.list[1],
				#"video_id":self.list[2],
				#与key值保持一致
				"video_id":self.key.split(':')[1],
				"video_minutes":self.list[3],
				"pi_sr":self.list[4],
				"pi_space(b)":self.list[5],
				"time_begin":self.list[6],
				"time_end":self.list[7],
				"flag":self.list[8]
			})
			#s=self.r.hgetall("pi:001")
			#print(s)
			print("成功录入树莓派数据库")
		else:
			print("非法信息，无法录入树莓派数据库")		
	#服务器数据库的插入 ？ 有个啥没有修改
	def server_insert(self):
		#server_id	video_name	src	space	pi_id	pi_video_id	pi_video_name time_begin  time_end
		if self.list!=[]:
			#print("ssss"+self.key)
			print(self.list)
			self.r.hmset(self.key, {"server_id":self.list[0],
				"video_name":self.list[1],
				"src":self.list[2],
				"space":self.list[3],
				"pi_id":self.list[4],
				"pi_video_id":self.list[5],
				"pi_video_name":self.list[6],
				"time_begin":self.list[7],
				"time_end":self.list[8]
				})
			#s=self.r.hgetall("pi:001")
			print("成功录入服务器数据库")
		else:
			print("非法信息，无法录入服务器数据库")
	#树莓派找到最新的视频信息,pi:num 最大
	def select(self):
		#print(self.r.hgetall("pi:001"))		
		keys = self.r.keys("pi:*")
		print(keys)
		line=[]
		num=0
		#找到最大的pi:num
		for term in keys:
			term_list=term.split(':')
			if int(term_list[1]) >num:
				num=int(term_list[1])
				line=term		
		if line!=[]:
			#print(self.r.hgetall(line)) 取所有的键值对
			print(self.r.hvals(line))
			return self.r.hvals(line)	
		else:
			return line	
		#判断最新的视频
		#倒叙法
		# for i in range(len(keys)-1, -1, -1):
  			#  print(keys[i])
	#树莓派找到最新的	num_key="pi:i"->"pi:i+1"
	#树莓派数据库“pi:1”键值+1
    #num_key=string_num_add(num_key) 
	def select_key(self):
		#print("???")
		keys = self.r.keys()
		#print(keys)
		str_key=''
		num=0
		print(keys)
		#找到最大的pi:num
		for term in keys:
			term_list=term.split(':')
			if term_list[0]=='pi':
				if int(term_list[1]) >num:
					num=int(term_list[1])		
		str_key="pi:"+str(num+1)	
			
		print(str_key)
		return str_key
	#服务器找到最新的server_key ,模糊查找
	def server_select_key(self):
		keys = self.r.keys("server:*")
		#print(keys)
		server_key=''
		num=0
		print(keys)
		#找到最大的pi:num
		for term in keys:
			term_list=term.split(':')
			if term_list[0]=='server':
				if int(term_list[1]) >num:
					num=int(term_list[1])		
		server_key="server:"+str(num+1)	
			
		#print(server_key)
		return server_key

	#将其它树莓派传来的视频信息写入自己的数据库
	#pi_id video_name video_id  video_minutes  pi_sr  pi_space(b)  time_begin  time_end flag	
	def other_video_insert(self):
		if self.list!=[]:
			#print("ssss"+self.key)
			print(self.list)
			self.r.hmset(self.key, 
				{"pi_id":self.list[0],
				"video_name":self.list[1],
				"video_id":self.list[2],
				"video_minutes":self.list[3],
				"pi_sr":self.list[4],
				"pi_space(b)":self.list[5],
				"time_begin":self.list[6],
				"time_end":self.list[7],
				"flag":0
			})
			print("成功录入树莓派数据库")
		else:
			print("非法信息，无法录入树莓派数据库")
	#树莓派根据视频号进行查找，返回一行信息
	def id_findline(self):
		print(self.list)
		keys = self.r.keys("pi:*")
		for temp in keys:
			print(temp)
			list_line=self.r.hmget(temp,"video_id","video_name")
			print(list_line)
			if (list_line[0]==self.list[0] and list_line[1]==self.list[1]):
				pi_id=self.r.hmget(temp,"pi_id")
				video_name=self.r.hmget(temp,"video_name")
				video_id=self.r.hmget(temp,"video_id")
				video_minutes=self.r.hmget(temp,"video_minutes")
				pi_sr=self.r.hmget(temp,"pi_sr")
				pi_space=self.r.hmget(temp,"pi_space(b)")
				time_begin=self.r.hmget(temp,"time_begin")
				time_end=self.r.hmget(temp,"time_end")
				flag=self.r.hmget(temp,"flag")
				r=[]
				r.append(pi_id[0])
				r.append(video_name[0])
				r.append(video_id[0])
				r.append(video_minutes[0])
				r.append(pi_sr[0])
				r.append(pi_space[0])
				r.append(time_begin[0])
				r.append(time_end[0])
				r.append(flag[0])
				print(r)
				return r
		print("树莓派根据视频号在数据库没有找到视频")							
		return False
	#树莓派根据视频名进行查找，返回一行信息
	def name_findline(self):
		print(self.list)
		keys = self.r.keys("pi:*")
		for temp in keys:
			print(temp)
			list_line=self.r.hmget(temp,"video_name")
			print(list_line)
			if (list_line[0]==self.list[0] ):
				pi_id=self.r.hmget(temp,"pi_id")
				video_name=self.r.hmget(temp,"video_name")
				video_id=self.r.hmget(temp,"video_id")
				video_minutes=self.r.hmget(temp,"video_minutes")
				pi_sr=self.r.hmget(temp,"pi_sr")
				pi_space=self.r.hmget(temp,"pi_space(b)")
				time_begin=self.r.hmget(temp,"time_begin")
				time_end=self.r.hmget(temp,"time_end")
				flag=self.r.hmget(temp,"flag")
				r=[]
				r.append(pi_id[0])
				r.append(video_name[0])
				r.append(video_id[0])
				r.append(video_minutes[0])
				r.append(pi_sr[0])
				r.append(pi_space[0])
				r.append(time_begin[0])
				r.append(time_end[0])
				r.append(flag[0])
				print(r)
				return r
		print("树莓派根据视频名字在数据库没有找到视频")							
		return False	
	def id_select_key(self):
		#print("???")
		keys = self.r.keys("pi:*")
		#print(keys)
		str_key=''
		num=0
		print(keys)
		#找到最大的pi:num
		for term in keys:
			term_list=term.split(':')
			if term_list[0]=='pi':
				if int(term_list[1]) >num:
					num=int(term_list[1])		
		str_key="pi:"+str(num+1)	
			
		print(str_key)
		return str_key	
if __name__ == '__main__':
	# 插入删除样例模板
	# key="pi:005"
	# list=['1','1','1','1','1','1','1','1','1']
	# test=redis_store(key,list)
	# #test.insert()
	# test=data_store()
	# test.select()
	
	#查询样例模板
	#select_test=redis_store()
	#select_test.select_key()

	#树莓派其它视频插入模板
	key="pi:8"
	list=['today.mp4']
	test=redis_store(key,list)
	test.name_findline()
	# select_test=redis_store()
	# select_test.server_select_key()
	# select_test=redis_store()
	# select_test.select()