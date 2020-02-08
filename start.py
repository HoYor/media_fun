# coding=utf-8

from PIL import Image
import os
import cv2
import numpy as np
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

def test1():
	im = Image.open('1.png')
	width = im.size[0]
	height = im.size[1]
	print "size:",im.size
	print "format:",im.format
	print "mode:",im.mode
	print "info:",im.info
	px = im.load()
	for i in range(height):
		for j in range(width):
			print px[j,i]

def test2():
	img = np.zeros((512,512),np.uint8)+255
	cv2.putText(img,"test",(200,200),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2)
	cv2.imwrite("write.jpg",img)
	cv2.imshow('img', img)
	cv2.waitKey(5000)

# 图片的每个像素由原图片组成
# isColorful:是否彩色
# degree:彩色程度(1-10)
def picFather(pic,savePath,isColorful = False,degree = 4):
	im = Image.open(pic)
	width = im.size[0]
	height = im.size[1]
	colorWidth = width*degree/20
	colorHeight = height*degree/20
	if width*height>3000:
		print '图片尺寸太大'
		return
	img = Image.new('RGB',(width*width,height*height))
	px = im.load()
	for i in range(height):
		for j in range(width):
			gray = image2char.get_gray(*px[j,i])
			# print gray
			# continue
			for m in range(height):
				for n in range(width):
					if isColorful:
						if m<colorHeight or m>height-colorHeight or n<colorWidth or n>width-colorWidth:
							(b,g,r) = px[j,i]
						else:
							(b,g,r) = px[n,m]
					else:
						(b,g,r) = px[n,m]
						point = round(gray/255.0,2)
						b = b*point
						g = g*point
						r = r*point
					img.putpixel((j*width+n,i*height+m),(int(b),int(g),int(r)))
	img.save(savePath)

# 图片的每个像素由原图片组成，藏hidePic进去
def picFatherHidePic(pic,savePath,hidePic):
	im = Image.open(pic)
	hideIm = Image.open(hidePic)
	width = im.size[0]
	height = im.size[1]
	if width*height>3000:
		print '图片尺寸太大'
		return
	img = Image.new('RGB',(width*width,height*height))
	px = im.load()
	hidePx = hideIm.load()
	for i in range(height):
		for j in range(width):
			gray = image2char.get_gray(*px[j,i])
			# print gray
			# continue
			for m in range(height):
				for n in range(width):
					point = round(gray/255.0,2)
					if j == width-4 and i == height-10:
						(b,g,r) = hidePx[n,m]
					else:
						(b,g,r) = px[n,m]
					b = b*point
					g = g*point
					r = r*point
					img.putpixel((j*width+n,i*height+m),(int(b),int(g),int(r)))
	img.save(savePath)

# 把pic2和pic1左右融合，degree是融合程度，1-9，取值的具体效果自己看
def mergeLtrPic(pic1,pic2,savePath,degree = 8,isColorful = False):
	im1 = Image.open(pic1)
	im2 = Image.open(pic2)
	width = im1.size[0]
	height = im1.size[1]
	px1 = im1.load()
	px2 = im2.load()
	for i in range(height):
		for j in range(width):
			if isColorful:
				(b1,g1,r1) = px1[j,i]
				(b2,g2,r2) = px2[j,i]
				b = ((degree-(degree-5)*2*j/width)*b2 + (10-degree+(degree-5)*2*j/width)*b1)/10
				g = ((degree-(degree-5)*2*j/width)*g2 + (10-degree+(degree-5)*2*j/width)*g1)/10
				r = ((degree-(degree-5)*2*j/width)*r2 + (10-degree+(degree-5)*2*j/width)*r1)/10
				im1.putpixel((j,i) , (b,g,r))
			else:
				gray1 = image2char.get_gray(*px1[j,i])
				gray2 = image2char.get_gray(*px2[j,i])
				# gray = ((8-6*j/width)*gray2 + (2+6*j/width)*gray1)/10
				gray = ((degree-(degree-5)*2*j/width)*gray2 + (10-degree+(degree-5)*2*j/width)*gray1)/10
				im1.putpixel((j,i) , (gray,gray,gray))
	im1.save(savePath)

# 融合图片
def mergePic(pic1,pic2,savePath,degree = 8,isColorful = False):
	im1 = Image.open(pic1)
	im2 = Image.open(pic2)
	width = im1.size[0]
	height = im1.size[1]
	px1 = im1.load()
	px2 = im2.load()
	for i in range(height):
		for j in range(width):
			if isColorful:
				(b1,g1,r1) = px1[j,i]
				(b2,g2,r2) = px2[j,i]
				b = ((10-degree)*b1+degree*b2)/10
				g = ((10-degree)*g1+degree*g2)/10
				r = ((10-degree)*r1+degree*r2)/10
				im1.putpixel((j,i) , (b,g,r))
			else:
				gray1 = image2char.get_gray(*px1[j,i])
				gray2 = image2char.get_gray(*px2[j,i])
				gray = ((10-degree)*gray1+degree*gray2)/10
				im1.putpixel((j,i) , (gray,gray,gray))
	im1.save(savePath)

# pic1渐变成pic2,保存在saveDir目录下
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

def config(picTxt):
	image2char.picString = picTxt

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
	# config(u"小六")
	# start()
	# start2()
	# reversePic('nana2.jpg','write.jpg')
	# mergePic('merge_item1.jpg','merge_item2.jpg','merge.jpg',3,True)
	mergeVideo("source1.mp4","source2.mp4")
	# picFather('lyx2.jpg','write1.jpg',True,2)
	# picFatherHidePic('pic_father.jpg','write.jpg','pic_mother.jpg')
	# mergeLtrPic('merge_right.jpg','merge_left.jpg','merge.jpg',8,True)
	# for i in range(9):
	# 	mergeLtrPic('merge_right.jpg','merge_left.jpg','merge'+str(i+1)+'.jpg',i+1)