import cv2
import numpy as np
from multiprocessing import Process
cars_cascade = cv2.CascadeClassifier('haarcascade_car.xml')
plate_cascade = cv2.CascadeClassifier('haarcascade_licence_plate_rus_16stage.xml')

def detect_cars_pic(frame, gray_frame):
    cars = cars_cascade.detectMultiScale(gray_frame, 1.15, 4)
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x+w,y+h), color=(255, 0, 0), thickness=2)
        roi_gray = gray_frame[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        plates = plate_cascade.detectMultiScale(roi_gray)
        for (px, py, pw, ph) in plates:
            cv2.rectangle(roi_color, (px, py), (px + pw, py + ph), (255, 255, 0), 2)
    return frame
def detect_cars_videos(frame):
    cars = cars_cascade.detectMultiScale(frame, 1.15, 4)
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x+w,y+h), color=(255, 0, 0), thickness=2)
    return frame

def send():
    cap_send = cv2.VideoCapture('videotestsrc ! video/x-raw,framerate=20/1 ! videoscale ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
    out_send = cv2.VideoWriter('appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=127.0.0.1 port=5000',cv2.CAP_GSTREAMER,0, 20, (320,240), True)

    if not cap_send.isOpened() or not out_send.isOpened():
        print('VideoCapture or VideoWriter not opened')
        exit(0)

    while True:
        ret,frame = cap_send.read()

        if not ret:
            print('empty frame')
            break

        out_send.write(frame)

        cv2.imshow('send', frame)
        if cv2.waitKey(1)&0xFF == ord('q'):
            break

    cap_send.release()
    out_send.release()

def receive():
    cap_receive = cv2.VideoCapture('udpsrc port=5000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

    if not cap_receive.isOpened():
        print('VideoCapture not opened')
        exit(0)

    while True:
        ret,frame = cap_receive.read()

        if not ret:
            print('empty frame')
            break

        cv2.imshow('receive', frame)
        if cv2.waitKey(1)&0xFF == ord('q'):
            break
    cap_receive.release()


'''    
def Simulator():
    choice = input("1.Video, 2.Picture")
    if choice == "1":
        carVideo = cv2.VideoCapture('cars.mp4')
        while carVideo.isOpened():
            ret, frame = carVideo.read()
            controlkey = cv2.waitKey(1)
            if ret:
                cars_frame = detect_cars_videos(frame)
                cv2.imshow('frame', cars_frame)
            else:
                break
            if controlkey == ord('q'):
                break
        carVideo.release()
    elif choice == "2":
        CarPhoto = cv2.imread('test_api.jpg')
        grey_CarPhoto = cv2.cvtColor(CarPhoto, cv2.COLOR_BGR2GRAY)
        cv2.imshow("original", CarPhoto)
        classified_pic = detect_cars_pic(CarPhoto, grey_CarPhoto)
        cv2.imshow("classified_pic",classified_pic)
        controlkey = cv2.waitKey(0)

    cv2.destroyAllWindows()'''

if __name__ == '__main__':
    s = Process(target=send)
    r = Process(target=receive)
    s.start()
    r.start()
    s.join()
    r.join()
    #Simulator()
