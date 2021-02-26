
import re
import os
import sys
import glob
import time
import pickle
import subprocess
from colorama import Fore
from pathlib import Path
import cv2
import numpy as np
TMP_PATH = '/tmp/chess_analysis'
WINDOW_NAME = 'is this split correctly? (y/n)'

# subprocess.run(['/home/eg4l/CLionProjects/ChessboardDetectionLib/ChessboardDetectionLib', '/home/eg4l/Downloads/test3', TMP_PATH])

cv2.namedWindow(WINDOW_NAME)
cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)

for file in glob.glob(TMP_PATH + '/*/_mozaic.*'):
    mozaic = cv2.imread(file, cv2.IMREAD_COLOR)

    cv2.imshow(WINDOW_NAME, mozaic)

    k = cv2.waitKey(0)

    if k == ord('y'):
        print("Yay")
    elif k == ord('n'):
        print("Nay")
    elif k == ord('q'):
        cv2.destroyAllWindows()
        exit(-1)
    else:
        print("What is this?")

cv2.destroyAllWindows()
