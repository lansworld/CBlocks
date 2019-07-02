# -*- coding: utf-8 -*-
import pygame
import sys
from cpoint import *
#from CFrame import *
#import image
#import ImageDraw
#from math import sin, cos, pi

BG_COLOR = (0x00,0x00,0x00)

##单个方块基础类
class CBlocks():
	#IDColor=BG_COLOR
	#xyPoint=SZ_0
	#screen=pygame.Surface()

	@classmethod
	def __init__(self,sc,color_arry,Point=SZ_0,Color=BG_COLOR):
		self.screen=sc     	#屏幕
		self.color_arry=color_arry
		self.xyPoint = CPoint(Point)  #方块中心当前逻辑坐标
		self.IDColor = Color  ##方块颜色
		self.preview_flag=True    #初始状态是预览状态
		#print(self.color_arry)
		#print(color_arry)

	def setAt(self,xy,color_id):
		#print("setAt:",xy,color2int(color_id))
		self.color_arry[xy[1]][xy[0]]=color2int(color_id)
	def getAt(self,xy):
		#c=self.color_arry[xy[1]][xy[0]]
		#print(xy[1],xy[0],c)
		return self.color_arry[xy[1]][xy[0]]

	def drawRect(self,xy,list_color):  #在逻辑坐标xy位置画一个矩形
		# if not self.preview_flag :	#如果不是预览模式，设置数组
		# 	self.setAt(xy,list_color)  #对应矩形位置把颜色设置在数组内
		startPoint=log2real_point(xy)
		pygame.draw.rect(self.screen,list_color,[startPoint[0],startPoint[1],BLOCK_SIZE,BLOCK_SIZE],0)
		#print(self.color_arry)

	def Display(self,color):
		self.drawRect(self.xyPoint,self.IDColor)
		if not self.preview_flag :	#如果不是预览模式，设置数组
			self.setAt(self.xyPoint,self.IDColor)  #对应矩形位置把颜色设置在数组内

		#pygame.draw.rect(self.screen,color,[startPoint[0],startPoint[1],BLOCK_SIZE,BLOCK_SIZE],0)
		#print(startPoint,endPoint)
	def Hide(self):
		self.drawRect(self.xyPoint,BG_COLOR)
		if not self.preview_flag :	#如果不是预览模式，设置数组
			self.setAt(self.xyPoint,BG_COLOR)  #对应矩形位置把颜色设置在数组内
	
	def arriveBorder(self,xy,xy_offset): #根据xy加上逻辑偏移量坐标后是否超界,超界返回true,否则返回false
		#zereturn False
		#new_xy=xy+xy_offset 
		c=self.getAt(xy+xy_offset)
		#return True
		if c != color2int(BG_COLOR) or c == color2int(FRAMECOLOR):
			#print("arriveborder:",xy+xy_offset,xy_offset,c)
			return True
		else:
			return False

	def PreView(self):
		self.preview_flag=True
		self.xyPoint=CPoint(PREVIEW_POINT)
		# print("PreView...",self.xyPoint,self.IDColor)
		self.Display(self.IDColor)
	#	self.preview_flag=False
		pass

	def Start(self):	#初始位置画积木，成功返回True，如果位置不是空，返回False
		self.Hide()
		self.xyPoint=CPoint(INIT_POINT)
		self.preview_flag=False	#设置开始模式
		if(self.getAt(self.xyPoint) == color2int(BG_COLOR)):
			self.Display(self.IDColor)
			return True
		else:
			return False	

	def MoveLeft(self):
		if self.arriveBorder(self.xyPoint,SZ_L):
			return False
		else:
			self.Hide()
			self.xyPoint+=SZ_L
			self.Display(self.IDColor)
			#print("MoveLeft")
			return True
	def MoveRight(self):
		if self.arriveBorder(self.xyPoint,SZ_R):
			return False
		else:
			self.Hide()
			self.xyPoint+=SZ_R
			self.Display(self.IDColor)
			return True

	def MoveDown(self):	#到底了则返回False，否则返回True积木下移一格
		if self.arriveBorder(self.xyPoint,SZ_D):	#到底了判断是否有删除行，如果有返回删除行数，没删除返回0
			#delline=self.deleteLines()
			return False
		else:
			self.Hide()
			self.xyPoint+=SZ_D
			self.Display(self.IDColor)
			#print("MoveDown")
			#return (False,0)
			return True
	def MoveUP(self):
		if self.arriveBorder(self.xyPoint,SZ_U):
			return False
		else:
			self.Hide()
			self.xyPoint+=SZ_U
			self.Display(self.IDColor)
			return True
			#print("MoveUP")
	def Run(self):
		#print("Run")
		return self.start()

	def Rotated(self):
		return True
		
	# def autoDown(self):
	# 	if self.arriveBorder(self.xyPoint,SZ_D):	#到底了判断是否有删除行，如果有返回删除行数，没删除返回0
	# 		delline=self.deleteLines(self.xyPoint[1])
	# 		return (True,delline)
	# 	else:
	# 		self.Hide()
	# 		self.xyPoint+=SZ_D
	# 		self.Display(self.IDColor)
	# 		#print("MoveDown")
	# 		return (False,0)

	def isFull(self,line):	#判断一行是否满了，满了触发消除行任务
		#print("isFull:",self.xyPoint,line,self.color_arry[line][1:COL+1])
		for i in range(1,COL+1):
			if self.color_arry[line][i] == color2int(BG_COLOR):
				return False
		return True
	def deleteLines(self):
		#lineno=xy[1]
		lineno=self.xyPoint[1]
		if self.isFull(lineno): #如果这行满了，则清理这行，上面所有行下移
			#print("###deleteLines...",lineno)
			i_row=lineno
			while i_row > 1 :	#清理这行，上面所有行下移
				#print(self.color_arry)
				self.color_arry[i_row]=self.color_arry[i_row-1]
				i_row -= 1 
			self.color_arry[1]=[color2int(FRAMECOLOR)]+ [0 for i in range(1,COL+1)]+[color2int(FRAMECOLOR)]	#首行设置为0
			return 1
		else:
			return 0
