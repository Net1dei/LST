import os
from utils_cv.model import *
from utils_cv.args import PATH_TO_FOLDER_WITH_VIDEOS
from utils_cv.utils import delete_files_in_folder

names_videos=[f for f in os.listdir(PATH_TO_FOLDER_WITH_VIDEOS)]
path=PATH_TO_FOLDER_WITH_VIDEOS+names_videos[0]
#delete_files_in_folder('images')
analise_video2(path)
#analise_stream('rtsp://admin:A1234567@188.170.176.190:8028/Streaming/Channels/101?transportmode=unicast&profile=Profile_1')