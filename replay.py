# replay.py
# alex standke
# hack day march 2017

from squid import *
from button import *
from time import sleep
import picamera
import subprocess

import signal
import sys

import socket

RESOLUTION = '720p'
FPS = 60

CLIP_TIME = 60 # in seconds

BIND = '0.0.0.0'
PORT = 4005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((BIND, PORT))
sock.setblocking(0)

led = Squid(18, 23, 24)
button = Button(25)

exit_button = Button(12)
camera = picamera.PiCamera(resolution=RESOLUTION, framerate=FPS)
subprocess.call("rm *.h264", shell=True)

start_time = int(time.time())

def signal_handler(signal, frame):
  clean_shutdown()
signal.signal(signal.SIGINT, signal_handler)

def clean_shutdown():
  global camera
  global sock
  print "Exiting..."
  subprocess.call("rm *.h264", shell=True)
  camera.stop_recording()
  camera.close()
  sock.close()
  sys.exit()

filename = 0
def reset_camera():
  global filename
  global start_time
  start_time = int(time.time())
  filename += 1
  sleep(1)
  camera.start_recording(str(filename) + '.h264')

reset_camera()

def take_replay():
  global led
  global camera
  global filename

  led.set_color(BLUE)
  camera.stop_recording()
  subprocess.call("python convert.py " + str(filename) + " &", shell=True)
  reset_camera()

def game_end():
  print "ending game"
  # do something idk

i = 0
while(True):
  if button.is_pressed():
    take_replay()
  elif exit_button.is_pressed():
    clean_shutdown()
  else:
    if (int(time.time()) - start_time) > CLIP_TIME:
      print "Clip too long, restarting"
      camera.stop_recording()
      reset_camera()

    i = (i + 10) % 100
    if (i > 50):
      led.set_color(RED, 100)
    else:
      led.set_color(RED, 0)

    try:
      data = sock.recv(1024)
      if data == 'game_end':
        game_end()
      else:
        take_replay()
    except socket.error:
      x = 'idk'

    sleep(0.1)

