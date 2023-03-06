from analyst import analytics
from export import *
from backend import allTeams
from utils import *

def contribution_csv(color=True):
    teams = allTeams()
    csv_list = [
        [
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
    ]
    for team in teams:
        analyst = analytics(team)
        docked_auto, engaged_auto, len_auton = analyst.format_charge("auton")
        docked_teleop, engaged_teleop, len_teleop = analyst.format_charge("teleop")
        team_data = [
            team,
            round(get_average(analyst.get_list_cargo_general("L", "auton")),2),
            round(get_average(analyst.get_list_cargo_general("M", "auton")),2),
            round(get_average(analyst.get_list_cargo_general("H", "auton")),2),
            round(get_average(analyst.get_list_cargo_general("L", "teleop")),2),
            round(get_average(analyst.get_list_cargo_general("M", "teleop")),2),
            round(get_average(analyst.get_list_cargo_general("H", "teleop")),2),
            round(get_average(analyst.get_list_cargo_specific("L", "teleop", "cone")),2),
            round(get_average(analyst.get_list_cargo_specific("M", "teleop", "cone")),2),
            round(get_average(analyst.get_list_cargo_specific("H", "teleop", "cone")),2),
            round(get_average(analyst.get_list_cargo_specific("L", "teleop", "cube")),2),
            round(get_average(analyst.get_list_cargo_specific("M", "teleop", "cube")),2),
            round(get_average(analyst.get_list_cargo_specific("H", "teleop", "cube")),2),
            round(get_average(analyst.get_list_cargo_specific("H", "teleop", "cone"))+get_average(analyst.get_list_cargo_specific("M", "teleop", "cone"))+get_average(analyst.get_list_cargo_specific("L", "teleop", "cone")),2),
            round(get_average(analyst.get_list_cargo_specific("H", "teleop", "cube"))+get_average(analyst.get_list_cargo_specific("M", "teleop", "cube"))+get_average(analyst.get_list_cargo_specific("L", "teleop", "cube")),2),
            round(docked_auto/len_auton, 2),
            round(engaged_auto/len_auton, 2),
            round(docked_teleop/len_teleop, 2),
            round(engaged_teleop/len_teleop, 2),
            round(analyst.get_point_average("auton"),2),
            round(analyst.get_point_average("teleop"), 2),
            round(analyst.get_point_average("endgame"),2),
            round(analyst.get_point_average("auton")+analyst.get_point_average("teleop")+analyst.get_point_average("endgame"),2),
        ]
        csv_list.append(team_data)
    save(csv_list, "averages")
    if color:
        colorCode("averages")
contribution_csv()