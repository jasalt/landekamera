import os

import schedule 
import time
from sh import echo, ffmpeg, ls

from ffmpeg import jpgs_to_mp4
import uploader

WORKDIR = "data/"

def process_timelapses():
    os.chdir(WORKDIR)
    for dirname in os.listdir(WORKDIR + "jpg"):
        try:
            jpgs_to_mp4(dirname)
        except:
            print("Problem processing dir " + dirname + " please check shell.log for errors.")
        
    # day to archive dir
    # week old days to s3 or removal?

# mp4 = jpgs_to_mp4("data/jpg/20160505", "data/video/")
# uploader.instagram("data/video/20160505.mp4")

# might need to crop ig video first.. ? no need.

# time limit! 1800 frames used at most. speed up by a factor with ffmpeg

# not working uploader.instagram("Instagram-API-python/vid.mp4")

# uploader.instagram("data/testing/long-crop.mp4")

# uploader.instagram("data/testi.mp4") # speedup not working? whole video not ok
# uploader.instagram("data/testing/long-crop.mp4") # not
# uploader.instagram("data/testing/short-crop.mp4")  # OK!
# uploader.instagram("Instagram-API-python/full-short.mp4") # ok! speedup ok! fullhd
# uploader.instagram("Instagram-API-python/full-crop.mp4") # ok when shortened speedup ok! 640
#uploader.instagram("data/testi.mp4") # ok when spedup at least, fullhd
uploader.instagram("data/video/20160505.mp4")

# uploader.instagram(mp4)
    
# schedule.every().day.at("03:00").do(process-timelapses)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
