# Raspberry Webcam Timelapse setup
- Take photo with webcam every 30 seconds (currently configured for Logitech C930e)
- Convert it daily into 640x640 h264 mp4 video and upload to Instagram
- TODO Also convert it into full resolution h265 mp4 video and upload to Amazon S3 for archival purposes ? or just upload full version to Youtube.

Additionally planned to take HDR photos, apply deflickering and run motion interpolation. Most probably doing processing on some other machine however..

Written in Python with readability in mind, utilizing [sh-library](http://amoffat.github.io/sh/) for running shell utilities and [schedule](https://github.com/dbader/schedule) for scheduling actions. NodeJS library instagram-private-api is used for video uploads.

# TODO Setup
    cd server
    # install-deps.sh  # TODO
    # pip install -r requirements.txt  # TODO, bloated
    python run.py  # this is the main file for now, see comments for running

## Setup on Raspberry / Raspbian Jessie

Raspbian does not have `ffmpeg`, so `sudo apt-get install libav-tools` and `sudo ln -s /usr/bin/avconv /usr/bin/ffmpeg`.

cp config_example.py config.py

    # Install ffmpeg from source
    ## -> Left out libfaac because of compilation problems, no audio on the file so doesn't matter.

    # Fix problem with ipdb installation
    sudo pip install --upgrade setuptools pip
    sudo pip list
    sudo pip install ipython

    # Update node 
    curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
    sudo apt install -y nodejs

# TODO 
- Crash on taking image (probably hardware/power supply related)

# Notes
## Exception handling
https://schedule.readthedocs.io/en/stable/faq.html#what-if-my-task-throws-an-exception

## Instagram upload
Instagram-API-python seems to only upload videos max ~10 sec, otherwise failing with vaque error message. Using node library instead.
## TODO Youtube/FB upload
## TODO Image enchancement
### Simple color correction / enchancement
### TODO HDR
Use manual exposure on c930e for taking stack of images, blend them together.
### TODO Deflick
https://www.youtube.com/watch?v=aABIlQokIaM ML & Darkangerl
### Cyberang3l
https://github.com/cyberang3l/timelapse-deflicker
apt-get install libfile-type-perl libterm-progressbar-perl perlmagick libimage-exiftool-perl

a fork has multicore support?
### ML A1ex http://www.magiclantern.fm/forum/index.php?topic=2553.0
### darktable 2.0
This is the first darktable release, in which deflicker is available, (in exposure module) and can be used.
(it got pulled out of 1.6 for some internal reasons.)

Some explanation on how to use it:
https://youtu.be/VJbJ0btlui0?t=8m10s  (from 8m10s to 11m17s)

IMPORTANT: only available for raw (not even SRAW!) files, i.e. .CR2, .NEF, etc; NOT FOR ANYTHING ELSE (ldr/hdr - jpg, tiff, png, etc)


### TODO Motion Interpolate
https://github.com/dthpham/butterflow


### TODO Artistic stylizer
Run https://github.com/jcjohnson/neural-style for video on server or on amazon ec2 p2/g2 gpu vps instance?
