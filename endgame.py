import sys
import subprocess
import glob, os

print "=== ENDING GAME ==="

command = "MP4Box"
for file in glob.glob("*.mp4"):
  command = command + " -cat " + file

subprocess.call(command + " out.mp4", shell=True)

