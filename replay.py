from squid import *
from button import *
from time import sleep
import picamera
import subprocess

led = Squid(18, 23, 24)
button = Button(25)
camera = picamera.PiCamera(resolution=(1024,576), framerate=60)

def reset_camera():
  subprocess.call("rm tmp.mp4 video.h264", shell=True)
  camera.start_preview(alpha=128)
  sleep(1)
  camera.start_recording('video.h264')

reset_camera()

while(True):
  if button.is_pressed():
    led.set_color(RED)
    sleep(3)
    camera.stop_recording()
    camera.stop_preview()

    command = "MP4Box -fps 25 -add video.h264 tmp.mp4"
    subprocess.call(command, shell=True)

#    subprocess.call("avprobe -show_format tmp.mp4 2>&1 | sed -n '/duration/s/.*=//p'", shell=True)
    duration = subprocess.check_output("avprobe -show_format tmp.mp4 2>&1 | sed -n '/duration/s/.*=//p'", shell=True)
    duration = int(float(duration))
    print 'DURATION'
    print duration
    print 'DURATION'
 
    start = duration - 10

    stop_time = int(time.time())
    command = "MP4Box -add tmp.mp4 -splitx " + str(start) + ":" + str(duration) + " " + str(stop_time) + ".mp4"
    subprocess.call(command, shell=True)

    led.set_color(GREEN)
    subprocess.call("omxplayer " + str(stop_time) + ".mp4", shell=True)
    
    reset_camera()
  else:
    led.set_color(BLUE)
    sleep(0.1)

