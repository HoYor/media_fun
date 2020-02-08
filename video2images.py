# coding=utf-8
 
import os
import cv2
 
videos_src_path = "./"
video_formats = [".mp4", ".mov"]
frames_save_path = "./"
width = 544/4
height = 960/4
time_interval = 5
 
 
def videos2frame(video_src_path, formats, frame_save_path, frame_width, frame_height, interval):
    """
    将视频按固定间隔读取写入图片
    :param video_src_path: 视频存放路径
    :param formats:　包含的所有视频格式
    :param frame_save_path:　保存路径
    :param frame_width:　保存帧宽
    :param frame_height:　保存帧高
    :param interval:　保存帧间隔
    :return:　帧图片
    """
    videos = os.listdir(video_src_path)
 
    def filter_format(x, all_formats):
        if x[-4:] in all_formats:
            return True
        else:
            return False
 
    videos = filter(lambda x: filter_format(x, formats), videos)
 
    for each_video in videos:
        each_video_name = each_video[:-4]
        if not os.path.exists(frame_save_path + each_video_name):
            os.mkdir(frame_save_path + each_video_name)
        each_video_save_full_path = os.path.join(frame_save_path, each_video_name) + "/"
        each_video_full_path = os.path.join(video_src_path, each_video)
        video2frame(each_video_full_path,each_video,each_video_save_full_path, frame_width, frame_height, interval)

def video2frame(each_video_full_path,each_video,each_video_save_full_path, frame_width, frame_height, interval,name_strategy = 0):
    print "正在读取视频：", each_video
    cap = cv2.VideoCapture(each_video_full_path)
    frame_index = 0
    frame_count = 0
    if cap.isOpened():
        success = True
    else:
        success = False
        print("读取失败!")

    while(success):
        success, frame = cap.read()
        if not success:
            break
        print "---> 正在读取第%d帧:" % frame_index, success

        if frame_index % interval == 0:
            resize_frame = cv2.resize(frame, (frame_width, frame_height), interpolation=cv2.INTER_AREA)
            # cv2.imwrite(each_video_save_full_path + each_video_name + "_%d.jpg" % frame_index, resize_frame)
            if name_strategy == 0:
                name = frame_count
            elif name_strategy == 1:
                name = frame_count*2
            elif name_strategy == 2:
                name = frame_count*2+1
            else:
                name = frame_count
            cv2.imwrite(each_video_save_full_path + "%d.jpg" % name, resize_frame)
            frame_count += 1

        frame_index += 1
    if 'cap' in vars():
        cap.release()
 
if __name__ == '__main__':
    video2frame(videos_src_path, video_formats, frames_save_path, width, height, time_interval)
    # video2frame('source1.mp4','source1.mp4','twoVideos/',544,960,1)
