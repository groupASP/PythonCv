import cv2
import numpy as np
import pymysql
import winsound
from PIL import Image

faceDetect = cv2.CascadeClassifier('Detect/haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("Recognizer\\trainingData.xml")
#path='DataSet'
fontface=cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (0,0,255)

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
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        Id, conf = rec.predict(gray[y:y+h, x:x+w])
        if(conf<50):
            profile = getProfile(Id)
            if(profile!=None):
                cv2.putText(img, str(profile[0]), (x, y+h+30), fontface, fontScale, fontColor)
                cv2.putText(img, str(profile[1]), (x, y+h+60), fontface, fontScale, fontColor)
                cv2.putText(img, str(profile[2]), (x, y+h+90), fontface, fontScale, fontColor)
                cv2.putText(img, str(profile[3]), (x, y+h+120), fontface, fontScale, fontColor) 
        else:
            cv2.putText(img, "Unknown", (x, y+h+30), fontface, fontScale, fontColor)
    cv2.imshow("Face", img)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
cam.release()
cv2.destroyAllWindows()