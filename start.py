# coding=utf-8

from PIL import Image,ImageDraw,ImageFont
import os
import cv2
import numpy as np
import random
import image2char,images2video,video2images

# 视频所在目录
videos_src_path = "./"
# 视频格式
video_formats = [".mp4", ".mov"]
# 帧图片保存根目录
frames_save_path = "./"
# 帧图片保存宽度
width = 544
# 帧图片保存高度
height = 960
# 帧图片截取间隔
time_interval = 3

# 图片的每个像素由原图片组成
# isColorful:是否彩色
# degree:彩色程度(1-5)
# TODO: 可以考虑不裁切小图
def picFather(pic,savePath,hidePic = None,isColorful = False,degree = 3):
	if degree < 1 or degree > 5:
		print 'degree取值范围为1-5'
		return
	im = Image.open(pic)
	width = im.size[0]
	height = im.size[1]
	colorWidth = width*degree/10
	colorHeight = height*degree/10
	if width*height>3000:
		print '图片尺寸太大'
		return
	img = Image.new('RGB',(width*width,height*height))
	px = im.load()
	if hidePic != None:
		hideIm = Image.open(hidePic)
		if width != hideIm.size[0] or height != hideIm.size[0]:
			print '隐藏的图和原图尺寸需要一致'
			return
		hidePx = hideIm.load()
		hideW = random.randint(0,width-1)
		hideH = random.randint(0,height-1)
	for i in range(height):
		for j in range(width):
			gray = image2char.get_gray(*px[j,i])
			for m in range(height):
				for n in range(width):
					if isColorful:
						if m<colorHeight or m>height-colorHeight or n<colorWidth or n>width-colorWidth:
							(b,g,r) = px[j,i]
						else:
							if hidePic != None and i == hideH and j == hideW:
								(b,g,r) = hidePx[n,m]
							else:
								(b,g,r) = px[n,m]
					else:
						if hidePic != None and i == hideH and j == hideW:
							(b,g,r) = hidePx[n,m]
						else:
							(b,g,r) = px[n,m]
						point = round(gray/255.0,2)
						b = b*point
						g = g*point
						r = r*point
					img.putpixel((j*width+n,i*height+m),(int(b),int(g),int(r)))
	img.save(savePath)

# 用一张图片写字
def picWord(pic,savePath,word):
	if word is None or len(word) > 1:
		print("只能写一个字")
		return
	im = Image.open(pic)
	width = im.size[0]
	height = im.size[1]
	if width != height:
		print("图片应该是正方形且不大于50")
		return
	if width != 50:
		im = im.resize((50, 50),Image.ANTIALIAS)
	# 建一个画布写字
	array = np.ndarray((50, 50, 3), np.uint8)
	array[:,:,0] = 255
	array[:,:,1] = 255
	array[:,:,2] = 255
	image = Image.fromarray(array)
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype("song.otf", 30, encoding="utf-8")
	draw.text((10, 2), word, (0,0,0), font)
	# 建一个画布用图片写字
	newWidth = 2500
	sourcePic = im.load()
	wordPic = image.load()
	savePic = Image.new('RGB',(newWidth,newWidth),color=(255,255,255))
	for i in range(50):
		for j in range(50):
			gray = image2char.get_gray(*wordPic[j,i])
			if gray < 50:
				for m in range(50):
					for n in range(50):
						savePic.putpixel((j*50+m,i*50+n),sourcePic[m,n])
	savePic.save(savePath)

