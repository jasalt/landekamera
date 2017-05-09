# Raspberry Webcam Timelapse setup
- Take photo with webcam every 30 seconds (currently configured for Logitech C930e)
- Convert it daily into 640x640 h264 mp4 -movie and upload to Instagram
- TODO Also convert it into full resolution h265 mp4 video and upload to Amazon S3 for archival purposes

Additionally planned to take HDR photos, apply deflickering and run motion interpolation. Most probably doing processing on some other machine however..

Written in Python with readability in mind, utilizing [sh-library](http://amoffat.github.io/sh/) for running shell utilities and [schedule](https://github.com/dbader/schedule) for scheduling actions. NodeJS library instagram-private-api is used for video uploads.

# TODO Setup
See ./install-deps.sh. 
pip install -r requirements.txt

# Notes
## Instagram upload
Instagram-API-python seems to only upload videos max ~10 sec, otherwise failing with vaque error message.
Using node library instead.

## Deflick
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


## Interpolate


