from tkinter import *
import backend
import cv2 
import numpy as np
from pyzbar.pyzbar import decode
from utils import *
from analyst import analytics
import json
import webbrowser
import os
from tkinter import ttk
import html_editor

config_file = json.load(open('assets/config.json'))
types = config_file["types"]
var_nums = len(types)
window = Tk()
window.wm_title("Scouting Unlimited")
style = ttk.Style()
style.configure('TButton',  font=('Arial', 8), foreground="black")
counterController=StringVar()
camera_constant = 1
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
        image = cv2.polylines(image, [pts], True, (255, 0, 0), 3)
        barcodeData = obj.data.decode("utf-8")
        if barcodeData.count("\n")>0:
            barcodeData = barcodeData.split("\n")[0:-1]
        else:
            barcodeData = [barcodeData]
        html_additions = []
        for indiv_barcode in barcodeData:
            try:
                added, new_data = backend.add2db(indiv_barcode)
                if added:
                    html_additions.append(new_data)
            except:
                if len(barcodeData)==1:
                    cv2.putText(image, "Error 404", (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
        cv2.putText(image, "Added to DB", (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)

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

def open_link():
    team = dataCounterEntry.get()
    location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "teleop", team+".html")
    if os.path.exists(location):
        os.remove(location)
    html_editor.generate_html_team(team, skip_auton=True)
    webbrowser.open(location,new=1)

cvButton=ttk.Button(window, text="Scan", width=14, command=scan)
cvButton.grid(row=0, column=0)
switchCamera=ttk.Button(window, text="Switch Camera", width=14, command=switch)
switchCamera.grid(row=1, column=0)
dataCounterEntry=Entry(window, textvariable=counterController, width=12)
dataCounterEntry.grid(row=0, column=6)
CounterButton=ttk.Button(window, text="Map", width=12, command=open_link)
CounterButton.grid(row=1, column=6)

teamController1 = StringVar()
newDataEntry1=Entry(window, textvariable=teamController1)
newDataEntry1.grid(row=2, column=1)
b1=ttk.Button(window, text="Update", width=12, command= lambda: update(0))
b1.grid(row=3, column=1)

teamController2 = StringVar()
newDataEntry2=Entry(window, textvariable=teamController2)
newDataEntry2.grid(row=2, column=2)
b2=ttk.Button(window, text="Update", width=12, command= lambda: update(1))
b2.grid(row=3, column=2)

teamController3 = StringVar()
newDataEntry3=Entry(window, textvariable=teamController3)
newDataEntry3.grid(row=2, column=3)
b3=ttk.Button(window, text="Update", width=12, command= lambda: update(2))
b3.grid(row=3, column=3)

teamController4 = StringVar()
newDataEntry4=Entry(window, textvariable=teamController4)
newDataEntry4.grid(row=2, column=4)
b4=ttk.Button(window, text="Update", width=12, command= lambda: update(3))
b4.grid(row=3, column=4)

teamController5 = StringVar()
newDataEntry5=Entry(window, textvariable=teamController5)
newDataEntry5.grid(row=2, column=5)
b5=ttk.Button(window, text="Update", width=12, command= lambda: update(4))
b5.grid(row=3, column=5)

teamController6 = StringVar()
newDataEntry6=Entry(window, textvariable=teamController6)
newDataEntry6.grid(row=2, column=6)
b6=ttk.Button(window, text="Update", width=12, command= lambda: update(5))
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
    if analyst.not_empty():
        data = [
            get_average(analyst.get_list_cargo_general("L", "auton")),
            get_average(analyst.get_list_cargo_general("M", "auton")),
            get_average(analyst.get_list_cargo_general("H", "auton")),
            get_average(analyst.get_list_cargo_general("L", "teleop")),
            get_average(analyst.get_list_cargo_general("M", "teleop")),
            get_average(analyst.get_list_cargo_general("H", "teleop")),
            get_average(analyst.get_list_cargo_specific_ignore_level("cube", "teleop")),
            get_average(analyst.get_list_cargo_specific_ignore_level("cone", "teleop")),
        ]
        docked_auton, engaged_auton, total_auton = analyst.format_charge("auton")
        docked_teleop, engaged_teleop, total_teleop= analyst.format_charge("teleop")
        data.append(str(engaged_auton)+"-"+str(docked_auton)+"-"+str(total_auton-docked_auton-engaged_auton))
        data.append(str(engaged_teleop)+"-"+str(docked_teleop)+"-"+str(total_teleop-docked_teleop-engaged_teleop))
    else:
        data = ["NONE"]*var_nums
    for i in range(0, var_nums):
        text = str(data[i])
        buttons[index][i].delete(0,END)
        buttons[index][i].insert(0, text)

window.mainloop()