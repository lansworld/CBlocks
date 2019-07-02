# -*- coding: utf-8 -*-
from block import *
import time
#from CFrame import *

#形状定义
BLOCK_O=[
	[SZ_0,SZ_R,SZ_D,SZ_RD],
	[SZ_0,SZ_R,SZ_D,SZ_RD],
	[SZ_0,SZ_R,SZ_D,SZ_RD],
	[SZ_0,SZ_R,SZ_D,SZ_RD]];

BLOCK_I=[
	[SZ_0,SZ_L,SZ_R,SZ_R2],
	[SZ_0,SZ_U,SZ_D,SZ_D2],
	[SZ_0,SZ_L,SZ_R,SZ_R2],
	[SZ_0,SZ_U,SZ_D,SZ_D2]];

BLOCK_J=[
	[SZ_0,SZ_LU,SZ_L,SZ_R],
	[SZ_0,SZ_U,SZ_RU,SZ_D],
	[SZ_0,SZ_L,SZ_R,SZ_RD],
	[SZ_0,SZ_U,SZ_LD,SZ_D]];

BLOCK_L=[
	[SZ_0,SZ_L,SZ_RU,SZ_R],
	[SZ_0,SZ_U,SZ_D,SZ_RD],
	[SZ_0,SZ_L,SZ_LD,SZ_R],
	[SZ_0,SZ_LU,SZ_U,SZ_D]];

BLOCK_Z=[
	[SZ_0,SZ_L,SZ_D,SZ_RD],
	[SZ_0,SZ_U,SZ_L,SZ_LD],
	[SZ_0,SZ_L,SZ_D,SZ_RD],
	[SZ_0,SZ_U,SZ_L,SZ_LD]];

BLOCK_S=[
	[SZ_0,SZ_LD,SZ_D,SZ_R],
	[SZ_0,SZ_U,SZ_R,SZ_RD],
	[SZ_0,SZ_LD,SZ_D,SZ_R],
	[SZ_0,SZ_U,SZ_R,SZ_RD]];

BLOCK_T=[
	[SZ_0,SZ_L,SZ_U,SZ_R],
	[SZ_0,SZ_U,SZ_R,SZ_D],
	[SZ_0,SZ_R,SZ_D,SZ_L],
	[SZ_0,SZ_D,SZ_L,SZ_U]];


COLOR0=(0xff,0x00,0x33)
COLOR1=(0x00,0x33,0xff)
COLOR2=(0x33,0xff,0x00)
COLOR3=(0xff,0x00,0xff)
COLOR4=(0xff,0xff,0x00)
COLOR5=(0x00,0xff,0xff)
COLOR6=(0x99,0xff,0xff)
COLOR7=(0x99,0x99,0x99)

#方块数组
CBlockExtLists=[
	[BLOCK_O,COLOR0,'O'],
	[BLOCK_I,COLOR1,'I'],
	[BLOCK_J,COLOR2,'J'],
	[BLOCK_L,COLOR3,'L'],
	[BLOCK_Z,COLOR4,'Z'],
	[BLOCK_S,COLOR5,'S'],
	[BLOCK_T,COLOR6,'T']]

class CBlocksExt(CBlocks):
	def __init__(self,sc,color_arry,Point=SZ_0,Color=BG_COLOR,shape=BLOCK_S):
		#print("__init__ CBlocksExt!")
		super(CBlocksExt, self).__init__(sc,color_arry,Point,Color)
		self.screen=sc     	#屏幕
		self.color_arry=color_arry
		self.xyPoint = CPoint(Point)  #方块中心当前逻辑坐标
		self.IDColor = Color  ##方块颜色
		self.phases=shape  	#形状
		self.phase=0	#旋转初始状态

	def setAt(self,xy,color_id):
		#print(point,color2int(color_id))
		#self.color_arry[point[1]][point[0]]=color2int(color_id)
		for i in range(0,4) :
			xy1=xy+self.phases[self.phase][i]
			# super().setAt(xy1,color_id)
			#print("setAtExt:",i,xy,self.phases[self.phase][i],xy1,color2int(color_id))
			self.color_arry[xy1[1]][xy1[0]]=color2int(color_id)

	def arriveBorder(self,xy,xy_offset): #根据当前坐标，加上逻辑偏移量坐标后是否超界
