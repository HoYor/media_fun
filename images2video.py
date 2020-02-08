# -*- coding: UTF-8 -*-
import os
import cv2

# 按照名字数字大小排序
def sortByNum(fileName1,fileName2):
	if fileName1.endswith('.jpg') and fileName2.endswith('.jpg'):
		return cmp(int(fileName1[0:-4]),int(fileName2[0:-4]))
	else:
		return False

# 图片合成视频
def pics2video(path,size):
    filelist = os.listdir(path) #获取该目录下的所有文件名
    filelist.sort(cmp=sortByNum)

    '''
    fps:
    帧率：1秒钟有n张图片写进去
    '''
    fps = 60
    file_path = path+".mp4"#导出文件名
    fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')#不同视频编码对应不同视频格式（例：'I','4','2','0' 对应avi格式）

    video = cv2.VideoWriter( file_path, fourcc, fps, size )
 
    for item in filelist:
        print "写入",item
        if item.endswith('.jpg'):   #判断图片后缀是否是.jpg
            item = path + '/' + item
            img = cv2.imread(item)  #使用opencv读取图像，直接返回numpy.ndarray 对象，通道顺序为BGR ，注意是BGR，通道值默认范围0-255。
            video.write(img)        #把图片写进视频

    video.release() #释放

if __name__ == '__main__':
	pics2video("target",(2720,4800))
	# pics2video("twoVideos",(544,960))