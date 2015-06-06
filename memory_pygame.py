#!/usr/bin/python
import os, sys, time, math, random 
import pygame
from pygame.locals import *

'''---------------------------------------------------------
Author:		Chandra Nepali
Programe:	Memory game
Date:		June 6, 2015
Version:	1.0
---------------------------------------------------------'''

WIDTH = 800
HEIGHT = 600
score = 0
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.init()
pygame.font.init()

card_image = pygame.image.load('Cards.jpg')
card_image_back = pygame.image.load('backCard.jpg')

#-------------------------------------------------------------------------------
class Image:
	def __init__(self, idd, width, height, loc, sur):
		self.__id = idd
		self.__width = width
		self.__height = height
		self.__loc = loc
		self.__sur = sur

	def get_id(self): return self.__id
	def get_width(self): return self.__width
	def get_height(self): return self.__height
	def get_loc(self): return self.__loc
	def get_surface(self): return self.__sur

	def set_loc(self, loc): self.__loc = loc
#-------------------------------------------------------------------------------

class Grid:
	def __init__(self, idd, width, height, pos, img):
		self.__idd = idd
		self.__width = width
		self.__height = height
		self.__pos = pos
		self.__img = img

	def get_id(self): return self.__idd
	def get_width(self): return self.__width
	def get_height(self): return self.__height
	def get_pos(self): return self.__pos
	def get_image_obj(self): return self.__img

	def set_image_obj(self, img): self.__img = img
#------------------------------------------------------------------------------- 

def makeGrid(size):
	n = size[0]	# n x m grid: n -> number of rows, m-> number of columns
	m = size[1]

	width = 65 #img.get_width()
	height = 84 #img.get_height()

	space = 5
	padding_left = 40
	padding_right = 40
	padding_top = 10
	padding_bottom = 10

	# sheet size
	sheet_width = m*width + (m-1)*space
	sheet_height = n*height + (n-1)*space

	# available size
	aval_height = HEIGHT - padding_top - padding_bottom
	aval_width = WIDTH - padding_left - padding_right

	surface = pygame.Surface((int(sheet_width), int(sheet_height)))	
	surface.fill(WHITE)

	grids = []
	for i in range(0, n):
		for j in range(0, m):
			loc1 = j*(width + 5)
			loc2 = i*(height + 5)
			gr = Grid(i*m+j, width, height, [loc1, loc2], '') 
			grids.append(gr)
	#---------------------------------------------------

	return surface, grids
#-------------------------------------------------------------------------------

def getImage(card, back=False):
	global card_image_back
	if(back):
		sur = pygame.Surface((65, 84))
		card_image_back = pygame.transform.scale(card_image_back, (65, 84))
		sur.blit(card_image_back, (0, 0))
		img = Image(-1, 65, 84, 0, sur)
		return img
	else:
		n = int((card-1)/13) + 1
		num = (card-1) % 13 + 1
		
		x1 = 40 + (num-1)*65 + (num-1)*12.5
		x2 = 65

		y1 = 48 + (n-1)*84 + (n-1)*13
		y2 = 84	

		sur = pygame.Surface((65, 84))
		sur.blit(card_image, (0, 0), (x1, y1, x2, y2))
		img = Image((n-1)*13+num, 65, 84, 0, sur)
		return img
#-------------------------------------------------------------------------------

def showImage():
	it = iter(gList)
	l = 0
	for i in range(0, len(grids)/2):
		img = imgList[i]
		
		for k in range(0, 2):
			gd = grids[it.next()]
			surface.blit(img.get_surface(), gd.get_pos(), (0, 0, img.get_width(), img.get_height()) )
			displaySurface.blit(surface, (WIDTH-surface.get_width()-50, WIDTH/2-surface.get_width()/2-40))
			img.set_loc(gd.get_id())
			gd.set_image_obj(img)
#-------------------------------------------------------------------------------

