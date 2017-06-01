from sh import identify, fswebcam, rsync
import sh
import os
import schedule
import time
import datetime

def initialize():
    v4l2ctl = sh.Command("v4l2-ctl")
    focus = 0
    wb = 6500
    v4l2ctl("-d", "0",
             "-c", "focus_auto=0",
             "-c", "focus_absolute=" + str(focus),
             "-c", "white_balance_temperature_auto=0",
             "-c", "white_balance_temperature=" + str(wb))
    print("Camera settings initialized. Focus %s, White Balance %s" % (focus, wb))
    print("Exposure auto.")

def calculate_deviation(image):
    deviation = str(identify('-format', ' \"%[standard-deviation]\"', image))
    return float(deviation[1:-1])  # strip quotes, convert to float

def photo_is_dark(photo):
    min_deviation = 800  # pretty much black with c930e
    deviation = calculate_deviation(photo)

    if deviation < min_deviation:
        print("Photo too dark. Deviation: %s, Limit: %s." % (deviation, min_deviation))
        return True

    print("Photo OK (not dark). Deviation: %s, Limit: %s." % (deviation, min_deviation))
    return False


# schedule every 30 seconds

def take_photo():
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

    print("Taking photo " + filename)
    
    fswebcam( "-S", "150",  # skip some frames for auto exposure 
              "--frames", "4",
              "-r", "1920x1080",
              "--jpeg", "88",
              "--no-banner",
              "--save", filename, _out="camera.log", _err="camera.log")

    if photo_is_dark(filename):
        os.remove(filename)  # don't save photos that don't have any light
        return  # TODO sleep longer if dark?
    
#    exiftool(filename, "-overwrite_original", "-GPSLatitudeRef=N", "-GPSLatitude=61.892220", "-GPSLongitudeRef=E", "-GPSLongitude=25.655319", "-GPSImgDirectionRef=T", "-GPSImgDirection=290", "-Model=\"Logitech C930e\"")
