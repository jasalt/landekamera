import schedule 
import time
from sh import echo, ffmpeg, ls
import os
from ffmpeg import jpgs_to_mp4
import uploader


if not os.path.isfile("config.py"):
    print("You haven't set up config.py yet, check config_example.py for example.")

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

# uploader.instagram("data/testing/full-crop.mp4")

uploader.instagram("Instagram-API-Python/full-short.mp4")
# uploader.instagram(mp4)
    
# schedule.every().day.at("03:00").do(process-timelapses)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
