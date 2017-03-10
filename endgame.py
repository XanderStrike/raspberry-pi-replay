import sys
import subprocess
import glob, os

print "=== ENDING GAME ==="

command = "MP4Box"
for file in glob.glob("*.mp4"):
  command = command + " -cat " + file

subprocess.call(command + " out.mp4", shell=True)

subprocess.call("/usr/local/bin/youtube-upload  --playlist \"Foosball Replays\" --client-secrets=/home/pi/replay/client_id.json --title=\"Foosball Replay\" out.mp4", shell=True)
