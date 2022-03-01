import tkinter as tk
from tkinter import *
import cv2
import pymysql
import time

faceDetect = cv2.CascadeClassifier('Detect/haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(1)
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("Recognizer\\trainingData2.yml")
#path='DataSet'
fontface=cv2.FONT_HERSHEY_SIMPLEX
fontScale = 2
fontColor = (255,0,0)

def getProfile(Id):
    connection = pymysql.connect(host="localhost", user="root", password="", database="facebase")
    conn = connection.cursor()
    sql = "SELECT * FROM people where P_ID='"+str(Id)+"';"
    conn.execute(sql)
    profile=None
    for row in conn:
        profile=row
    conn.close()
    return profile

while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    for(x, y, w, h) in faces:
            # now = time.time()
            # future = now + 20
            conf=0
            Id, conf = rec.predict(gray[y:y+h, x:x+w])
            if(conf>45 and conf<70):
                print(conf)
                global profile
                profile = getProfile(Id)
                if(profile!=None):
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(img, str(profile[0]), (x, y+h+30), fontface, fontScale, fontColor)
                    cv2.putText(img, str(profile[1]), (x, y+h+80), fontface, fontScale, fontColor)
            else:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(img, "Unknown", (x, y+h+30), fontface, fontScale, fontColor)
    cv2.imshow("Face", img)
    key=cv2.waitKey(1) & 0xFF == ord('q')
    if conf>46:
        break
cam.release()
cv2.destroyAllWindows()
