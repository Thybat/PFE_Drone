import cv2
import time
from multiprocessing import Process

def send():
    video_writer = cv2.VideoWriter(
        'appsrc ! '
        'videoconvert ! '
        'x264enc tune=zerolatency speed-preset=superfast ! '
        'udpsink host=127.0.0.1 port=5000',
        cv2.CAP_GSTREAMER, 0, 1, (640, 480), True)

    video_getter = cv2.VideoCapture(0)

    while True:

        if video_getter.isOpened():
            ret, frame = video_getter.read()
            video_writer.write(frame)
            # cv2.imshow('send', data_to_stream)
            time.sleep(0.1)

if __name__ == '__main__':
    s = Process(target=send)
    s.start()
    s.join()
    cv2.destroyAllWindows()