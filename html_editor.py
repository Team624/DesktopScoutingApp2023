from bs4 import BeautifulSoup
import base64
from graphing import getAutonGrid
import os 
from basic import Match

html_template = """<html>
<head>
<link rel= "stylesheet" type= "text/css" href= "./style.css">
<title>TEAM NUMBER</title>
</head>
<body>
</body>
</html>"""

def get_src(image_path):
    img_file = open(image_path, "rb").read() 
    img_str = base64.b64encode(img_file).decode("utf-8")
    return "data:image/png;base64, "+img_str

def add_image(match_object):
    team = str(match_object.team)
    location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "auton", team+".html")
    if not os.path.exists(location):
        create_empty(team)
    with open("auton/"+team+".html", "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, "html.parser")
    new_graph = getAutonGrid(match_object.get_map()["auton"])
    soup.body.append(soup.new_tag("br"))
    text = soup.new_tag("h1")
    text.string=str(match_object.match)
    soup.body.append(text)
    new_link = soup.new_tag("img", src="data:image/png;base64, "+new_graph)
    soup.body.append(new_link)
    with open("auton/"+team+".html", "w") as f:
        f.write(str(soup))

def create_empty(team):
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "auton")
    if not os.path.exists(directory):
        os.makedirs(directory)
    f = open("auton/"+team+'.html', 'w')
    f.write(html_template.replace("TEAM NUMBER", team))
    f.close()

def generate_html_loop(data):
    for match_list in data:
        add_image(Match(match_list))