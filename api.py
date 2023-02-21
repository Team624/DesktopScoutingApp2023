import numpy as np
import requests
from scipy.linalg import solve
import json 

config = json.load(open('assets/config.json'))
class TBA:

    def __init__(self):
        self.event = config["event"]
        self.key = {'X-TBA-Auth-Key': config["tba-key"]}
    
    def get_comp_data(self):
        link = "https://www.thebluealliance.com/api/v3/event/"+self.event+"/matches"
        return requests.get(url=link, headers=self.key).json()
    
    def get_teams(self):
        link = "https://www.thebluealliance.com/api/v3/event/"+self.event+"/rankings"
        teams_json = requests.get(url=link, headers=self.key).json()
        return [team["team_key"] for team in teams_json["rankings"]]
    
    def dump_json(self, data, file_name):
        with open(file_name+'.json', 'w') as json_file:
            json.dump(data, json_file)

    def get_links(self):
        comp_data = self.get_comp_data()
        teams = self.get_teams()
        scores_matrix = []
        teams_matrix = []
        for match in comp_data:
            if match['comp_level']=='qm':
                colors =['red', 'blue']
                for color in colors:
                    alliance_data =  match["score_breakdown"][color]
                    if alliance_data["totalPoints"]==-1:
                        break
                    scores_matrix.append(alliance_data["linkPoints"]/5)
                    teams_matrix.append(self.get_row(match, teams, color))
        teams_matrix = np.array(teams_matrix) 
        scores_matrix = np.array(scores_matrix)
        oprs = solve(np.matmul(teams_matrix.transpose(), teams_matrix), np.matmul(teams_matrix.transpose(), scores_matrix))
        final_data = sorted(zip(teams, oprs.tolist()), key=lambda x:x[1], reverse=True)
        return final_data
    
    def get_row(self, match, teams, color):
        row = [0]*len(teams)
        for team in match["alliances"][color]["team_keys"]:
            row[teams.index(team)]=1
        return row

    def get_oprs_dict(self):
        opr_data = self.OPR_links()
        final_data={}
        for [team, opr] in opr_data:
            final_data[team]=opr
        return final_data
    
    def get_grid(self, match_object, teleop=True):
        if teleop:
            period = "teleopCommunity"
        else:
            period = "autoCommunity"
        team = str(match_object.team)
        match = str(match_object.match)
        link = "https://www.thebluealliance.com/api/v3/match/"+self.event+"_qm"+match
        match_data = requests.get(url=link, headers=self.key).json()
        if "frc"+team in match_data["alliances"]["red"]['team_keys']:
            alliance = "red"
        elif "frc"+team in match_data["alliances"]["blue"]['team_keys']:
            alliance = "blue"
        else:
            return None
        if period=="autoCommunity":
             return match_data["score_breakdown"][alliance][period]
        else:
            auton_grid = match_data["score_breakdown"][alliance]["autoCommunity"]
            teleop_grid = match_data["score_breakdown"][alliance]["teleopCommunity"]
            for level in ["B", "M", "T"]:
                for index in range(0, 9):
                    if teleop_grid[level][index]==auton_grid[level][index]:
                        teleop_grid[level][index]="None"
            return teleop_grid
         
    def check_match(self, match, period):
        tba_data = self.get_grid(match, period=="teleop")
        if tba_data is None:
            return -1
        mistakes = 0
        match_data = match.get_map()[period]
        for levels in [["B","L", 2],["M", "M", 1], ["T", "H", 1]]:
            level_tba = levels[0]
            level_local = levels[1]
            max_val = levels[2]
            for index in range(0,9):
                tba_value = tba_data[level_tba][index]
                local_value = match_data[level_local][index]
                if 0<local_value<=max_val and tba_value=="None":
                    mistakes+=1
        return mistakes