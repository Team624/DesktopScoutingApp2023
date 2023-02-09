from tkinter import *
import backend
import cv2 
import numpy as np
from pyzbar.pyzbar import decode
from utils import *
from analyst import analytics
import json

config_file = json.load(open('assets/config.json'))
types = config_file["types"]
var_nums = len(types)
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

# def change_image():
#     try:
#         new_image = graphing.get_graph(["624"])
#         img2 = ImageTk.PhotoImage(new_image)
#         label.configure(image=img2)
#         label.image=img2
#     except:
#         img2 = ImageTk.PhotoImage(Image.open("assets/dont_let_him_cool.png"))
#         label.configure(image=img2)
#         label.image=img2

cvButton=Button(window, text="Scan", width=12, command=scan)
cvButton.grid(row=0, column=0)
switchCamera=Button(window, text="Switch Camera", width=12, command=switch)
switchCamera.grid(row=1, column=0)
dataCounterEntry=Entry(window, textvariable=counterController, width=12)
dataCounterEntry.grid(row=0, column=6)
CounterButton=Button(window, text="Count", width=12)
CounterButton.grid(row=1, column=6)

teamController1 = StringVar()
newDataEntry1=Entry(window, textvariable=teamController1)
newDataEntry1.grid(row=2, column=1)
b1=Button(window, text="Update", width=12, command= lambda: update(0))
b1.grid(row=3, column=1)

teamController2 = StringVar()
newDataEntry2=Entry(window, textvariable=teamController2)
newDataEntry2.grid(row=2, column=2)
b2=Button(window, text="Update", width=12, command= lambda: update(1))
b2.grid(row=3, column=2)

teamController3 = StringVar()
newDataEntry3=Entry(window, textvariable=teamController3)
newDataEntry3.grid(row=2, column=3)
b3=Button(window, text="Update", width=12, command= lambda: update(2))
b3.grid(row=3, column=3)

teamController4 = StringVar()
newDataEntry4=Entry(window, textvariable=teamController4)
newDataEntry4.grid(row=2, column=4)
b4=Button(window, text="Update", width=12, command= lambda: update(3))
b4.grid(row=3, column=4)

teamController5 = StringVar()
newDataEntry5=Entry(window, textvariable=teamController5)
newDataEntry5.grid(row=2, column=5)
b5=Button(window, text="Update", width=12, command= lambda: update(4))
b5.grid(row=3, column=5)

teamController6 = StringVar()
newDataEntry6=Entry(window, textvariable=teamController6)
newDataEntry6.grid(row=2, column=6)
b6=Button(window, text="Update", width=12, command= lambda: update(5))
b6.grid(row=3, column=6)

dataEntries = [
    newDataEntry1,
    newDataEntry2,
    newDataEntry3,
    newDataEntry4,
    newDataEntry5,
    newDataEntry6
]

buttons = [
    [],
    [],
    [],
    [],
    [],
    []
]
for i in range(0, 6):
    for b in range(0, var_nums):
        defaultLabel=Entry(window, text="", fg='blue')
        defaultLabel.grid(row=5+b, column=i+1)
        buttons[i].append(defaultLabel)

for i in range(0, len(types)):
    newLabel = Label(window, text=types[i].replace("_", " "), width=18)
    newLabel.grid(row=5+i, column=0)

def update(index):
    team = dataEntries[index].get()
    analyst = analytics(team)
    data = [
        analyst.get_list_cargo_general("L", "auton"),
        analyst.get_list_cargo_general("M", "auton"),
        analyst.get_list_cargo_general("H", "auton"),
        analyst.get_list_cargo_general("L", "teleop"),
        analyst.get_list_cargo_general("M", "teleop"),
        analyst.get_list_cargo_general("H", "teleop"),
    ]
    for i in range(0, var_nums):
        average = round(get_average(data[i]),2)
        text = str(average)
        buttons[index][i].delete(0,END)
        buttons[index][i].insert(0, text)


window.mainloop()