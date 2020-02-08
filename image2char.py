# coding=utf-8

import os
from PIL import Image,ImageDraw,ImageFont
import cv2
import numpy as np

# ascii_char = list('''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1\{\}[]?-_+~<>i!lI;:,"^`'. ''')
ascii_char =  list('#8XOHLTI)i=+;:,. ')
scale = 10
# scale = 10
# picString = u"我爱你"
picString = u"这是我女朋友，我把她的名字藏在了里面，找到的朋友给你做一张这样的图"

# 得到颜色对应灰度的字符
def get_char(r, g, b, alpha = 256):
	if alpha == 0:
		return ' '
	length = len(ascii_char)
	gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
	unit = (256.0 + 1) / length
	return ascii_char[int(gray / unit)]

# 得到灰度
def get_gray(r, g, b):
	return int(0.2126 * r + 0.7152 * g + 0.0722 * b)

# 把openPath图片转换成字符图片
def image2pic(openPath,savePath):
	im = Image.open(openPath)
	width = im.size[0]
	height = im.size[1]
	# print "width:",width
	# print "height:",height
	# return
	img = np.zeros([height*scale,width*scale],np.uint8)+255
	px = im.load()
	for i in range(height):
		for j in range(width):
			gray = get_gray(*px[j,i])
			cv2.putText(img,"*",(j*scale,i*scale),cv2.FONT_HERSHEY_SIMPLEX,0.5,(gray,gray,gray),1)
	# compress = cv2.resize(img, (width,height), interpolation=cv2.INTER_AREA)
	cv2.imwrite(savePath,img)
	# cv2.imshow('img', img)

# 把openPath图片转换成中文字符图片
def image2picZN(openPath,savePath):
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
	for i in range(height):
		for j in range(width):
			gray = get_gray(*px[j,i])
			draw.text((j*scale, i*scale), picString[curPicStringIndex], (gray,gray,gray), font)
			if curPicStringIndex+1 == picStringLen:
				curPicStringIndex = 0
			else:
				curPicStringIndex = curPicStringIndex+1
	image.save(savePath)

def image2picZNColorful(openPath,savePath):
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
	for i in range(height):
		for j in range(width):
			(b,g,r) = px[j,i]
			if i == 100 and j == 60:
				draw.text((j*scale, i*scale), u"江", (b,g,r), font)
			elif i==100 and j== 61:
				draw.text((j*scale, i*scale), u"娜", (b,g,r), font)
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
	# images2pics("source","target")
	# image2txt()
	# image2pic("1.jpg","write.jpg")
	picString = u"兰沅羲"
	# image2picZN("lyx.jpg","write.jpg")
	image2picZNColorful("lyx3.jpg","write.jpg")
	# mergePic("1.jpg","2.jpg","merge.jpg")