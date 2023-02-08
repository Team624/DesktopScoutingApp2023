import backend
from basic import Match
class analytics:

    def __init__(self, teamNumber):
        self.data = [Match(indiv_data) for indiv_data in backend.search(teamNumber)]

    def get_list_cargo_general(self, level, period):
        progression = []
        for match in self.data:
            count = match.get_cargo_specific_count("cube")[period][level]+match.get_cargo_specific_count("cone")[period][level]
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


        

            
        
