from mss import mss
import mss.tools
from win32api import SetCursorPos, mouse_event, GetCursorPos
from win32con import MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
from PyQt5.QtWidgets import QApplication, QLabel
import numpy as np
import cv2
from PIL import Image
import time
from multiprocessing import Process, Queue


def main():
    # The screenshots queue
    screen = Queue()  # type: # Queue
    t0 = Queue()

    # 2 processes: one for grabing and one for saving PNG files
    Process(target=grab, args=(screen, t0)).start()
    Process(target=show, args=(screen, t0)).start()


def rgb_mouse_pos():
    with mss.mss() as sct:
        # Part of the screen to capture
        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        SetCursorPos((0, 0))

        while "Getting pixel color":
            pos = GetCursorPos()
            mouse_x = pos[0]
            mouse_y = pos[1]
            img = np.array(sct.grab(monitor))
            rgb = img[mouse_y, mouse_x]
            print(pos, rgb)
            # Press "q" to quit
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break


def grab(scrn, t1):
    # type: # (Queue) -> None

    rect = {"top": 180, "left": 320, "width": 1280, "height": 720}

    with mss.mss() as sct:
        for _ in range(2_000):
            img = np.array(sct.grab(rect))
            scrn.put(img)
            t1.put(time.time())

    # Tell the other worker to stop
    scrn.put(None)
    t1.put(None)


def show(scrn, t1):
    # type: # (Queue) -> None
    start = time.time()
    frames = 0
    while "there are screenshots":
        img = scrn.get()
        t2 = t1.get()
        frames += 1
        if img is None or t2 is None:
            print(f"\nframes: {frames}\ntotal time: {time.time() - start}\naverage fps: {frames/(time.time() - start)}")
            break
        # Display the picture
        cv2.imshow("OpenCV/Numpy normal", img)

        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale', cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))
        print_no_newline(f"fps: {frames / (time.time() - start)}")
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


def print_no_newline(string):
    import sys
    sys.stdout.write("\r")
    sys.stdout.write(string)
    sys.stdout.flush()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    # rgb_mouse_pos()