#		#print(xy,xy_offset)
		isnull=0
		#if xy_offset == SZ_R :
		#print("setAt:",self.color_arry[1:4])
		self.setAt(self.xyPoint,BG_COLOR)
		#print("setAt_new:",self.color_arry[1:4])
		for i in range(0,4) :
			xy1=xy+self.phases[self.phase][i]
			if not super().arriveBorder(xy1,xy_offset):
				isnull+=1
		self.setAt(self.xyPoint,self.IDColor)
		#print("blockExt.arriveBorder:",isnull)
		if isnull == 4 :
			return False
		else:
			return True


	def Display(self,color):
		xy=self.xyPoint
		for i in range(0,4) :
			xy1=xy+self.phases[self.phase][i]
			self.drawRect(xy1,self.IDColor)
			if not self.preview_flag:
				self.setAt(xy,self.IDColor)

	def Hide(self):
		xy=self.xyPoint
		for i in range(0,4) :
			xy1=xy+self.phases[self.phase][i]
			self.drawRect(xy1,BG_COLOR)
		if not self.preview_flag :	#如果不是预览模式，设置数组
			self.setAt(xy,BG_COLOR)  #对应矩形位置把颜色设置在数组内

	def Rotated(self):
		##判断新位置是否可以旋转
		self.setAt(self.xyPoint,BG_COLOR)
		nextPhase=self.phase+1
		if nextPhase == 4 :
			nextPhase=0
		for i in range(0,4) :
			xy1=self.xyPoint+self.phases[nextPhase][i]
			if super().getAt(xy1) != color2int(BG_COLOR):
				#self.setAt(self.xyPoint,self.IDColor)
				return False
		self.setAt(self.xyPoint,self.IDColor)

		self.Hide()
		self.phase+=1
		if self.phase==4 :
			self.phase=0
		self.Display(self.IDColor)
		pass

	# def isFull(self):	#判断一行是否满了，满了触发消除行任务
	# 	xy = self.xyPoint
	# 	ret=0
	# 	lines=[]
	# 	for i in range(0,4) :
	# 		xy1=xy+self.phases[self.phase][i]
	# 		line = xy1[1]
	# 		if super().isFull(line):
	# 			lines.append(line)
	# 			ret+=1
	# 	return (ret,lines)

	def deleteLines(self):
		lines=[]
		for i in range(0,4) :
			xy1=self.xyPoint+self.phases[self.phase][i]
			if xy1[1] not in lines:
				lines.append(xy1[1]) 
			#blocklines1=set(lines)
			#print(lines)
		lines.sort()
		#blocklines=lines.sort()	 #去重，升序排序
		#print("blocklines:",lines)
		ret=0
		for lineno in lines:
			if super().isFull(lineno):
				#print("###deleteLines...",lineno,ret)
				i_row = lineno
				while i_row > 1:
					self.color_arry[i_row]=self.color_arry[i_row-1]
					i_row -= 1
				self.color_arry[1]=[color2int(FRAMECOLOR)]+ [0 for i in range(1,COL+1)]+[color2int(FRAMECOLOR)]
				ret+=1
			# print("17:",self.color_arry[17][1:COL+1])
			# print("18:",self.color_arry[18][1:COL+1])
			# print("19:",self.color_arry[19][1:COL+1])
			# print("20:",self.color_arry[20][1:COL+1])
		return ret


def main():
	print(CBlockExtLists[2][1])
	pass

if __name__ == '__main__':
    main()