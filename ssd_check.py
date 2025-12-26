import os
import constants

def check_func():
    return constants.SSD_NAME in os.listdir(constants.PATH)
