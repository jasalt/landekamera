from sh import identify, fswebcam, rsync
import sh
import os
import schedule
import time
import datetime

from config import rsync_target  # string eg "user@example.com:~/landekamera/server/data/jpg/"

def initialize_camera():
    v4l2ctl = sh.Command("v4l2-ctl")
    v4l2ctl("-d", "0",
             "-c", "focus_auto=0",
             "-c", "focus_absolute=0",
             "-c", "white_balance_temperature_auto=0",
             "-c", "white_balance_temperature=6500")
    # v4l2ctl("-d", "0", "-c", "focus_absolute=0")
    # v4l2ctl("-d", "0", "-c", "white_balance_temperature_auto=0")
    # v4l2ctl("-d", "0", "-c", "white_balance_temperature=6500")
    print("Camera settings initialized")

def calculate_deviation(image):
    deviation = str(identify('-format', ' \"%[standard-deviation]\"', image))
    return float(deviation[1:-1])  # strip quotes, convert to float

def picture_is_dark(picture):
    min_deviation = 850  # pretty much black with c930e
    deviation = calculate_deviation(picture)

    if deviation < min_deviation:
        print("Picture too dark. Deviation: %s, Limit: %s." % (deviation, min_deviation))
        return True

    print("Picture OK (not dark). Deviation: %s, Limit: %s." % (deviation, min_deviation))
    return False



# if dark.. sleep longer?
# schedule every 30 seconds

def take_picture():
    now = datetime.datetime.now()
    
    date = now.strftime("%y%m%d")
    dirname = "data/%s/" %date
    
    timestamp = date + "-" + now.strftime("%H%M%S")
    filename = dirname + timestamp + ".jpg"    

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    # Try HDR?
    # exposure_auto (menu)   : min=0 max=3 default=0 value=3
    # exposure_absolute (int)    : min=3 max=2047 step=1 default=250 value=3 flags=inactive

    print("Taking picture " + filename)
    
    fswebcam( "-S", "150",  # skip some frames for auto exposure 
              "--frames", "4",
              "-r", "1920x1080",
              "--jpeg", "88",
              "--no-banner",
              "--save", filename)

    if picture_is_dark(filename):
        os.remove(filename)  # don't save pictures that don't have any light
        return
    
#    exiftool(filename, "-overwrite_original", "-GPSLatitudeRef=N", "-GPSLatitude=61.892220", "-GPSLongitudeRef=E", "-GPSLongitude=25.655319", "-GPSImgDirectionRef=T", "-GPSImgDirection=290", "-Model=\"Logitech C930e\"")

def process_log(line):
    print(line)


def upload_dir(dir):
    print("Uploading directory %s to server." % dir)
    rsync("-avn", "--remove-source-files", "--ignore-existing", dir, rsync_target, _err=process_log, _out=process_log)


def upload_previous_days():
    today = datetime.datetime.now().strftime("%y%m%d")
    dirs = os.listdir("data")
    for dir in dirs:
        if dir is not today:
            # import pdb; pdb.set_trace()        
            upload_dir("data/" + dir)


# initialize_camera()            
# take_picture()
# schedule.every(30).seconds.do(take_picture)

upload_previous_days()

# schedule.every().day.at("03:00").do(upload_previous_days)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
    
