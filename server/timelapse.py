from sh import ffmpeg, mv
# convert jpg's to mp4 and archive source jpg's


def jpgs_to_mp4(source_dir, target_dir):
    # ffmpeg -sameq -f image2 -i time-lapse-%010d.jpg -r 12 -s 640x480 your-awesome-movie.mp4
    # my
    # ffmpeg -r 12 -pattern_type glob -i "*.jpg" -c:v libx264 -r 12 ../timelapse.mp4
    # ffmpeg -r 24 -pattern_type glob -i "*.jpg" -c:v libx264 -r 24 output.mp4
    # ffmpeg -r 24 -pattern_type glob -i "$d/*.jpg" -c:v libx264 -r 24 ../outputs/$d.mp4
    
    FRAMERATE = 30

    if source_dir[-1:] != "/":
        source_dir = source_dir + "/"
    if target_dir[-1:] != "/":
        target_dir = target_dir + "/"

    timestamp = source_dir[:-1][-6:]
    target_filename = target_dir + timestamp + ".mp4"

    print("Converting jpg's from %s to %s with framerate %s" % (source_dir, target_filename, FRAMERATE))    
    
    ffmpeg("-y", "-r", FRAMERATE, "-pattern_type", "glob", "-i", source_dir + "*.jpg", "-c:v", "libx264", "-r", FRAMERATE, target_filename, _err="timelapse.log")

    # then move the pics to archive
    
    #print("Done. Archiving source jpg's.")
    #mv(source_dir, "data/archive/jpg/")
    return target_filename
