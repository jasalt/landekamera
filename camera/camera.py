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

    filename = timestamp + ".jpg"            
    
    # "data/day"
    # fswebcam -S 150 --frames 4 -r 1920x1080 --jpeg 85 --no-banner   --save $TEMP_IMG

    # exiftool $TEMP_IMG -overwrite_original -GPSLatitudeRef=N -GPSLatitude=61.892220 -GPSLongitudeRef=E -GPSLongitude=25.655319 -GPSImgDirectionRef=T -GPSImgDirection=290 -Model="Logitech C930e"

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
    
