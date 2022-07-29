""" Methods intended to encode/decode video using simple opencv dependencies (unless specified). Code was written by
    Brett Nelson, Lawrence Berkeley National Lab and UC Berkeley.
    """

import os

os.chdir('../')
import cv2


# public functions
# simple interface: set video folder for decode, check folder for any video files related to file type

# Load, re-code frame by frame, save in folder


def mkdir(video_path):
    r = True
    if os.path.exists(video_path):
        os.mkdir(video_path + '/new_videos/')
    else:
        print('no directory found to store new videos')
        r = False
    new_video_path = video_path+'/new_videos/'
    return r, new_video_path


def get_video_from_path(video_path, conditions):
    video_file_names = []
    for files in os.listdir(video_path):
        for condition in conditions:
            if condition in files:
                video_file_names.append(files)
    return video_file_names


def uptake_and_recode_video_file(video_path_vector, output_path, new_conditions, ffmpeg=False, resize=False):
    for files in video_path_vector:
        try:
            cap = cv2.VideoCapture(files)
        except:
            raise AssertionError(" File does not exist or wrong format has been specified. ")
        video_fps = cap.get(cv2.CAP_PROP_FPS),
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        # Initialize video writer
        if resize:
            output_path = [output_path + '1' + str(new_conditions), output_path + '2' + str(new_conditions),
                           output_path + '3' + str(new_conditions)]
        if ffmpeg:  # ffmpeg implementation
            pass
        elif resize:
            fourcc = cv2.VideoWriter_fourcc(*str(new_conditions))
            writer = [cv2.VideoWriter(output_path[0], fourcc, video_fps, (int(width) / 3, int(height))),
                      cv2.VideoWriter(output_path[1], fourcc, video_fps, (int(width) / 3, int(height))),
                      cv2.VideoWriter(output_path[2], fourcc, video_fps, (int(width) / 3, int(height)))]
        else:
            fourcc = cv2.VideoWriter_fourcc(*str(new_conditions))  # set new conditions for encoding
            writer = cv2.VideoWriter(output_path, fourcc, video_fps, (int(width), int(height)))
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if resize:
                for i, writers in enumerate(writer):
                    writers.write(frame[:, ((i - 1) * width) / 3:(width * i) / 3, :])
            else:
                writer.write(frame)
        # release and destroy windows
        if resize:
            for writers in writer:
                writers.release()
        else:
            writer.release()
        cap.release()
        return


