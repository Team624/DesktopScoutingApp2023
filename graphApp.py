from tkinter import * 
import matplotlib.pyplot as plt
from analyst import analytics
from graphing import get_graph
from PIL import ImageTk

def plotProgression(teams, period):
    x_max=0
    y_max=0
    for team in teams:
        progression_list = analytics(team).get_point_progression()
        plot_data = []
        for indiv_list in progression_list:
            latest = indiv_list[period]
            if latest>y_max:
                y_max = latest
            plot_data.append(latest)
        plt.plot([*range(1, len(plot_data)+1)], plot_data, label = team)
    plt.legend()
    plt.xlabel("Match Number")
    plt.ylabel(period.upper()+" Score")
    plt.xticks(range(1,x_max+1))
    plt.yticks(range(0,y_max+2, 5)) 
    plt.title("Teleop Data")
    plt.show()

window = Tk() 
window.title('Data Visualization')
teamsController=StringVar()
newDataEntry=Entry(window, textvariable=teamsController, width=12*7)
newDataEntry.grid(row=0, column=0, columnspan=7)

def get_radar(teams):
    picture = ImageTk.PhotoImage(get_graph(teams))
    newWindow = Toplevel(window)
    label= Label(newWindow)
    label.configure(image=picture)
    label.image=picture
    label.grid(row=3, column=0)
    newWindow.mainloop(1)

plot_button_teleop = Button(master = window, 
                     command= lambda: plotProgression(teamsController.get().split(" "), "teleop"),
                     height = 2, 
                     width = 24,
                     text = "Plot Teleop")
plot_button_teleop.grid(row=1, column=3)

plot_button_auton = Button(master = window, 
                     command= lambda: plotProgression(teamsController.get().split(" "), "auton"),
                     height = 2, 
                     width = 24,
                     text = "Plot Auton")
plot_button_auton.grid(row=2, column=3)

plot_button_endgame = Button(master = window, 
                     command= lambda: get_radar(teamsController.get().split(" ")),
                     height = 2, 
                     width = 24,
                     text = "Get Radar")
plot_button_endgame.grid(row=3, column=3)

window.mainloop()