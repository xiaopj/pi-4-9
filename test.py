import re
s1 = "xxx出生于1995年6月1日"
s2 = "xxx出生于1995/6/1"
s3 = "xxx出生于1995-6-1"
s4 = "xxx出生于1995-06-01"
s5 = "xxx出生于1995-06"

l=[s1,s2,s3,s4,s5]

for index in l:
	res = re.match("\D+(\d+)\D(\d+)\D*(\d+)*\D*",index)
	for i in range(1,4):
		if res.group(i):
			print(res.group(i)+" ",end="")
	print("")
# # 删除字符串中的 Python注释 
# num = re.sub(r'#.*$', "", phone)
# print ("电话号码是: "+num)
 
# # 删除非数字(-)的字符串 
# num = re.sub(r'\D', "", phone)
# print ("电话号码是 : "+ num)
# import time

# def string_num_add(num):
# 		#print("ssssss")
# 		l=num.split(':')
# 		#print( type(l[1]))
# 		l[1]=':'+str(int(l[1])+1)
# 		num=''.join(l)
# 		return num
st="name"
l=st.split(" ")
print(type(l))


