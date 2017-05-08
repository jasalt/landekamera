from sh import identify, fswebcam, v4l2-ctl
import os
import schedule
import time
import datetime

def initialize_camera():
    v4l2-ctl("-d", "0",
             "-c", "focus_auto=0",
             "-c", "focus_absolute=0",
             "-c", "white_balance_temperature_auto=0",
             "-c", "white_balance_temperature=6500")
    # v4l2-ctl("-d", "0", "-c", "focus_absolute=0")
    # v4l2-ctl("-d", "0", "-c", "white_balance_temperature_auto=0")
    # v4l2-ctl("-d", "0", "-c", "white_balance_temperature=6500")
    print("Camera settings initialized")

def calculate_deviation(image):
    deviation = str(identify('-format', ' \"%[standard-deviation]\"', image))
    return float(deviation[1:-1])  # strip quotes, convert to float

def image_is_dark(image):
    min_deviation = 850  # pretty much black with c930e
    deviation = calculate_deviation(image)

    if deviation < min_deviation:
        print("Image too dark. Deviation: %s, Limit: %s." % (deviation, min_deviation))
        return True

    print("Image not too dark. Deviation: %s, Limit: %s." % (deviation, min_deviation))
    return False


image_is_dark("out.jpg")
# if dark.. wait long?

# schedule every 30 seconds

def take_picture():
    now = datetime.datetime.now()
    timestamp = now.strftime("%y%m%d-%H%M%S")
    dirname = "data/%s/" %timestamp

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    filename = dirname + timestamp + ".jpg"    
    # "data/day"

    # Try HDR?
    # exposure_auto (menu)   : min=0 max=3 default=0 value=3
    # exposure_absolute (int)    : min=3 max=2047 step=1 default=250 value=3 flags=inactive
    
    fswebcam( "-S", "150",  # skip some frames for auto exposure 
              "--frames", "4",
              "-r", "1920x1080",
              "--jpeg", "88",
              "--no-banner",
              "--save", filename)

    if image_is_dark(filename):
        os.remove(filename)
        return
    
    exiftool(filename, "-overwrite_original", "-GPSLatitudeRef=N", "-GPSLatitude=61.892220", "-GPSLongitudeRef=E", "-GPSLongitude=25.655319", "-GPSImgDirectionRef=T", "-GPSImgDirection=290", "-Model=\"Logitech C930e\"")


def upload_dir(dir):
    # rsync
    print("TODO uploading directory %s to server" % dir)

def upload_previous_days():
    today = datetime.datetime.now().strftime("%y%m%d")
    dirs = os.listdir("data")
    for dir in dirs:
        if dir is not today:
            upload_dir("data/" + dir)
            

schedule.every(30).seconds.do(take_picture)
schedule.every().day.at("03:00").do(upload_previous_days)
schedule.every

while True:
    schedule.run_pending()
    time.sleep(1)
    
