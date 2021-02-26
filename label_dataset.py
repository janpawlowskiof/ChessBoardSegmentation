
import glob
import pickle
import shutil
import subprocess
import cv2
from path import Path
import numpy as np

RAW_PATH = '/home/eg4l/Downloads/test3'
UNFILTERED_TMP_PATH = '/home/eg4l/datasets/tmp/unfiltered_tmp_chess'
FILTERED_TMP_PATH = '/home/eg4l/datasets/tmp/filtered_tmp_chess'
LABELS_PATH = '/home/eg4l/datasets/labels.pickle'

WHITE_PATH = '/home/eg4l/datasets/white'
BLACK_PATH = '/home/eg4l/datasets/black'
EMPTY_PATH = '/home/eg4l/datasets/empty'

EMPTY = 0
WHITE = 1
BLACK = 2


def get_empty_chessboard_dict():
    result = {}
    for x in range(8):
        for y in range(8):
            result[(x, y)] = EMPTY
    return result


def label_chessboard(intersections_path: str, labels: dict):

    while True:
        intersections_base = cv2.imread(intersections_path)
        preview = np.zeros_like(intersections_base)
        cell_size = int(preview.shape[0]/8)
        folder_name = Path(intersections_path).parent.name

        def refresh_preview():
            print("refreshing_preview")
            nonlocal preview
            preview = np.ones_like(intersections_base)*128
            for x in range(9):
                preview = cv2.line(preview, (x * cell_size, -1000), (x * cell_size, 1000), 255)
            for y in range(9):
                preview = cv2.line(preview, (-1000, y * cell_size), (1000, y * cell_size), 255)

            for (x, y), state in labels[folder_name].items():
                if state == WHITE:
                    cv2.circle(preview, (x*cell_size + cell_size//2, y*cell_size + cell_size//2), 10, (255, 255, 255), -1)
                if state == BLACK:
                    cv2.circle(preview, (x*cell_size + cell_size//2, y*cell_size + cell_size//2), 10, (0, 0, 0), -1)

            cv2.imshow('preview', preview)
            cv2.setMouseCallback('preview', mark_cell)

        def mark_cell(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                labels[folder_name][(x//cell_size, y//cell_size)] = WHITE
                refresh_preview()
            elif event == cv2.EVENT_RBUTTONDOWN:
                labels[folder_name][(x//cell_size, y//cell_size)] = BLACK
                refresh_preview()
            elif event == cv2.EVENT_MBUTTONDOWN:
                labels[folder_name][(x//cell_size, y//cell_size)] = EMPTY
                refresh_preview()

        labels.setdefault(folder_name, get_empty_chessboard_dict())

        refresh_preview()

        if cv2.waitKey(0) == ord('y'):
            print('braking')
            break


def main():
    if Path(LABELS_PATH).isfile():
        with open(LABELS_PATH) as file:
            labels = pickle.load(file)
    else:
        labels = {}

    chessboards = glob.glob(FILTERED_TMP_PATH + '/*/_intersections.jpg')

    for chessboard in chessboards:
        print(chessboard)
        label_chessboard(chessboard, labels)


if __name__ == '__main__':
    main()
