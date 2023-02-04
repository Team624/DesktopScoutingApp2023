import os.path
import json

filename = "scouts.json"

def create():
    if not os.path.isfile(filename):
        with open(filename, "w") as f:
            json.dump({}, f)

def add_scout(name, match, team):
    with open(filename, 'r') as f:
        data = json.load(f)
    if match not in data.keys():
        data[match]={}
    data[match][team]=name
    with open(filename, "w") as f:
        json.dump(data, f)

create()

add_scout("Teymur", "1", "624")
add_scout("Arnav", "2", "624")
add_scout("Teymur", "2", "1477")
