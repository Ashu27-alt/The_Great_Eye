import os, time
from main import extra
import constants

SSD = constants.SSD_PATH
processed_this_mount = False

while True:
    if os.path.exists(SSD):
        if not processed_this_mount:
            extra()
            processed_this_mount = True
    else:
        processed_this_mount = False

    time.sleep(2)
