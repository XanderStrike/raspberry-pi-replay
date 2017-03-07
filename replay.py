from squid import *
from button import *
from time import sleep
import picamera
import subprocess

led = Squid(18, 23, 24)
button = Button(25)
camera = picamera.PiCamera(resolution='720p', framerate=60)
subprocess.call("rm *.h264", shell=True)

filename = 0
def reset_camera():
  global filename
  filename += 1
  camera.start_preview(alpha=0)
  sleep(1)
  camera.start_recording(str(filename) + '.h264')

reset_camera()

i = 0

while(True):
  if button.is_pressed():
    led.set_color(BLUE)
    camera.stop_recording()
    camera.stop_preview()

    subprocess.call("python convert.py " + str(filename) + " &", shell=True)
    
    reset_camera()
  else:
    i = (i + 10) % 100
    if (i > 50):
      led.set_color(RED, 100)
    else:
      led.set_color(RED, 0)
    
    sleep(0.1)

