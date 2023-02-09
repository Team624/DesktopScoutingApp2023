import json

config_file = json.load(open('assets/config.json'))
variables = config_file["variables"]
  
def class_generator():
    for i in range(0, len(variables)):
        print("self."+variables[i]+" = data["+str(i)+"]")

def getVariables():
    return variables

def getCreateStatement():
    output = "CREATE TABLE IF NOT EXISTS performance ("
    for variable in variables:
        output+=variable+" integer, "
    return output[:-2]+")"

class Match:

    def __init__(self, data):
        self.match = data[0]
        self.team = data[1]
        self.position = data[2]
        self.preload = data[3]
        self.move = data[4]
        self.auto_charge = data[5]
        self.auto_hybrid_L1 = data[6]
        self.auto_hybrid_L2 = data[7]
        self.auto_hybrid_L3 = data[8]
        self.auto_hybrid_L4 = data[9]
        self.auto_hybrid_L5 = data[10]
        self.auto_hybrid_L6 = data[11]
        self.auto_hybrid_L7 = data[12]
        self.auto_hybrid_L8 = data[13]
        self.auto_hybrid_L9 = data[14]
        self.auto_cone_M1 = data[15]
        self.auto_cube_M2 = data[16]
        self.auto_cone_M3 = data[17]
        self.auto_cone_M4 = data[18]
        self.auto_cube_M5 = data[19]
        self.auto_cone_M6 = data[20]
        self.auto_cone_M7 = data[21]
        self.auto_cube_M8 = data[22]
        self.auto_cone_M9 = data[23]
        self.auto_cone_H1 = data[24]
        self.auto_cube_H2 = data[25]
        self.auto_cone_H3 = data[26]
        self.auto_cone_H4 = data[27]
        self.auto_cube_H5 = data[28]
        self.auto_cone_H6 = data[29]
        self.auto_cone_H7 = data[30]
        self.auto_cube_H8 = data[31]
        self.auto_cone_H9 = data[32]
        self.teleop_hybrid_L1 = data[33]
        self.teleop_hybrid_L2 = data[34]
        self.teleop_hybrid_L3 = data[35]
        self.teleop_hybrid_L4 = data[36]
        self.teleop_hybrid_L5 = data[37]
        self.teleop_hybrid_L6 = data[38]
        self.teleop_hybrid_L7 = data[39]
        self.teleop_hybrid_L8 = data[40]
        self.teleop_hybrid_L9 = data[41]
        self.teleop_cone_M1 = data[42]
        self.teleop_cube_M2 = data[43]
        self.teleop_cone_M3 = data[44]
        self.teleop_cone_M4 = data[45]
        self.teleop_cube_M5 = data[46]
        self.teleop_cone_M6 = data[47]
        self.teleop_cone_M7 = data[48]
        self.teleop_cube_M8 = data[49]
        self.teleop_cone_M9 = data[50]
        self.teleop_cone_H1 = data[51]
        self.teleop_cube_H2 = data[52]
        self.teleop_cone_H3 = data[53]
        self.teleop_cone_H4 = data[54]
        self.teleop_cube_H5 = data[55]
        self.teleop_cone_H6 = data[56]
        self.teleop_cone_H7 = data[57]
        self.teleop_cube_H8 = data[58]
        self.teleop_cone_H9 = data[59]
        self.cycles = data[60]
        self.fouls_committed = data[61]
        self.charging_station_time = data[62]
        self.charging_station_endgame = data[63]
        self.triple_balance = data[64]
        self.disconnect = data[65]
    
    def weight(self, variable, point_value):
        return variable*point_value
    
    def auton_cargo(self):
        map = self.get_map()["auton"]
        L, M, H = map["L"], map["M"], map["H"]
        return (L.count(1)+L.count(2))*3+M.count(1)*4+H.count(1)*6
    
    def teleop_cargo(self):
        map = self.get_map()["teleop"]
        L, M, H = map["L"], map["M"], map["H"]
        return (L.count(1)+L.count(2))*2+M.count(1)*3+H.count(1)*5

    def translate(self, index, values_list):
        return values_list[index]
    
    def conditional(self, value, points):
        if value==1:
            return points
        else:
            return 0
    
    def get_map(self):
        data = {
            "auton":{
                "L": [
                    self.auto_hybrid_L1,
                    self.auto_hybrid_L2,
                    self.auto_hybrid_L3,
                    self.auto_hybrid_L4,
                    self.auto_hybrid_L5,
                    self.auto_hybrid_L6,
                    self.auto_hybrid_L7,
                    self.auto_hybrid_L8,
                    self.auto_hybrid_L9
                ],
                "M" : [
                    self.auto_cone_M1,
                    self.auto_cube_M2,
                    self.auto_cone_M3,
                    self.auto_cone_M4,
                    self.auto_cube_M5,
                    self.auto_cone_M6,
                    self.auto_cone_M7,
                    self.auto_cube_M8,
                    self.auto_cone_M9 
                ],
                "H" : [
                    self.auto_cone_H1,
                    self.auto_cube_H2,
                    self.auto_cone_H3,
                    self.auto_cone_H4,
                    self.auto_cube_H5,
                    self.auto_cone_H6,
                    self.auto_cone_H7,
                    self.auto_cube_H8,
                    self.auto_cone_H9
                ]
            },
            "teleop": {
                "L" : [
                    self.teleop_hybrid_L1,
                    self.teleop_hybrid_L2,
                    self.teleop_hybrid_L3,
                    self.teleop_hybrid_L4,
                    self.teleop_hybrid_L5,
                    self.teleop_hybrid_L6,
                    self.teleop_hybrid_L7,
                    self.teleop_hybrid_L8,
                    self.teleop_hybrid_L9
                ],
                "M" :  [
                    self.teleop_cone_M1,
                    self.teleop_cube_M2,
                    self.teleop_cone_M3,
                    self.teleop_cone_M4,
                    self.teleop_cube_M5,
                    self.teleop_cone_M6,
                    self.teleop_cone_M7,
                    self.teleop_cube_M8,
                    self.teleop_cone_M9 
                ],
                "H" : [
                    self.teleop_cone_H1,
                    self.teleop_cube_H2,
                    self.teleop_cone_H3,
                    self.teleop_cone_H4,
                    self.teleop_cube_H5,
                    self.teleop_cone_H6,
                    self.teleop_cone_H7,
                    self.teleop_cube_H8,
                    self.teleop_cone_H9
                ]
            }
        }
        return data
    
    def get_cargo_specific_count(self, cargo):
        cones = {
            "auton": {
                "L": [
                    self.auto_hybrid_L1,
                    self.auto_hybrid_L2,
                    self.auto_hybrid_L3,
                    self.auto_hybrid_L4,
                    self.auto_hybrid_L5,
                    self.auto_hybrid_L6,
                    self.auto_hybrid_L7,
                    self.auto_hybrid_L8,
                    self.auto_hybrid_L9]
                .count(2),
                "M": [
                    self.auto_cone_M1,
                    self.auto_cone_M3,
                    self.auto_cone_M4,
                    self.auto_cone_M6,
                    self.auto_cone_M7,
                    self.auto_cone_M9
                ].count(1),
                "H": [
                    self.auto_cone_H1,
                    self.auto_cone_H3,
                    self.auto_cone_H4,
                    self.auto_cone_H6,
                    self.auto_cone_H7,
                    self.auto_cone_H9
                ].count(1)
            },
            "teleop": {
                "L": [
                    self.teleop_hybrid_L1,
                    self.teleop_hybrid_L2,
                    self.teleop_hybrid_L3,
                    self.teleop_hybrid_L4,
                    self.teleop_hybrid_L5,
                    self.teleop_hybrid_L6,
                    self.teleop_hybrid_L7,
                    self.teleop_hybrid_L8,
                    self.teleop_hybrid_L9
                ].count(2),
                "M": [
                    self.teleop_cone_M1,
                    self.teleop_cone_M3,
                    self.teleop_cone_M4,
                    self.teleop_cone_M6,
                    self.teleop_cone_M7,
                    self.teleop_cone_M9
                ].count(1),
                "H": [
                    self.teleop_cone_H1,
                    self.teleop_cone_H3,
                    self.teleop_cone_H4,
                    self.teleop_cone_H6,
                    self.teleop_cone_H7,
                    self.teleop_cone_H9
                ].count(1)
            }
        }
        cubes = {
            "auton": {
                "L": [
                    self.auto_hybrid_L1,
                    self.auto_hybrid_L2,
                    self.auto_hybrid_L3,
                    self.auto_hybrid_L4,
                    self.auto_hybrid_L5,
                    self.auto_hybrid_L6,
                    self.auto_hybrid_L7,
                    self.auto_hybrid_L8,
                    self.auto_hybrid_L9
                ].count(1),
                "M": [
                    self.auto_cube_M2,
                    self.auto_cube_M5,
                    self.auto_cube_M8
                ].count(1),
                "H": [
                    self.auto_cube_H2,
                    self.auto_cube_H5,
                    self.auto_cube_H8
                ].count(1)
            },
            "teleop": {
                "L": [
                    self.teleop_hybrid_L1,
                    self.teleop_hybrid_L2,
                    self.teleop_hybrid_L3,
                    self.teleop_hybrid_L4,
                    self.teleop_hybrid_L5,
                    self.teleop_hybrid_L6,
                    self.teleop_hybrid_L7,
                    self.teleop_hybrid_L8,
                    self.teleop_hybrid_L9
                ].count(1),
                "M": [
                    self.teleop_cube_M2,
                    self.teleop_cube_M5,
                    self.teleop_cube_M8
                ].count(1),
                "H": [
                    self.teleop_cube_H2,
                    self.teleop_cube_H5,
                    self.teleop_cube_H8
                ].count(1)
            }
        }
        if cargo=="cube":
            return cubes
        else:
            return cones





