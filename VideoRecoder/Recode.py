""" Methods intended to encode/decode video using simple opencv dependencies (unless specified). Code was written by
    Brett Nelson, Lawrence Berkeley National Lab and UC Berkeley.
    """

import os
import pdb

os.chdir('../')
import cv2


# public functions
# simple interface: set video folder for decode, check folder for any video files related to file type

# Load, re-code frame by frame, save in folder


def mkdir(video_path):
    r = True
    if os.path.exists(video_path):
        try:
            os.mkdir(video_path + 'new_videos/')
        except:
            pass
    else:
        print('no directory found to store new videos')
        r = False
    new_video_path = video_path + 'new_videos/'
    return r, new_video_path


def get_video_from_path(video_path, new_path, conditions):
    video_file_names = []
    new_path_names = []
    for files in os.listdir(video_path):
        for condition in conditions:
            if condition in files:
                video_file_names.append(str(video_path) + str(files))
                new_path_names.append(str(new_path) + str(files))
    return video_file_names, new_path_names


def uptake_and_recode_video_file(video_path_vector, output_path, new_conditions, ffmpeg=False, resize=False):
    for i, files in enumerate(video_path_vector):
        nf = output_path[i]
        try:
            cap = cv2.VideoCapture(files)
        except:
            raise AssertionError(" File does not exist or wrong format has been specified. ")
        video_fps = 60  # hard-code for now.
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

        # Initialize video writer
        if resize:
            output_path = [ + '1' + str(new_conditions), output_path + '2' + str(new_conditions),
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
            writer = cv2.VideoWriter(nf, fourcc, video_fps, (int(width), int(height)))
        while True:
            ret, frame = cap.read()
            if not ret:
                print('Done')
                break
            if resize:
                for ix, writers in enumerate(writer):
                    writers.write(frame[:, ((ix - 1) * width) / 3:(width * ix) / 3, :])
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


class Recode:
    def __int__(self):
        self.new_path, self.file_path, self.file_types, self.videos_in_file = None, None, None, None
        self.new_conditions = None
        self.get_path_var()
        self.get_conditions_var()
        self.get_new_conditions_var()
        print('Decoding videos! ')
        uptake_and_recode_video_file(self.videos_in_file, self.new_path, self.new_conditions)
        print('Decoding finished!')

    def get_path_var(self):
        self.file_path = input("Please enter file path for video file path: ")
        ere, self.new_path = mkdir(self.file_path)
        if ere:
            pass
        else:
            self.get_path_var()

    def get_conditions_var(self):
        self.file_types = input("Please enter extension of video you wish to cut: ")
        self.videos_in_file = get_video_from_path(self.file_path, self.file_types)
        if len(self.videos_in_file) > 0:
            print('Found videos.')
        else:
            self.get_conditions_var()

    def get_new_conditions_var(self):
        self.new_conditions = input("Please enter extension you wish to decode into:  ")
        try:
            cv2.VideoWriter_fourcc(*str(self.new_conditions))
        except:
            print('Incorrect file extension type passed to decoder! ')
            self.get_new_conditions_var()
