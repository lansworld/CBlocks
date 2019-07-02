# -*- coding: utf-8 -*-

#绝对坐标系
START_POINT=[0,0]	#屏幕绝对坐标起点位置
BLOCK_SIZE=20  #模块的像素大小

##相对坐标定义
ROW=20					#总逻辑行数
COL=10					#总逻辑列数
INIT_POINT=[5,2]		#出现的起始位置
PREVIEW_POINT=[14,18]	#预览的中心点位置
TEXT_POINT=[12,2]		#成绩坐标
CENTER_POINT=[5,10]		#中间警告信息坐标

SZ_0=[0,0]  #中心点
SZ_U=[0,-1]	#上
SZ_D=[0,1]	#下
SZ_L=[-1,0]	#左
SZ_R=[1,0]	#右
SZ_LD=[-1,1]	#左下
SZ_RD=[1,1]		#右下
SZ_LU=[-1,-1]	#左上
SZ_RU=[1,-1]	#右上
SZ_D2=[0,2]		#下2
SZ_R2=[2,0]		#右2

#(ROW+2)*BLOCK_SIZE (COL+7)*BLOCK_SIZE
SET_MODE=[(COL+8)*BLOCK_SIZE,(ROW+2)*BLOCK_SIZE]		#分辨率

##颜色定义
#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
GREEN       = (  0, 155,   0)
BLUE        = (  0,   0, 155)
YELLOW      = (155, 155,   0)
TEXTCOLOR	= BLUE
FRAMECOLOR=(230,230,230)  ##框架背景色

#BORDERCOLOR = BLUE
KEY_REPEAT_TIME = 100 #按键后不放开重复执行时延，单位毫秒


def log2real_point(point):  #逻辑坐标转化为物理坐标
	realPoint=(point[0]*BLOCK_SIZE+START_POINT[0],point[1]*BLOCK_SIZE+START_POINT[1])
	return realPoint

def color2int(value):
	digit = list(map(str, range(10))) + list("ABCDEF")
	#print(digit)
	if isinstance(value, tuple):	#(155, 0, 0) => color2int(39680)
		#print(value[0],value[1],value[2]) 
		return  value[0]*256*256+value[1]*256+value[2]
	elif isinstance(value,str):	#FF0000 => (255,0.0)
		value = value.upper()
		if value[0:2] == '0X' and len(value)==8:
			value=value[2:8]
		else:	##错误的格式，返回0
			return(0,0,0)
		a1 = digit.index(value[0]) * 16 + digit.index(value[1])
		a2 = digit.index(value[2]) * 16 + digit.index(value[3])
		a3 = digit.index(value[4]) * 16 + digit.index(value[5])
		return (a1, a2, a3)
	elif isinstance(value,int):  #color2int(39680) => (155, 0, 0)
		a1 = int(value / 256)
		b1 = int(value % 256)
		a2 = int(a1 / 256)
		b2 = int(a1 % 256)
		return (a2, b2, b1)

class CPoint:
	def __init__(self,data):
		self.data=data
	def __add__(self,data):  	#+
		return CPoint([self.data[0]+data[0],self.data[1]+data[1]]) #用v创建一个新的对象返回给调用者 
	def __radd__(self,data):	#+=
		return CPoint([self.data[0]+data[0],self.data[1]+data[1]]) #用v创建一个新的对象返回给调用者 
	def __sub__(self,data):		#-
		return CPoint([self.data[0]-data[0],self.data[1]-data[1]]) #用v创建一个新的对象返回给调用者 
	def __rsub__(self,data):	#-=
		return CPoint([self.data[0]-data[0],self.data[1]-data[1]]) #用v创建一个新的对象返回给调用者 
	def __getitem__(self,number=0):	#xy[]
		return self.data[number]
	def _repr__(self):			#print
		return ("x:%d,y:%d" %(self.data[0],self.data[1]))
	def __str__(self):
		return ("x:%d,y:%d" %(self.data[0],self.data[1]))
	def __getattr__(self,attrname):	#xy.x xy.y
		if attrname == 'x' or attrname == 'X':
			return self.data[0]
		if attrname == 'y' or attrname == 'Y':
			return self.data[1]
		pass
	# def __setattr__(self,attrname,value):
	# 	if attrname == 'x' or attrname == 'X':
	# 		self.data[0]=value
	# 		pass
	# 	if attrname == 'y' or attrname == 'Y':
	# 		self.data[1]=value
	# 		pass
	# 	pass