def showBack():
	it = iter(gList)
	img = getImage(0, True)
	for i in range(0, len(grids)):
		surface.blit(img.get_surface(), grids[i].get_pos(), (0, 0, img.get_width(), img.get_height()) )
		displaySurface.blit(surface, (WIDTH-surface.get_width()-50, WIDTH/2-surface.get_width()/2-40))
#-------------------------------------------------------------------------------

def suffle():
	imgList = []
	for i in range(0, 52):
		img = getImage(card[i])
		imgList.append(img)

	return imgList
#-------------------------------------------------------------------------------

def init():
	imgList = suffle()
	surface, grids = makeGrid([nRows, nCols])
	g = [x for x in range(0, len(grids))]
	random.shuffle(g)
	return imgList, g, surface, grids
#-------------------------------------------------------------------------------

shownId = []
prev = -2
match = True
gId = -2
pId = -2
kdown = 0
def mouseStat(evt):
	global gId, pId, kdown
	global prev, shownId, match
	if(evt.type == pygame.MOUSEBUTTONDOWN and start == False):
		kdown = 1
		pos = pygame.mouse.get_pos()
		gId = getGridId(pos)
		pId = grids[gId].get_image_obj().get_id()
		if(gId >= 0): 
			surface.blit(grids[gId].get_image_obj().get_surface(), grids[gId].get_pos(), (0, 0, grids[gId].get_width(), grids[gId].get_height()) )
			displaySurface.blit(surface, (WIDTH-surface.get_width()-50, WIDTH/2-surface.get_width()/2-40))

			if(prev == -2): 
				prev = gId
			elif(pId == grids[prev].get_image_obj().get_id()): 
				shownId.append(prev) 
				shownId.append(gId)
				prev = -2
			elif(not pId == grids[prev].get_image_obj().get_id()):
				match = False
	elif(evt.type == pygame.MOUSEBUTTONUP and start == False and kdown == 1):
		if(not match):
			pygame.time.delay(200)
			img = getImage(0, True)
			surface.blit(img.get_surface(), grids[gId].get_pos(), (0, 0, grids[gId].get_width(), grids[gId].get_height()) )
			displaySurface.blit(surface, (WIDTH-surface.get_width()-50, WIDTH/2-surface.get_width()/2-40))

			surface.blit(img.get_surface(), grids[prev].get_pos(), (0, 0, grids[prev].get_width(), grids[prev].get_height()) )
			displaySurface.blit(surface, (WIDTH-surface.get_width()-50, WIDTH/2-surface.get_width()/2-40))
			prev = -2
			match = True
			kdown = 0
#-------------------------------------------------------------------------------

def getGridId(pos):
	for g in grids:
		width = g.get_width()
		height = g.get_height()
		idd = g.get_id()
		gPos = g.get_pos()
		x = gPos[0]
		y = gPos[1]

		x = x + WIDTH-surface.get_width()-50
		y = y + WIDTH/2-surface.get_width()/2-40

		if(pos[0] > x and pos[0] < x+width and pos[1] > y and pos[1] < y+height):
			return g.get_id()
	return -1
#-------------------------------------------------------------------------------

nRows = 3
nCols = 4

clock = pygame.time.Clock()
displaySurface = pygame.display.set_mode((WIDTH, HEIGHT))
displaySurface.fill(WHITE)
pygame.display.set_caption('Memory Game')
basicFont = pygame.font.SysFont('comicsansms', 16)
displaySurface.fill(WHITE)

card = [x for x in range(1, 53)]
random.shuffle(card)

start = True

startTime = time.time()
shBack = True

while True:
	#---------------------------------------------------
	if(start):
		global imgList, gList, surface, grids
		imgList, gList, surface, grids = init()
		start = False
	#---------------------------------------------------
	nowTime = time.time()

	if(nowTime-startTime < 4): showImage()
	elif(shBack): 
		showBack()
		shBack = False

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if(nowTime-startTime > 4): mouseStat(event)

	pygame.display.update()
	clock.tick(20)
