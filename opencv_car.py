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

    cv2.destroyAllWindows()

if __name__ == '__main__':
    Simulator()
