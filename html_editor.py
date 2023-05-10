import os 
import base64
import backend
from basic import Match
from bs4 import BeautifulSoup
from utils import getGridDiagram

html_template = """<!DOCTYPE html>
<html>
<head>
<title>TEAM NUMBER</title>
<style>
img {
width: 600px;
height: 200px;
}
</style>
</head>
<body>
</body>
</html>"""

def get_src(image_path):
    img_file = open(image_path, "rb").read() 
    img_str = base64.b64encode(img_file).decode("utf-8")
    return "data:image/png;base64, "+img_str

def add_image(match_object, period):
    team = str(match_object.team)
    location = os.path.join(os.path.dirname(os.path.abspath(__file__)), period, team+".html")
    if not os.path.exists(location):
        create_empty(team, period)
    with open(period+"/"+team+".html", "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, "html.parser")
    new_graph = getGridDiagram(match_object.get_map()[period], period)
    soup.body.append(soup.new_tag("br"))
    text = soup.new_tag("h1")
    text.string=str(match_object.match)
    soup.body.append(text)
    new_link = soup.new_tag("img", src="data:image/png;base64, "+new_graph)
    soup.body.append(new_link)
    with open(period+"/"+team+".html", "w") as f:
        f.write(str(soup))

def create_empty(team, period):
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), period)
    if not os.path.exists(directory):
        os.makedirs(directory)
    f = open(period+"/"+team+".html", 'w')
    f.write(html_template.replace("TEAM NUMBER", period.capitalize()+" "+team))
    f.close()

def generate_html_loop():
    for team in backend.allTeams():
        generate_html_team(team)

def generate_html_team(team, skip_auton=False):
    for match_list in backend.search(team):
        add_image(Match(match_list), "teleop")
        if not skip_auton:
            add_image(Match(match_list), "auton")
