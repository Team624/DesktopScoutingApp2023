from tkinter import *
import backend
import cv2 
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
import graphing

window = Tk()
window.wm_title("Scouting Unlimited")
counterController=StringVar()
camera_constant = 0
cap = cv2.VideoCapture(camera_constant)

def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)
    cv2.putText(image, str(len(backend.view())), (10,45), cv2.FONT_HERSHEY_SIMPLEX,1.8,(255,0,0), 2) 
    for obj in barcode:
        points = obj.polygon
        (x,y,_,_) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)
        barcodeData = obj.data.decode("utf-8")
        try:
            backend.add2db(barcodeData)
            cv2.putText(image, "Good stuff", (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
        except Exception:
            cv2.putText(image, "Error 404", (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)

def scan():
    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        decoder(frame)
        cv2.imshow('Image', frame)
        cv2.waitKey(1)
        if cv2.getWindowProperty('Image',cv2.WND_PROP_VISIBLE) < 1:        
            break   

def switch():
    global camera_constant
    camera_constant = 1-camera_constant
    global cap 
    cap = cv2.VideoCapture(camera_constant)

def count():
    try:
        dataCounterEntry.delete(0,END)
        dataCounterEntry.insert(0, str(len(backend.view())))
    except Exception:
        pass

def change_image():
    new_image = None #image goes here
    img2 = ImageTk.PhotoImage(new_image)
    label.configure(image=img2)
    label.image=img2


cvButton=Button(window, text="Scan", width=12, command=scan)
cvButton.grid(row=0, column=0)
switchCamera=Button(window, text="Switch Camera", width=12, command=switch)
switchCamera.grid(row=1, column=0)
dataCounterEntry=Entry(window, textvariable=counterController, width=12)
dataCounterEntry.grid(row=0, column=6)
CounterButton=Button(window, text="Count", width=12, command=change_image)
CounterButton.grid(row=1, column=6)

teamController1 = StringVar()
newDataEntry1=Entry(window, textvariable=teamController1)
newDataEntry1.grid(row=2, column=1)

teamController2 = StringVar()
newDataEntry2=Entry(window, textvariable=teamController1)
newDataEntry2.grid(row=2, column=2)

teamController3 = StringVar()
newDataEntry3=Entry(window, textvariable=teamController1)
newDataEntry3.grid(row=2, column=3)

teamController4 = StringVar()
newDataEntry4=Entry(window, textvariable=teamController1)
newDataEntry4.grid(row=2, column=4)

teamController5 = StringVar()
newDataEntry5=Entry(window, textvariable=teamController1)
newDataEntry5.grid(row=2, column=5)

teamController6 = StringVar()
newDataEntry6=Entry(window, textvariable=teamController1)
newDataEntry6.grid(row=2, column=6)

default_pic= ImageTk.PhotoImage(Image.open("assets/624.png"))
label= Label(window,image= default_pic)

label.grid(row=3, column=0)


window.mainloop()