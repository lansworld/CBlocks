# -*- coding: utf-8 -*-
import pygame
from cpoint import *
from blockExt import *
import random
#import time

MIN_TIMER = 50 ##最大速度时延 50ms下降一格

class CFrame():

	def __init__(self,set_mode=SET_MODE,start_point=START_POINT,bg_color=FRAMECOLOR):
		self.m_mode=set_mode
		self.m_StartPoint=start_point
		self.m_Bg_Color=bg_color
		self.CurrentBlock=None
		self.NextBlock=None
		self.color_arry=[[0 for i in range(COL+2)] for i in range(ROW+2)] ##存放颜色区域数组,包括两个边界
		self.m_Level=0
		self.m_Speed=0
		self.m_Score=0
		self.pausestatus=False
		#print(self.color_arry)
		self.BASICFONT=None		#中间显示提示字体，大小18
		self.CENTERFONT=None	#中间显示提示字体，大小30
		self.gameStartFlag=False	
		self.screen=None

	def set_timer(self):
		#speed 处理方法 通过时间常数进行控制 时延=1000ms/level(1~30) * 2  2000ms~66.6ms
		#SetTimer(100,1000-50*pDoc->m_Speed,NULL);
		timer=int(1000-50*self.m_Speed)
		if timer <= MIN_TIMER:	#最大速度后不在增加速度,避免有负速度
			timer = MIN_TIMER
		print("timer:",timer)
		pygame.time.set_timer(pygame.USEREVENT,timer)	#设置自动事件
	def clear_timer(self):
		#speed 处理方法 通过时间常数进行控制 时延=1000ms/level(1~30) * 2  2000ms~66.6ms
		pygame.time.set_timer(pygame.USEREVENT,0)	#设置自动事件

	def gameover(self):
		self.clear_timer()
		print("gameover")
		#self.__init__(SET_MODE,START_POINT,FRAMECOLOR)  #初始化变量
		self.gameStartFlag=False

		xy=CPoint(CENTER_POINT)
		self.CENTERFONT=pygame.font.SysFont('simsunnsimsun', 60)
		#fontObj3 = pygame.font.SysFont('宋体', 20)

		scoreSurf = self.CENTERFONT.render(u'游戏结束！' , True, WHITE,BG_COLOR)
		scoreRect = scoreSurf.get_rect()
		xy1=log2real_point(xy)
		#print(xy1)
		scoreRect.topleft = (xy1)
		self.screen.blit(scoreSurf, scoreRect)

	def Display(self,color=FRAMECOLOR):
		pygame.init()
		self.screen = pygame.display.set_mode((self.m_mode))
		self.screen.fill(self.m_Bg_Color)	##用背景色填充整个屏幕
		pygame.display.set_caption("CBlocks")
		pygame.display.flip()
		return self.screen

		#drawRect(self,color,xy)

	def drawPlayArea(self):#按照颜色数组重画整个积木区域
		print("drawPlayArea...")
		xy=log2real_point([1,1])  #从1,1,开始画，画一个大黑框
		pygame.draw.rect(self.screen,BG_COLOR,[xy[0],xy[1],BLOCK_SIZE*COL,BLOCK_SIZE*ROW],0)
		#print(self.color_arry)
		for x in range(1,ROW+1):
			for y in range(1,COL+1):
				color=self.color_arry[x][y]
				if color == color2int(BG_COLOR) or color == color2int(FRAMECOLOR): 
					#print("null:",x,y,color)
					pass
				else:
					#print("area:",x,y,color,color2int(color))
					startPoint=log2real_point([y,x])
					pygame.draw.rect(self.screen,color2int(color),[startPoint[0],startPoint[1],BLOCK_SIZE,BLOCK_SIZE],0)
					#pygame.draw.rect(self.screen, color2int(color), [x,y,BLOCK_SIZE,BLOCK_SIZE],0)

	def drawPreviewArea(self):
		#预览区域
		xy=log2real_point([PREVIEW_POINT[0]-2,PREVIEW_POINT[1]-2])
		pygame.draw.rect(self.screen,BG_COLOR,[xy[0],xy[1],BLOCK_SIZE*5,BLOCK_SIZE*5],0)

	def drawBorder(self):
		#背景区域
		xy=log2real_point([1,1])  #从1,1,开始画，4个边框不用
		pygame.draw.rect(self.screen,BG_COLOR,[xy[0],xy[1],BLOCK_SIZE*COL,BLOCK_SIZE*ROW],0)
		for x in range(0,ROW+2):
			for y in range(0,COL+2):
				#print(i,j,color2int(BG_COLOR))
				if x == 0 or x == ROW+1 or y == 0 or y==COL+1:  #是边框
					self.color_arry[x][y]=color2int(FRAMECOLOR)
				else:
					self.color_arry[x][y]=color2int(BG_COLOR)	#是游戏区域
		# print(self.color_arry)
		# exit(0)

	def drawStatus(self):
		xy=CPoint(TEXT_POINT)
		self.BASICFONT=pygame.font.Font('freesansbold.ttf', 18)

		scoreSurf = self.BASICFONT.render('Score: %d' % self.m_Score, True, TEXTCOLOR,FRAMECOLOR)
		scoreRect = scoreSurf.get_rect()
		xy1=log2real_point(xy)
		#print(xy1)
		scoreRect.topleft = (xy1)
		self.screen.blit(scoreSurf, scoreRect)
		xy2=log2real_point(xy+SZ_D)
		#print(TEXT_POINT,xy,xy1,xy2)
		levelSurf = self.BASICFONT.render('Level: %d' % self.m_Level, True, TEXTCOLOR,FRAMECOLOR)
		levelRect = levelSurf.get_rect()
		levelRect.topleft = (xy2)
		self.screen.blit(levelSurf, levelRect)
		xy2=log2real_point(xy+SZ_D2)
		#print(TEXT_POINT,xy,xy1,xy2)
		levelSurf = self.BASICFONT.render('Speed: %d' % self.m_Speed, True, TEXTCOLOR,FRAMECOLOR)
		levelRect = levelSurf.get_rect()
		levelRect.topleft = (xy2)
		self.screen.blit(levelSurf, levelRect)


	def getRandomBlock(self):
		block=random.choice(CBlockExtLists)
		#print("getRandomBlock",block)
		obj_block1=CBlocksExt(self.screen,self.color_arry,SZ_0,block[1],block[0])
		print("New Block :",block[2],block[1])
		#one block test
		# obj_block1=CBlocks(self.screen,self.color_arry,SZ_0,RED)
		return obj_block1

	def gameStart(self):
		self.gameStartFlag=True
		self.color_arry=[[0 for i in range(COL+2)] for i in range(ROW+2)] ##存放颜色区域数组,包括两个边界
		self.m_Level=0
		self.m_Speed=0
		self.m_Score=0
		self.screen=self.Display(FRAMECOLOR)
		self.drawBorder()
		self.drawStatus()
		self.drawPreviewArea()
		self.CurrentBlock=self.getRandomBlock()
		self.CurrentBlock.PreView()
		self.CurrentBlock.Start()
		self.NextBlock=self.getRandomBlock()
		self.NextBlock.PreView()
		self.set_timer()	#设置自动事件开始

	def Pause(self):
		if self.pausestatus :
			self.pausestatus=False
			self.set_timer()
		else:
			self.pausestatus=True
			self.clear_timer()			
		print("Pause...")

