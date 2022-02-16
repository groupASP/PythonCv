from os import name
import cv2
import numpy as np
import pandas as pd
import pymysql

faceDetect = cv2.CascadeClassifier('Detect/haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

def insertOrUpdate(Id, Name):
    global conn
    connection = pymysql.connect(host="localhost", user="root", password="", database="facebase")
    conn = connection.cursor()
    sql = "Select * from people where P_ID='"+str(Id)+"';"
    conn.execute(sql)
    isRecordExist=0
    for row in conn:
        isRecordExist=1
    if(isRecordExist==1):
        sql="Update people set Name='"+str(Name)+"'where P_ID='"+str(Id)+"';"
    else:
        sql="Insert into people(P_ID, Name) values('"+str(Id)+"', '"+str(Name)+"');"
    conn.execute(sql)
    connection.commit()
    conn.close()
Id = input("Enter user ID:")
Name = input("Enter your name:")
insertOrUpdate(Id, Name)
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