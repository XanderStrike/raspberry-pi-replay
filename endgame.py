import sys
import subprocess
import glob, os

import json
import requests

print "=== ENDING GAME ==="

command = "MP4Box"
for file in glob.glob("*.mp4"):
  command = command + " -cat " + file

subprocess.call(command + " out.mp4", shell=True)

subprocess.call("/usr/local/bin/youtube-upload  --playlist \"Foosball Replays\" --client-secrets=/home/pi/replay/client_id.json --title=\"Foosball Replay\" out.mp4 > youtube 2>&1", shell=True)

url = open('youtube', 'r').read().splitlines()[-3]

webhook_url = "https://hooks.slack.com/services/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"
slack_data = {'text': url, 'username': "Replay Bot", 'icon_emoji': "movie_camera"}

response = requests.post(
    webhook_url, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
)
