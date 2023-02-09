from bs4 import BeautifulSoup
import base64
import graphing

def get_src(image_path):
    img_file = open(image_path, "rb").read() 
    img_str = base64.b64encode(img_file).decode("utf-8")
    return "data:image/png;base64, "+img_str

def add_image(match_object):
    team = str(match_object.match)
    with open(team+".html", "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, "html.parser")
    new_graph = graphing.getAutonGrid(match_object.get_map()["auton"])
    soup.body.append(soup.new_tag("br"))
    text = soup.new_tag("h1")
    text.string=str(match_object.match)
    soup.body.append(text)
    new_link = soup.new_tag("img", src="data:image/png;base64, "+new_graph)
    soup.body.append(new_link)
    with open(team+".html", "w") as f:
        f.write(str(soup))
