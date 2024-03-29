# coding=utf-8

from PIL import Image,ImageDraw,ImageFont
import os
import cv2
import numpy as np
import random
import image2char,images2video,video2images
import sys
reload(sys)
sys.setdefaultencoding('utf8')

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
# isMiniPic:是否按位置生成所有的小图
# TODO: 可以考虑不裁切小图
def picFather(pic,savePath,hidePic = None,isColorful = False,degree = 3,isNeedMiniPic = False):
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
	if isNeedMiniPic:
		saveFoldPath = savePath[:savePath.rindex('.')]+'/'
		os.system('mkdir {}'.format(saveFoldPath))
	for i in range(height):
		for j in range(width):
			gray = image2char.get_gray(*px[j,i])
			if isNeedMiniPic:
				miniImg = Image.new('RGB',(width,height))
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
					if isNeedMiniPic:
						miniImg.putpixel((n,m),(int(b),int(g),int(r)))
					img.putpixel((j*width+n,i*height+m),(int(b),int(g),int(r)))
			if isNeedMiniPic:
				miniImg.save('{}{}_{}.jpg'.format(saveFoldPath, i+1, j+1))
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
				print('[{},{}],'.format(i,j))
				for m in range(50):
					for n in range(50):
						savePic.putpixel((j*50+m,i*50+n),sourcePic[m,n])
	savePic.save(savePath)


# 用多张图片写字
# direction: 0(从左到右),1(从上到下)
def picWords(picDir,savePath,words,direction,writePosition=True):
	sourcePics = []
	os.mkdir('output/{}'.format(words))
	for pic in os.listdir(picDir):
		if pic.endswith('.png') or pic.endswith('.jpg') or pic.endswith('.jpeg'):
			fullPath = '{}/{}'.format(picDir, pic)
			im = Image.open(fullPath)
			width = im.size[0]
			height = im.size[1]
			if width > height:
				resizeWidth = 50
				resizeHeight = 50*height/width
			else:
				resizeHeight = 50
				resizeWidth = 50*width/height
			if writePosition:
				# 稍微存大一点
				im = im.resize((resizeWidth*2, resizeHeight*2),Image.ANTIALIAS)
				im.save('output/{}/{}'.format(words, pic))
			else:
				im = im.resize((resizeWidth, resizeHeight),Image.ANTIALIAS)
			sourcePics.append([im.load(), resizeWidth, resizeHeight])
	if len(sourcePics) == 0:
		print("没有图片")
		return
	# 建一个画布写字
	if direction == 0:
		text_canvas_width = 40*len(words)
		text_canvas_height = 50
	else:
		text_canvas_height = 40*len(words)
		text_canvas_width = 50
	array = np.ndarray((text_canvas_height, text_canvas_width, 3), np.uint8)
	array[:,:,0] = 255
	array[:,:,1] = 255
	array[:,:,2] = 255
	image = Image.fromarray(array)
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype("song.otf", 30, encoding="utf-8")
	if direction == 0:
		for index, word in enumerate(words):
			draw.text((8+36*index, 2), word, (0,0,0), font)
	else:
		for index, word in enumerate(words):
			draw.text((10, 36*index), word, (0,0,0), font)
	# image.save('text{}.png'.format(direction))
	# 建一个画布用图片写字
	newWidth = text_canvas_width * 50
	newHeight = text_canvas_height * 50
	wordPic = image.load()
	savePic = Image.new('RGB',(newWidth,newHeight),color=(255,255,255))
	if writePosition:
		writePositionStr = ''
	for i in range(text_canvas_height):
		if writePosition:
			writePositionStr += '['
		for j in range(text_canvas_width):
			gray = image2char.get_gray(*wordPic[j,i])
			if gray < 50:
				if writePosition:
					writePositionStr += '[{},{}],'.format(i,j)
					continue
				sourcePicArr = sourcePics[random.randint(0, len(sourcePics)-1)]
				sourcePic = sourcePicArr[0]
				sourcePicWidth = sourcePicArr[1]
				sourcePicHeight = sourcePicArr[2]
				offsetX = 0
				offsetY = 0
				if sourcePicWidth != 50:
					offsetX = (50-sourcePicWidth)/2
				if sourcePicHeight != 50:
					offsetY = (50-sourcePicHeight)/2
				for m in range(sourcePicWidth):
					for n in range(sourcePicHeight):
						savePic.putpixel((j*50+offsetX+m,i*50+offsetY+n),sourcePic[m,n])
		if writePosition:
			writePositionStr += '],\n'
	if writePosition:
		with open('{}.txt'.format(words), 'w') as wpf:
			wpf.write(writePositionStr)
	else:
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


# 边缘检测
def findImageEdge(img_path):
    from PIL import Image, ImageFilter
    with open(img_path,'rb') as imgf:
        image_handler = Image.open(imgf)
        # 边缘检测
        image_handler = image_handler.convert("L")
        image_handler = image_handler.filter(ImageFilter.FIND_EDGES)
		# 保存边缘检测的图
        # image_handler.save("edge.png")
	edge_width = image_handler.size[0]
	edge_height = image_handler.size[1]
	edge_image = image_handler.load()
	save_pic = Image.new('RGB',(edge_width,edge_height),color=(255,255,255))
	for i in range(edge_width):
		for j in range(edge_height):
			gray = edge_image[j,i]
			if gray > 50:
				print('[{},{}],'.format(j, i))
				save_pic.putpixel((j,i), (255, 0, 0))
	save_pic.save('edge.png')


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
	# picFather("source/source4.jpg","output/output15.jpg",isColorful=True,degree=1,isNeedMiniPic=True)
	# 两张图片融合
	# mergePic("source/source3.jpg","source/source4.jpg","output/output15.jpg",degree=3,isColorful=True,isLtr=False)
	# mergeVideo("source1.mp4","source2.mp4")
	# picWord("source/source4.jpg","output/output14.jpg",u"嵩")
	wordsArr = []
	for words in wordsArr:
		picWords("source/idol/{}".format(words),"output/output16.jpg",u"{}".format(words), 1)
	# findImageEdge("source/source1.jpg")

