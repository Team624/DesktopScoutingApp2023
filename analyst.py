import backend
from basic import Match
from utils import save

class analytics:

    def __init__(self, teamNumber):
        self.teamNumber = teamNumber
        self.data = [Match(indiv_data) for indiv_data in backend.search(teamNumber)]
    
    def not_empty(self):
        return len(self.data)>0
    
    def get_data(self):
        return self.data

    def get_list_cargo_general(self, level, period):
        progression = []
        for match in self.data:
            progression.append(match.get_cargo_general(period, level))
        return progression
    
    def get_list_cargo_specific(self, level, period, cargo):
        progression = []
        for match in self.data:
            count = match.get_cargo_specific_count(cargo)[period][level]
            progression.append(count)
        return progression
    
    def get_list_cargo_specific_ignore_level(self, cargo, period):
        progression = []
        for match in self.data:
            count = 0
            for level in ["L", "M", "H"]:
                count += match.get_cargo_specific_count(cargo)[period][level]
            progression.append(count)
        return progression
    
    def get_charging_station(self):
        auton, endgame, triple = [], [], []
        for match in self.data:
            auton.append(match.auto_charge)
            endgame.append(match.charging_station_endgame)
            triple.append(match.triple_balance)
        return auton, endgame, triple
    
    def format_charge(self, period):
        auton, endgame, _ = self.get_charging_station()
        if period=="auton":
            docked =auton.count(1)
            engaged = auton.count(2)
            return docked, engaged, len(auton)
        else:
            docked =endgame.count(2)
            engaged = endgame.count(3)
            return docked, engaged, len(endgame)
 
    def triple_success_rate(self):
        _, endgame, triple = self.get_charging_station()
        engaged, attempted = 0, 0
        for i in range(0, len(triple)):
            if triple[i]==1:
                attempted+=1
                if endgame[i]==3:
                    engaged+=1
        if attempted==0:
            return 0
        else:
            return engaged/attempted
    
    def get_point_progression(self):
        output = []
        for match in self.data:
            output.append(
                {
                    "auton": match.get_auton_points(),
                    "teleop": match.teleop_cargo(),
                    "endgame": match.endgame_charging_station_points(),
                    "total": match.get_total_points()
                }
            )
        return output
    
    def get_point_average(self, period):
        progression = self.get_point_progression()
        output = []
        for item in progression:
            output.append(item[period])
        return round(sum(output)/len(output),2)
    
    def get_efficiency_progression(self):
        ratios = []
        for match in self.data:
            cargo = match.teleop_raw_count()
            fumbles = match.fumbles
            if cargo+fumbles==0:
                ratios.append(0)
            else:
                ratios.append(cargo/(cargo+fumbles))
        return ratios
    
    def get_mobility_progression(self):
        progression = []
        for match in self.data:
            progression.append(match.move)
        return progression
    
    def csv_progression(self):
        output = [
            [
                "Match Number",
                "Auton Low",
                "Auton Mid",
                "Auton High",
                "Auton Charge",
                "Auton Mobility",
                "Pieces in Auton",
                "Points in Auton",
                "Teleop Low",
                "Teleop Mid", 
                "Teleop High",
                "Pieces in Teleop",
                "Points in Teleop",
                "Endgame Points",
                "Total"
            ]
        ]
        for match in self.data:
            output.append(
                [
                    match.match,
                    match.get_cargo_general("auton", "L"),
                    match.get_cargo_general("auton", "M"),
                    match.get_cargo_general("auton", "H"),
                    match.auton_charging_station_points(),
                    match.mobility_points(),
                    match.auton_raw_count(),
                    match.get_auton_points(),
                    match.get_cargo_general("teleop", "L"),
                    match.get_cargo_general("teleop", "M"),
                    match.get_cargo_general("teleop", "H"),
                    match.teleop_raw_count(),
                    match.teleop_cargo(),
                    match.endgame_charging_station_points(),
                    match.get_total_points()
                ]
            )
        save(output, self.teamNumber, "progression")