#@staticmethod


def main():
	#log2real_point(SZ_0)
	#exit(0)

	pygame.init()
	screen = pygame.display.set_mode((SET_MODE))
	screen.fill(BG_COLOR)
	pygame.display.set_caption("CBlocks")
	obj_block1=CBlocks(screen,SZ_0,COLOR4)
	obj_block1.PreView()
	obj_block1.Start()
	while True:
		for event in pygame.event.get():
			#为KEYDOWN和KEYUP
			# if event.type == pygame.KEYDOWN:  ##有按键
			# 	keys_pressed = pygame.key.get_pressed()
			# 	if keys_pressed[pygame.K_RIGHT]:
			# 		obj_block1.MoveRight()

			# keys_pressed = pygame.key.get_pressed()
			# 2.通过键盘常量，判断元组中键盘的值来确认按键是否被按下。  如果被按下按键对应的值为1。如：
			# if keys_pressed[pygame.K_RIGHT]:
			#      print（‘向右移动’）


			if event.type == pygame.KEYDOWN and (event.key == pygame.K_DOWN or event.key == pygame.K_s):
			#if event.type == pygame.K_DOWN or event.type == pygame.K_s:
				obj_block1.MoveDown()
			if event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_w):
				obj_block1.MoveUP()
			if event.type == pygame.KEYDOWN and (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
				obj_block1.MoveRight()
			if event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_a):
				obj_block1.MoveLeft()
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				sys.exit()
			#print(event)
		
		
		#pygame.draw.rect(screen,COLOR1,[80,150,20,20],0)
		#pygame.draw.circle(screen,COLOR0,[100,100],30,0)
		#pygame.draw.rect(screen,
		pygame.display.flip()



if __name__ == '__main__':
    main()