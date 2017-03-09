from squid import *
from button import *
from time import sleep
import picamera
import subprocess

import signal
import sys

led = Squid(18, 23, 24)
button = Button(25)

exit_button = Button(12)
camera = picamera.PiCamera(resolution='1080p', framerate=30)
subprocess.call("rm *.h264", shell=True)

def signal_handler(signal, frame):
  print 'Exiting...'
  subprocess.call("rm *.h264", shell=True)
  camera.stop_recording()
  camera.close()
  sys.exit()
signal.signal(signal.SIGINT, signal_handler)

filename = 0
def reset_camera():
  global filename
  filename += 1
  sleep(1)
  camera.start_recording(str(filename) + '.h264')

reset_camera()

i = 0

while(True):
  if button.is_pressed():
    led.set_color(BLUE)
    camera.stop_recording()

    subprocess.call("python convert.py " + str(filename) + " &", shell=True)

    reset_camera()
  elif exit_button.is_pressed():
    print 'Exiting...'
    subprocess.call("rm *.h264", shell=True)
    camera.stop_recording()
    camera.close()
    sleep(0.5)
    sys.exit()
  else:
    i = (i + 10) % 100
    if (i > 50):
      led.set_color(RED, 100)
    else:
      led.set_color(RED, 0)

    sleep(0.1)

