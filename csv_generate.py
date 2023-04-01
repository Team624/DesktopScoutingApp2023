import os
import math
import json 
import backend
import openpyxl
from utils import *
from backend import allTeams
from analyst import analytics
from openpyxl.styles import PatternFill
from html_editor import generate_html_loop

config_file = json.load(open('assets/config.json'))
colors = config_file["colors"]

def contribution_csv(color=True):
    teams = allTeams()
    csv_list = []
    header = [
            "Team",
            "Auton Low",
            "Auton Mid",
            "Auton High",
            "Teleop Low",
            "Teleop Mid",
            "Teleop High",
            "Low Cones Teleop",
            "Mid Cones Teleop",
            "High Cones Teleop",
            "Low Cubes Teleop",
            "Mid Cubes Teleop",
            "High Cubes Teleop",
            "Cones Teleop",
            "Cubes Teleop",
            "Auton Dock %",
            "Auton Engage %",
            "Teleop Dock %",
            "Teleop Engage %",
            "Auton Pts",
            "Teleop Pts",
            "Endgame Pts",
            "Total Pts",
        ]
    for team in teams:
        analyst = analytics(team)
        docked_auto, engaged_auto, len_auton = analyst.format_charge("auton")
        docked_teleop, engaged_teleop, len_teleop = analyst.format_charge("teleop")
        team_data = [
            team,
            get_average(analyst.get_list_cargo_general("L", "auton")),
            get_average(analyst.get_list_cargo_general("M", "auton")),
            get_average(analyst.get_list_cargo_general("H", "auton")),
            get_average(analyst.get_list_cargo_general("L", "teleop")),
            get_average(analyst.get_list_cargo_general("M", "teleop")),
            get_average(analyst.get_list_cargo_general("H", "teleop")),
            get_average(analyst.get_list_cargo_specific("L", "teleop", "cone")),
            get_average(analyst.get_list_cargo_specific("M", "teleop", "cone")),
            get_average(analyst.get_list_cargo_specific("H", "teleop", "cone")),
            get_average(analyst.get_list_cargo_specific("L", "teleop", "cube")),
            get_average(analyst.get_list_cargo_specific("M", "teleop", "cube")),
            get_average(analyst.get_list_cargo_specific("H", "teleop", "cube")),
            get_average(analyst.get_list_cargo_specific_ignore_level("cone", "teleop")), 
            get_average(analyst.get_list_cargo_specific_ignore_level("cube", "teleop")), 
            round(docked_auto/len_auton, 2),
            round(engaged_auto/len_auton, 2),
            round(docked_teleop/len_teleop, 2),
            round(engaged_teleop/len_teleop, 2),
            analyst.get_point_average("auton"),
            analyst.get_point_average("teleop"),
            analyst.get_point_average("endgame"),
            analyst.get_point_average("total")
        ]
        csv_list.append(team_data)
    csv_list = sorted(csv_list, key=lambda x:x[-1], reverse=True)
    csv_list.insert(0, header) 
    save(csv_list, "averages")
    if color:
        colorCode("averages")

def colorCode(filename):
    assert os.path.isfile(filename+".xlsx")
    doc = openpyxl.load_workbook(filename+".xlsx")
    spreadsheet = doc.active
    for column in range(2, spreadsheet.max_column+1):
        column_data = []
        for row in range(2, spreadsheet.max_row+1):
            column_data.append(spreadsheet.cell(row=row, column=column).value)
        column_data = sorted(column_data, reverse=True)
        for row in range(2, spreadsheet.max_row+1):
            cell = spreadsheet.cell(row=row, column=column)
            index = math.floor((len(colors)-1)*column_data.index(cell.value)/(len(column_data)-1))
            if cell.value==0 and index!=7:
                index==6
            color = colors[index]
            cell.fill = PatternFill(fgColor=color, bgColor=color, fill_type='solid')
    doc.save(filename+".xlsx")

def generate_auton(team):
    data = backend.search(team)
    generate_html_loop(data)

def get_all_autons():
    for team in backend.allTeams():
        generate_auton(team)
        
contribution_csv()