import backend
from basic import Match

class analytics:

    def __init__(self, teamNumber):
        self.data = [Match(indiv_data) for indiv_data in backend.search(teamNumber)]
    
    def not_empty(self):
        return len(self.data)>0
    
    def get_data(self):
        return self.data

    def get_list_cargo_general(self, level, period):
        progression = []
        for match in self.data:
            cubes = match.get_cargo_specific_count("cube")[period][level]
            cones = match.get_cargo_specific_count("cone")[period][level]
            count = cubes + cones
            progression.append(count)
        return progression
    
    def get_list_cargo_specific(self, level, period, cargo):
        progression = []
        for match in self.data:
            count = match.get_cargo_specific_count(cargo)[period][level]
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
            mobility = match.mobility_points()
            auton_cargo = match.auton_cargo()
            teleop_cargo = match.teleop_cargo()
            auton_charge, endgame_charge = match.changing_station_points()
            output.append(
                {
                    "auton": mobility+auton_cargo+auton_charge,
                    "teleop": teleop_cargo,
                    "endgame": endgame_charge
                }
            )
        return output
    
    def get_point_average(self, period):
        progression = self.get_point_progression()
        output = []
        for item in progression:
            output.append(item[period])
        return sum(output)/len(output)

    def get_time_progression(self):
        docked_endgame, engaged_endgame = [], []
        for match in self.data:
            if match.charging_station_endgame==2:
                docked_endgame.append(match.charging_station_time)
            elif match.charging_station_endgame==3:
                engaged_endgame.append(match.charging_station_time)
        return docked_endgame, engaged_endgame
    
    def get_efficiency_progression(self):
        ratios = []
        for match in self.data:
            cargo = match.teleop_raw_count()
            fumbles = match.fumbles
            if cargo+fumbles==0:
                ratios.append(0)
            else:
                ratios.append((cargo+fumbles)/fumbles)
        return ratios
    
    def get_mobility_progression(self):
        progression = []
        for match in self.data:
            progression.append(match.move)
        return progression

    
    
            
        
