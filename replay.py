from squid import *
from button import *
from time import sleep
import picamera
import subprocess

led = Squid(18, 23, 24)
button = Button(25)
camera = picamera.PiCamera(resolution=(1024,576), framerate=30)

def reset_camera():
  camera.start_preview(alpha=128)
  sleep(1)
  camera.start_recording('video.h264')

reset_camera()
start_time = int(time.time())

while(True):
  if button.is_pressed():
    led.set_color(RED)
    sleep(2)
    stop_time = int(time.time())
    camera.stop_recording()
    end = stop_time - start_time
    start = end - 10
    command = "MP4Box -fps 25 -add video.h264 " + str(stop_time) + ".mp4"
    print command
    subprocess.call(command, shell=True)
    camera.stop_preview()
    led.set_color(GREEN)
    subprocess.call("omxplayer " + str(stop_time) + ".mp4", shell=True)
    
    reset_camera()
    start_time = int(time.time())
  else:
    led.set_color(BLUE)
    sleep(0.1)

