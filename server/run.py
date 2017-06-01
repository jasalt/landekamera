import os
import sys

import schedule
import threading
import time
import datetime
from sh import echo, ffmpeg, ls

import timelapse
import uploader


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def upload_yesterday_ig():
    today = datetime.datetime.now().strftime("%y%m%d")
    yesterday = str(int(today) - 1)

    video = timelapse.jpgs_to_mp4("data/" + yesterday, "data/")
    uploader.instagram(video, yesterday)
    print("everything seems ok, should rm video now")
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

def print_help():
    print('''Usage: python run.py
                     --i             Run debug/interactive mode.
                     --instagram     Starts daily Instagram uploader job.
                     --camera        Starts taking timelapses.
                     --youtube       TODO upload files to Youtube for archival, remove after uploaded?
                     --loop          TODO delete oldest dir if less than 500MB space available on /

Ideally you could run:
    python run.py --camera --instagram [TODO --youtube --loop]
But currently better to test every single functionality on it's own process/tmux window.

''')

if "--i" in sys.argv:
    print("Dropping to debugger/interactive mode.")
    import ipdb; ipdb.set_trace()
    # upload_yesterday_ig()
    # exit(1)
    
if "--ig" in sys.argv:
    print("Starting daily instagram upload job.")
    schedule.every().day.at("03:00").do(upload_yesterday_ig)

    # TODO run threaded
    # schedule.every().day.at("03:00").do(run_threaded, upload_yesterday_ig)


if "--camera" in sys.argv:
    import camera
    print("Starting timelapse camera job.")
    camera.initialize()
    camera.take_photo()
    schedule.every(30).seconds.do(camera.take_photo)

if len(sys.argv) == 1:
    print_help()
    exit(1)
    
print("Starting wait for scheduled actions")
    
while True:
     schedule.run_pending()
     time.sleep(1)