# 融合图片，degree是融合程度，1-9，取值的具体效果自己看，isLtr:是否左右融合
def mergePic(pic1,pic2,savePath,degree = 8,isColorful = False,isLtr = False):
	if degree < 1 or degree > 9:
		print "degree取值范围为1-9"
		return
	im1 = Image.open(pic1)
	im2 = Image.open(pic2)
	width = im1.size[0]
	height = im1.size[1]
	if width != im2.size[0] or height != im2.size[1]:
		print "融合的两张图片尺寸需要一致"
		return
	px1 = im1.load()
	px2 = im2.load()
	for i in range(height):
		for j in range(width):
			if isColorful:
				(b1,g1,r1) = px1[j,i]
				(b2,g2,r2) = px2[j,i]
				if isLtr:
					b = ((degree-(degree-5)*2*j/width)*b2 + (10-degree+(degree-5)*2*j/width)*b1)/10
					g = ((degree-(degree-5)*2*j/width)*g2 + (10-degree+(degree-5)*2*j/width)*g1)/10
					r = ((degree-(degree-5)*2*j/width)*r2 + (10-degree+(degree-5)*2*j/width)*r1)/10
				else:
					b = ((10-degree)*b1+degree*b2)/10
					g = ((10-degree)*g1+degree*g2)/10
					r = ((10-degree)*r1+degree*r2)/10
				im1.putpixel((j,i) , (b,g,r))
			else:
				gray1 = image2char.get_gray(*px1[j,i])
				gray2 = image2char.get_gray(*px2[j,i])
				if isLtr:
					gray = ((degree-(degree-5)*2*j/width)*gray2 + (10-degree+(degree-5)*2*j/width)*gray1)/10
				else:
					gray = ((10-degree)*gray1+degree*gray2)/10
				im1.putpixel((j,i) , (gray,gray,gray))
	im1.save(savePath)

# pic1渐变成pic2,保存在saveDir目录下,frames是帧率
def pic1ShadePic2(pic1,pic2,saveDir,frames):
	im1 = Image.open(pic1)
	im2 = Image.open(pic2)
	width = im1.size[0]
	height = im1.size[1]
	saveImg = Image.new('RGB',(width,height),'white')
	px1 = im1.load()
	px2 = im2.load()
	if not os.path.exists(saveDir):
		os.mkdir(saveDir)
	for d in range(frames):
		print "正在生成第%d张..." % (d+1)
		for i in range(height):
			for j in range(width):
				(b1,g1,r1) = px1[j,i]
				(b2,g2,r2) = px2[j,i]
				percent = float(d)/(frames-1)
				b = int(b1 + (b2-b1)*percent)
				g = int(g1 + (g2-g1)*percent)
				r = int(r1 + (r2-r1)*percent)
				saveImg.putpixel((j,i) , (b,g,r))
		saveImg.save(saveDir+"/"+str(d)+".jpg")

# 颜色反转
def reversePic(openPath,savePath):
	img = Image.open(openPath)
	# img.point(lambda i:255-i)
	(width,height) = img.size
	px = img.load()
	for i in range(height):
		for j in range(width):
			(b,g,r) = px[j,i]
			img.putpixel((j,i) , (255-b,255-g,255-r))
	img.save(savePath)

def start():
	video2images.videos2frame(videos_src_path, video_formats, frames_save_path, width/4, height/4, time_interval)
	image2char.images2pics("source","target")
	images2video.pics2video("target",(width*2,height*2))

def start2():
	pic1ShadePic2("merge_item1.jpg","merge_item2.jpg","shade",100)
	images2video.pics2video("shade",(108,108))

# 融合两个视频
def mergeVideo(video1,video2):
	if not os.path.exists("twoVideos"):
		os.mkdir("twoVideos")
	video2images.video2frame(video1,video1,'twoVideos/',544,960,1,1)
	video2images.video2frame(video2,video2,'twoVideos/',544,960,1,2)
	images2video.pics2video("twoVideos",(544,960))

if __name__ == '__main__':
	# 图片转某些字符组成的图片（像素长宽乘积不大于10000）- 效果很差
	# image2char.image2charPic("source/source4.jpg","output/output5.jpg")
	# 图片转某些字符组成的文本文件（像素长宽乘积不大于10000）- 效果不太好
	# image2char.image2txt("source/source4.jpg","output/output.txt")
	# 图片转一个字符组成的图片（像素长宽乘积不大于10000）
	# image2char.image2pic("source/source4.jpg","output/output1.jpg",char="*")
	# 图片转字符图片（像素长宽乘积不大于10000）
	# image2char.image2picZN("source/source4.jpg","output/output6.jpg",isColorful=False,picString=u"我爱你",hideString="许嵩")
	# 图片颜色反转
	# reversePic("source/source1.jpg","output/output6.jpg")
	# 组成一张由小图构成的大图（像素长宽乘积不大于3000）
	# picFather("source/source4.jpg","output/output12.jpg",isColorful=False,degree=1,hidePic="source/source3.jpg")
	# 两张图片融合
	# mergePic("source/source3.jpg","source/source4.jpg","output/output15.jpg",degree=3,isColorful=True,isLtr=False)
	# mergeVideo("source1.mp4","source2.mp4")
	picWord("source/source4.jpg","output/output13.jpg",u"秀")