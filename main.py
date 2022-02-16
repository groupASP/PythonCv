import tkinter as tk
from tkinter import *
import cv2
import csv
import os
import numpy as np
from PIL import Image,ImageTk
import pandas as pd
import datetime
import time
import pymysql


frm = tk.Tk()
frm.title("Prototype")

frm.geometry('1280x720')
frm.configure(background='snow')




def clear():
    txt.delete(first=0, last=22)
    txt2.delete(first=0, last=22)
    txt.focus()


def insertOrUpdate():
    Id=txt.get()
    Name=txt2.get()
    faceDetect = cv2.CascadeClassifier('Detect/haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
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

Notification = tk.Label(frm, text="All things are good", bg="Green", fg="white", width=15,
                height=3, font=('times', 17, 'bold'))


def trainimg():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detector
    detector = cv2.CascadeClassifier("D:\Python4.2\Detect\haarcascade_frontalface_default.xml")
    try:
        global faces,Id
        faces, Id = getImagesAndLabels("DataSet")
    except Exception as e:
        l='please make "DataSet" folder & put Images'
        Notification.configure(text=l, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    recognizer.train(faces, np.array(Id))
    try:
        recognizer.save("Recognizer\trainingData.yml")
    except Exception as e:
        q='Please make "Recognizer" folder'
        Notification.configure(text=q, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    res = "Model Trained" 
    Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
    Notification.place(x=250, y=400)



def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    Ids = []

    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')

        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(imageNp)
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids

faceDetect = cv2.CascadeClassifier('Detect/haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("Recognizer\\trainingData.yml")
#path='DataSet'
fontface=cv2.FONT_HERSHEY_SIMPLEX
fontScale = 2
fontColor = (255,0,0)

def auto():
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
            now = time.time()
            future = now + 20
            Id, conf = rec.predict(gray[y:y+h, x:x+w])
            if(conf<70):
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
        key = cv2.waitKey(1) & 0xFF == ord('q')
        if key:
            break
    try:
        connection = pymysql.connect(host="localhost", user="root", password="", database="facebase")
        conn = connection.cursor()
    except Exception as e:
        print(e)

    insert_data =  "INSERT INTO attandance VALUES (0, %s, %s)"
    VALUES = (str(profile[0]),str(profile[1]))
    try:
        conn.execute(insert_data, VALUES)
        connection.commit()
    except Exception as ex:
        print(ex)
    cam.release()
    cv2.destroyAllWindows()

def on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        frm.destroy()
frm.protocol("WM_DELETE_WINDOW", on_closing)

lbl = tk.Label(frm, text="Enrollment:", width=20, height=2, fg="black", bg="snow", font=('times', 15, ' bold '))
lbl.place(x=200, y=200)

def testVal(inStr,acttyp):
    if acttyp == '1': #insert
        if not inStr.isdigit():
            return False
    return True

txt = tk.Entry(frm, validate="key", width=20, bg="lightblue", fg="red", font=('times', 25, ' bold '))
txt['validatecommand'] = (txt.register(testVal),'%P','%d')
txt.place(x=550, y=210)

lbl2 = tk.Label(frm, text="Name:", width=20, fg="black", bg="snow", height=2, font=('times', 15, ' bold '))
lbl2.place(x=200, y=300)

txt2 = tk.Entry(frm, width=20, bg="lightblue", fg="red", font=('times', 25, ' bold '))
txt2.place(x=550, y=310)

takeImg = tk.Button(frm, text="Take Images",command=insertOrUpdate,fg="black"  ,bg="lightgreen"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=200, y=500)

clearButton = tk.Button(frm, text="Clear",command=clear,fg="black"  ,bg="deep pink"  ,width=10  ,height=1 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=950, y=310)

trainImg = tk.Button(frm, text="Train Images",fg="black",command=trainimg ,bg="lawn green"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trainImg.place(x=550, y=500)

FA = tk.Button(frm, text="Automatic Attendace",fg="white",command=auto  ,bg="blue2"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
FA.place(x=900, y=500)


frm.mainloop()