def main():
	#log2real_point(SZ_0)
	#exit(0)

	cf=CFrame(SET_MODE,START_POINT,FRAMECOLOR)
	# cf.gameover()
	# exit()
	cf.gameStart()


	#pygame.time.set_timer(obj_block1.MoveDown(),5)
	#obj_block1=CBlocksExt(screen,SZ_0,COLOR4,BLOCK_T)
	#obj_block1.PreView()
	
	#speed 处理方法 通过时间常数进行控制 时延=1000ms/level(1~30) * 2  2000ms~66.6ms
	pygame.key.set_repeat(KEY_REPEAT_TIME)  #设置重复按键时延，默认100ms
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
			if not cf.pausestatus and cf.gameStartFlag:
				if event.type == pygame.KEYDOWN and not cf.pausestatus and (event.key == pygame.K_DOWN or event.key == pygame.K_s):
					cf.CurrentBlock.MoveDown()
				if event.type == pygame.KEYDOWN and not cf.pausestatus and (event.key == pygame.K_UP or event.key == pygame.K_w):
					cf.CurrentBlock.Rotated()	#上键等于旋转
				if event.type == pygame.KEYDOWN and not cf.pausestatus and (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
					cf.CurrentBlock.MoveRight()
				if event.type == pygame.KEYDOWN and not cf.pausestatus and (event.key == pygame.K_LEFT or event.key == pygame.K_a):
					cf.CurrentBlock.MoveLeft()
				if event.type == pygame.KEYDOWN and not cf.pausestatus and (event.key == pygame.K_SPACE ):
					cf.CurrentBlock.Rotated()
			if event.type == pygame.KEYDOWN and (event.key == pygame.K_p ):
				cf.Pause()
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				cf.clear_timer()
				pygame.quit()
				sys.exit()
			#print(event)
			if not cf.gameStartFlag and event.type == pygame.KEYDOWN:	#游戏结束，按任意键重新开始
				#cf.gameStartFlag=True
				cf.gameStart()

			if event.type == pygame.USEREVENT:	#自动下降事件
				if not cf.CurrentBlock.MoveDown():	#到底了，需要判断是否有删除
					delLine = cf.CurrentBlock.deleteLines()
					if delLine > 0 :	#有删除行
						#print("delLine:%d,score:%d,level:%d" %(delLine,cf.m_Score,cf.m_Level))
						cf.m_Score+=((delLine*2)*100-100)
						if int(cf.m_Score/1000) > cf.m_Level:
							cf.m_Level=int(cf.m_Score/1000)
							cf.m_Speed += 1
							cf.set_timer()
						cf.drawStatus()
						cf.drawPlayArea()	#如果有删除，则需要重画整个区域
					else:
						pass
					#print("next block start...")
					#del cf.CurrentBlock 	#销毁原对象
					cf.CurrentBlock=cf.NextBlock
					s=cf.CurrentBlock.Start()
					if s==False:
						cf.gameover()
						break
					cf.drawPreviewArea()	#准备第二个实例对象
					cf.NextBlock=cf.getRandomBlock()
					cf.NextBlock.PreView()
				else:
					pass

		#pygame.draw.rect(screen,COLOR1,[80,150,20,20],0)
		#pygame.draw.circle(screen,COLOR0,[100,100],30,0)
		#pygame.draw.rect(screen,

		pygame.display.flip()

if __name__ == '__main__':
	#try:
	main()
	#except:
		#pygame.quit()
		#main()	
	#	pass		