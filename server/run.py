import os
import sys

import schedule
import threading
import time
import datetime
from sh import echo, ffmpeg, ls

import timelapse
import uploader

today = datetime.datetime.now().strftime("%y%m%d")

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def upload_yesterday_ig():
    yesterday = str(int(today) - 1)
    video = timelapse.jpgs_to_mp4("data/" + yesterday, "data/")
    uploader.instagram(video, "TESTMODE ON...")
    import ipdb; ipdb.set_trace()
    # If OK, remove video

def upload_s3():
    '''Convert all previous days to h265 and upload to Amazon S3 storage'''
    os.chdir(WORKDIR)
    for dirname in os.listdir(WORKDIR + "jpg"):
        try:
            jpgs_to_mp4(dirname)
        except:
            print("Problem processing dir " + dirname + " please check shell.log for errors.")
            
# mp4 = jpgs_to_mp4("data/jpg/20160505", "data/video/")
# uploader.instagram("data/video/20160505.mp4")
# uploader.instagram("data/testing/long-crop.mp4", "Long Cropped")

if len(sys.argv) == 1:
    print("Nothing to be done, dropping to interactive mode")
    #import ipdb; ipdb.set_trace()
    upload_yesterday_ig()
    # exit(1)
    
if "--ig" in sys.argv:
    # Create process for it?
    print("Starting daily instagram upload job.")
    # schedule.every().day.at("03:00").do(run_threaded, upload_yesterday_ig)
    schedule.every().day.at("03:00").do(upload_yesterday_ig)

if "--s3" in sys.argv:
    # schedule.every().day.at("05:00").do(upload_s3)
    print("Starting S3 upload job.")
    print("TODO process all into h265 video and upload to S3")

if "--camera" in sys.argv:
    import camera
    print("Starting timelapse camera job.")
    camera.initialize()
    camera.take_photo()
    schedule.every(30).seconds.do(camera.take_photo)
    
import ipdb; ipdb.set_trace()
    
while True:
     schedule.run_pending()
     time.sleep(1)
