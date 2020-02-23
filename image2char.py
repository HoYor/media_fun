# coding=utf-8

import os
from PIL import Image,ImageDraw,ImageFont
import cv2
import numpy as np
import random

# ascii_char = list('''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1\{\}[]?-_+~<>i!lI;:,"^`'. ''')
ascii_char = list(u'#8XOHLTI)i=+;:,. ')
scale = 10

# 得到颜色对应灰度的字符
def get_char(r, g, b, alpha = 256, gray = None):
	if alpha == 0:
		return ' '
	length = len(ascii_char)
	if gray == None:
		gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
	unit = (256.0 + 1) / length
	return ascii_char[int(gray / unit)]

# 得到灰度
def get_gray(r, g, b):
	return int(0.2126 * r + 0.7152 * g + 0.0722 * b)

# 把openPath图片转换成某些字符组成的图片
def image2charPic(openPath,savePath,r = 0,g = 0,b = 0):
	im = Image.open(openPath)
	width = im.size[0]
	height = im.size[1]
	img = np.zeros([height*scale,width*scale],np.uint8)+255
	px = im.load()
	for i in range(height):
		for j in range(width):
			cv2.putText(img,get_char(*px[j,i]),(j*scale,i*scale),cv2.FONT_HERSHEY_SIMPLEX,0.5,(r,g,b),1)
	# compress = cv2.resize(img, (width,height), interpolation=cv2.INTER_AREA)
	cv2.imwrite(savePath,img)

# 把openPath图片转换成一个字符组成的图片
def image2pic(openPath,savePath,char="*"):
	im = Image.open(openPath)
	width = im.size[0]
	height = im.size[1]
	img = np.zeros([height*scale,width*scale],np.uint8)+255
	px = im.load()
	for i in range(height):
		for j in range(width):
			gray = get_gray(*px[j,i])
			cv2.putText(img,char,(j*scale,i*scale),cv2.FONT_HERSHEY_SIMPLEX,0.5,(gray,gray,gray),1)
	# compress = cv2.resize(img, (width,height), interpolation=cv2.INTER_AREA)
	cv2.imwrite(savePath,img)
	# cv2.imshow('img', img)

# 把openPath图片转换成由一段文字组成的图片，可以用来替代image2pic方法
def image2picZN(openPath,savePath,isColorful=False,picString=u"我爱你",hideString=""):
	im = Image.open(openPath)
	width = im.size[0]
	height = im.size[1]
	picStringLen = len(picString)
	curPicStringIndex = 0
	array = np.ndarray((height*scale, width*scale, 3), np.uint8)
	array[:,:,0] = 255
	array[:,:,1] = 255
	array[:,:,2] = 255
	image = Image.fromarray(array)
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype("song.otf", scale, encoding="utf-8")
	px = im.load()
	hideStartI = 0
	hideStartJ = 0
	if hideString != "":
		hideStartI = random.randint(0,height)
		hideStartJ = random.randint(0,width-len(hideString))
	for i in range(height):
		for j in range(width):
			if(isColorful):
				(b,g,r) = px[j,i]
			else:
				b=g=r = get_gray(*px[j,i])
			if hideString != "" and i == hideStartI and j >= hideStartJ:
				draw.text((j*scale, i*scale), hideString[0], (b,g,r), font)
				hideString = hideString[1:]
			else:
				draw.text((j*scale, i*scale), picString[curPicStringIndex], (b,g,r), font)
				if curPicStringIndex+1 == picStringLen:
					curPicStringIndex = 0
				else:
					curPicStringIndex = curPicStringIndex+1
	image.save(savePath)

# 把openPath图片转换成字符txt文件
def image2txt(openPath,savePath):
	im = Image.open(openPath)
	width = im.size[0]
	height = im.size[1]
	txt = ""
	px = im.load()
	for i in range(height):
		for j in range(width):
			txt += get_char(*px[j,i])
		txt += '\n'

	fobj=open(savePath,'w')
	fobj.write(txt)
	fobj.close()

# 把openDir文件夹下的图片全都转换成文字图片放到saveDir中
def images2pics(openDir,saveDir):
	filelist = os.listdir(openDir)
	if not os.path.exists(saveDir):
		os.mkdir(saveDir)
	for file in filelist:
		print "正在处理",file
		image2picZN(openDir+"/"+file,saveDir+"/"+file)

if __name__ == '__main__':
	pass