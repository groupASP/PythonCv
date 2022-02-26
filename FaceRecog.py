from os import name
import cv2
import numpy as np
import pandas as pd
import pymysql

faceDetect = cv2.CascadeClassifier('Detect/haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(1)

def getProfile():
    connection = pymysql.connect(host="localhost", user="root", password="", database="facebase")
    conn = connection.cursor()
    sql = "SELECT P_ID FROM people order by P_ID desc limit 1;"
    conn.execute(sql)
    profile=None
    for row in conn:
        profile=row
    connection.close()
    c = int(''.join(map(str, profile)))
    return c

def insert(Id, Name):
    connection = pymysql.connect(host="localhost", user="root", password="", database="facebase")
    conn = connection.cursor()
    sql = "Select * from people;"
    conn.execute(sql)
    # isRecordExist=0

    sql="Insert into people(P_ID, Name) values('"+str(Id)+"','"+str(Name)+"');"
    conn.execute(sql)
    connection.commit()
    conn.close()
oid = getProfile()
Id = oid+1
# Id = input("Enter user ID:")
Name = input("Enter your name:")
insert(Id, Name)
SampleNum = 0
while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    for(x, y, w, h) in faces:
        SampleNum=SampleNum+1
        cv2.imwrite("DataSet/ "+Name+"."+str(Id)+"."+str(SampleNum)+".jpg", gray[y:y+h, x:x+w])
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.waitKey(100)
    cv2.imshow("Face", img)
    cv2.waitKey(1)
    if(SampleNum>70):
        break
    
cam.release()
cv2.destroyAllWindows()