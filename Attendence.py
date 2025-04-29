import time
import cv2
import numpy as np
import face_recognition as fr
import os
from datetime import datetime
import TempTest

path = 'AttendImages'
images = []
classNames = []
mylist = os.listdir(path)
print(mylist)

for cl in mylist:
    curimg = cv2.imread(f'{path}/{cl}')
    images.append(curimg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


temp = TempTest.temprature()


def markattendance(name):
    with open('AttendenceFile.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        now = datetime.now()
        date = now.strftime('%D')
        # datenow = now.strftime('%H:%M:%S %p')
        dtString = now.strftime('%H:%M:%S %p')
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            # a = str([[name], [dtString], [date], [temp]])
            f.writelines(f'\n{name},{dtString},{date},{temp}')
            f.flush()

encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = fr.face_locations(imgS)
    encodeCurFrame = fr.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = fr.compare_faces(encodeListKnown, encodeFace)
        faceDist = fr.face_distance(encodeListKnown, encodeFace)
        # print(faceDist)
        matchIndex = np.argmin(faceDist)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            # y2-35
            cv2.rectangle(img, (x1 + 9, y1), (x2, y2 + 20), (99, 255, 60), 2)
            cv2.rectangle(img, (x1 + 9, y2), (x2, y2), (99, 255, 60), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 1, (235, 235, 235), 2)
            # cv2.putText(img, temp, (x1 + 7, y2 + 20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
            markattendance(name)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
