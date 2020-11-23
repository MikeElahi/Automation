# This is a work in progress, the icon is desktop-specific, probably won't work on Windows

import subprocess
import os

host = "8.8.8.8"
response = os.system(f'ping -c 1 {host}')

if response != 0:
    os.system('notify-send "We seem to be disconnected." "Failed to ping Google DNS"  -i network-disconnect --urgency=normal -t 5000')