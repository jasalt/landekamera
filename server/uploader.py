import sys
from sh import ffmpeg, rm, mediainfo
from time import strptime
import datetime

sys.path.insert(0, "./Instagram-API-python")

def get_length(video):
    '''Return video length in seconds.'''
    milliseconds = int(mediainfo("--Output=General;%Duration%", video))
    seconds = milliseconds // 1000.0
    return seconds

def make_thumbnail(video):
    ''' Save a thumnail of video from middle of it as "thumbnail.jpg".
    TODO save as videopath/thumbnail.jpg?
    # TODO add date to thumbnail = weather?
    ffmpeg -y -ss 00:00:20 -i video -vframes 1 thumbnail.jpg _err=uploader.log'''
    
    # get duration in form "00:00:20"
    len_seconds = get_length(video)
    len_seconds = len_seconds / 2  # take thumbnail from middle of the video
    
    time_str = str(datetime.timedelta(seconds=len_seconds))
    if (len(time_str) == 7):
        time_str = "0" + time_str  # add zero to string
    elif (len(time_str) != 8):
        raise ValueError("Video length is probably over 24h which is not supported.")

    print("Taking thumbnail from position " + time_str)
    
    ffmpeg("-y", "-ss", time_str, "-i", video, "-vframes", "1", "thumbnail.jpg", _err="uploader.log")
    
    return "thumbnail.jpg"

def instagram(video):
    from InstagramAPI import InstagramAPI
    InstagramAPI = InstagramAPI("landekamera", "***REMOVED***")
    print("Uploading video " + video + " to Instagram.")
    InstagramAPI.login() # login

    print("Logged in.")

    thumbnail = make_thumbnail(video)
    
    print("Starting upload..")
    upload = InstagramAPI.uploadVideo(video, thumbnail, caption="Testing 2")
    loginfo = InstagramAPI.LastJson # last response JSON
    print(loginfo)

    rm(thumbnail)
    
    import ipdb; ipdb.set_trace()
    
