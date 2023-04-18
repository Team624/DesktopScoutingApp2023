import numpy as np
import requests
from scipy.linalg import solve
import json 
from utils import save
import pandas as pd
import os
import backend
from basic import Match
import concurrent.futures
import statbotics

config = json.load(open('assets/config.json'))
class TBA:

    def __init__(self):
        self.event = config["event"]
        self.key = {'X-TBA-Auth-Key': config["tba-key"]}
        self.sb = statbotics.Statbotics()
        self.rp_threshold = {
            "1":config["rp1_threshold"],
            "2":config["rp2_threshold"]
        }
    
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
            if match['comp_level']=='qm' and match['actual_time']!=None:
                colors =['red', 'blue']
                for color in colors:
                    alliance_data =  match["score_breakdown"][color]
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
        opr_data = self.get_links()
        final_data={}
        for [team, opr] in opr_data:
            final_data[team]=round(opr,2)
        return final_data
    
    def get_grid(self, match_object, teleop=True):
        period = "teleopCommunity" if teleop else "autoCommunity"
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
         
    def check_grid(self, match, period):
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

    def check_charging(self, match_object, auton):
        team = str(match_object.team)
        match = str(match_object.match)
        link = "https://www.thebluealliance.com/api/v3/match/"+self.event+"_qm"+match
        match_data = requests.get(url=link, headers=self.key).json()
        if "frc"+team in match_data["alliances"]["red"]['team_keys']:
            team_index= match_data["alliances"]["red"]['team_keys'].index("frc"+team)
            alliance = "red"
        elif "frc"+team in match_data["alliances"]["blue"]['team_keys']:
            team_index= match_data["alliances"]["blue"]['team_keys'].index("frc"+team)
            alliance = "blue"
        else:
            return False
        score_breakdown = match_data["score_breakdown"][alliance]
        if auton:
            result = score_breakdown["autoChargeStationRobot"+str(team_index+1)]
            if result=="None":
                return match_object.auto_charge==0
            else:
                if score_breakdown["autoChargeStationPoints"]==12:
                    return match_object.auto_charge==2
                else:
                    return match_object.auto_charge==1
        else:
            result = score_breakdown["endGameChargeStationRobot"+str(team_index+1)]
            if result=="None":
                return match_object.charging_station_endgame==0
            elif result=="Park":
                return match_object.charging_station_endgame==1
            else:
                robotsOn = [
                    score_breakdown["endGameChargeStationRobot1"],
                    score_breakdown["endGameChargeStationRobot2"],
                    score_breakdown["endGameChargeStationRobot3"]
                ].count("Docked")
                points_per_bot = score_breakdown["endGameChargeStationPoints"]/robotsOn
                if points_per_bot==6:
                    return match_object.charging_station_endgame==2
                else:
                    return match_object.charging_station_endgame==3
            
    def export_links(self):
        df = pd.DataFrame(self.get_links(), columns =['Team', 'Links'])
        save(df, 'link')

    def check_match(self, match_object):
        auton_accuracy = self.check_grid(match_object, 'auton')
        teleop_accuracy = self.check_grid(match_object, 'teleop')
        auton_charge = self.check_charging(match_object, True)
        teleop_charge = self.check_charging(match_object, False)
        return [
                match_object.match,
                match_object.team,
                auton_accuracy, 
                auton_charge, 
                teleop_accuracy, 
                teleop_charge
            ]
    
    def check_db(self):
        data = [Match(indiv_data) for indiv_data in backend.view()]
        accuracy = []
        threads = []
        header = [
                "Match",
                "Team",
                "Auton Mistakes",
                "Auton Charge Mistakes",
                "Teleop Mistakes",
                "Teleop Charge Mistakes"
        ]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for match_object in data:
                thread = executor.submit(self.check_match, match_object)
                threads.append(thread)
        for thread in threads:
            result = thread.result()
            if result[-2]!=-1:
                accuracy.append(thread.result())
        accuracy = sorted(accuracy, key=lambda x:x[0])
        accuracy.insert(0, header)
        save(accuracy, "accuracy")
    
    def get_prediction(self, match_key):
        prediction = self.sb.get_match(match=match_key)
        output = {
            "red":0,
            "blue":0
        }
        output[prediction['winner']] = 2
        for color in ["red", "blue"]:
            for rp in ["1","2"]:
                if prediction[color+"_rp_"+rp+"_prob"]>self.rp_threshold[rp]:
                    output[color] = output[color]+1
        return output

    def predict_table(self):
        matches = self.get_comp_data()
        table = {}
        for match in matches:
            if match['comp_level']=='qm':
                if match["winning_alliance"]!="":
                    rps = {
                        "red":match["score_breakdown"]["red"]["rp"],
                        "blue":match["score_breakdown"]["blue"]["rp"]
                    }
                else:
                    rps = self.get_prediction(match["key"])
                for color in ["red", "blue"]:
                    for team in match["alliances"][color]["team_keys"]:
                        team = team[3:]
                        if team not in table.keys():
                            table[team]=0
                        table[team] = table[team]+rps[color]
        table = dict(sorted(table.items(), key=lambda item: item[1], reverse=True))
        self.dump_json(table, "table")
    
    def sort_pictures(self):
        df = pd.read_csv("pit.csv")
        df = df.values.tolist()[1:]
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pictures')
        if not os.path.exists(directory):
            os.makedirs(directory)
        for row in df:
            team = str(row[1])
            link = row[-1]
            try:
                file_id = link[link.index("=")+1:]
                response = requests.get(f'https://drive.google.com/uc?id={file_id}&export=download')
                with open('pictures/'+team+'.jpg', 'wb') as f:
                    f.write(response.content)
            except:
                print("FAILED TO DOWNLOAD", team)
