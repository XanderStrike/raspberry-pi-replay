import sys
import subprocess
import time

print "=== CONVERSION STARTING ==="
filename = sys.argv[1] + ".h264"

command = "MP4Box -fps 25 -add " + filename + " tmp.mp4"
subprocess.call(command, shell=True)

duration = subprocess.check_output("avprobe -show_format tmp.mp4 2>&1 | sed -n '/duration/s/.*=//p'", shell=True)
duration = int(float(duration))

start = duration - 10

stop_time = int(time.time())
command = "MP4Box -add tmp.mp4 -splitx " + str(start) + ":" + str(duration) + " " + str(stop_time) + ".mp4"
subprocess.call(command, shell=True)

subprocess.call("omxplayer " + str(stop_time) + ".mp4", shell=True)

subprocess.call("rm tmp.mp4 " + filename, shell=True)

print "=== DONE ==="
