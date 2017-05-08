import sys
import os
from sh import ffmpeg, rm, mediainfo, node
from time import strptime
import datetime

from config import ig_user, ig_password

sys.path.insert(0, "./Instagram-API-python")

def process_log(line):
    print(line)
    

def get_length(video):
    '''Return video length in seconds.'''
    milliseconds = int(mediainfo("--Output=General;%Duration%", video))
    seconds = int(milliseconds // 1000.0)
    return seconds

def make_thumbnail(video):
    ''' Save a thumnail of video from middle of it as "thumbnail.jpg".
    TODO save as videopath/thumbnail.jpg?
    # TODO add date to thumbnail = weather?
    ffmpeg -y -ss 00:00:20 -i video -vframes 1 thumbnail.jpg'''
    
    # get duration in form "00:00:20"
    len_seconds = get_length(video)
    len_seconds = len_seconds // 2  # take thumbnail from middle of the video
    
    time_str = str(datetime.timedelta(seconds=len_seconds))
    if (len(time_str) == 7):
        time_str = "0" + time_str  # add zero to string
    elif (len(time_str) != 8):
        import ipdb; ipdb.set_trace()
        raise ValueError("Video length is probably over 24h which is not supported.")

    print("Taking thumbnail from position " + time_str)
    
    ffmpeg("-y", "-ss", time_str, "-i", video, "-vframes", "1", "thumbnail.jpg", _err="uploader.log")
    return "thumbnail.jpg"

def prepare_video_to_instagram(video):
    '''Make sure the video length is max target_seconds. Speed it up otherwise.
    Eg. speed up by factor of 2:
    ffmpeg -i input.mkv -filter:v "setpts=0.5*PTS" output.mkv'''
    target_height = 640
    left_offset = 300
    
    vf_scale = "scale=-1:%s" % target_height  # 1920x1080 -> 1137x640
    vf_crop = ",crop=640:640:%s:0" % left_offset  # 640x640

    orig_len = get_length(video)
    target_seconds = 59
    if orig_len < target_seconds:
        print("Original length ok, skipping speedup. %s is under target maximum %s s."
              % (orig_len, target_seconds))
        vf_slowdown = ""
    else:
        slowdown_factor = float(target_seconds)/float(orig_len)
        print("Too long video. Speeding up by slowing down video by factor %0.3f"%slowdown_factor+
              " to fit original length %02d"%orig_len+" to target "+str(target_seconds))
        vf_slowdown = ",setpts=%0.3f*PTS"      % slowdown_factor
    
    ffmpeg("-y","-i", video, "-filter:v", vf_scale+vf_crop+vf_slowdown,
           "-b:v", "1000k", "-r", "29.970", "-profile:v", "main", "-level", "3", "short.mp4",
           # err="uploader.log")
           _err=process_log,_out=process_log)
    return "short.mp4"

def instagram(video):
    if not os.path.isfile(video):
        raise IOError("File %s not accessible." % video)

    print("Processing video " + video + " for Instagram.")
    video = prepare_video_to_instagram(video)
    thumbnail = make_thumbnail(video)
    
    node("./js/instagram-uploader.js", ig_user, ig_password,
         video, thumbnail, "crop,scale,speedup")
    # import ipdb; ipdb.set_trace()

    # Cleanup
    import ipdb; ipdb.set_trace()
    [os.remove(x) for x in ["thumbnail.jpg", "short.mp4"] if os.path.isfile(x)]
    
