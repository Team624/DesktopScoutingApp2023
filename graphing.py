import plotly.graph_objects as go
from analyst import analytics
from base64 import b64encode
from io import BytesIO
from utils import *
import PIL.Image
import base64

def radar_helper(json_data, categories):
    fig = go.Figure()
    for team in json_data.keys():
        fig.add_trace(go.Scatterpolar(
            r=json_data[team],
            theta=categories,
            fill='toself',
            name=team
        ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 4]
            )
        ),
        showlegend=True
    )
    img_bytes = fig.to_image("png")
    encoding = b64encode(img_bytes).decode()
    img = PIL.Image.open(BytesIO(base64.b64decode(encoding)))
    return img

def getGridDiagram(data):
    fig = go.Figure()
    fig.add_layout_image(
        dict(
            source=PIL.Image.open('assets/grid.png'),
            xref="x",
            yref="y",
            x=0,
            y=3,
            sizex=9,
            sizey=3,
            sizing="stretch",
            opacity=1,
            layer="below")
    )
    low_assets = [
        PIL.Image.open("assets/cube.png"),
        PIL.Image.open("assets/cone.png"),
        PIL.Image.open("assets/failedCube.png"),
        PIL.Image.open("assets/failedCone.png")
    ]
    cone_assets = [
        PIL.Image.open("assets/cone.png"),
        PIL.Image.open("assets/failedCone.png")
    ]
    cube_assets = [
        PIL.Image.open("assets/cube.png"),
        PIL.Image.open("assets/failedCube.png")
    ]
    heights = {
        "L": 0,
        "M": 1,
        "H": 2
    }
    for level in data:
        for index in range(0,9):
            result = data[level][index]-1
            if result>=0:
                if level=="L":
                    asset = low_assets[result]
                elif index in [1, 4, 7]:
                    asset = cube_assets[result]
                else:
                    asset = cone_assets[result]
                fig.add_layout_image(
                    source=asset,
                    xref="x",
                    yref="y",
                    x=index,
                    y=heights[level]+1,
                    layer="below",
                    sizing="stretch",
                    sizex=1,
                    sizey=1
                )
    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        margin=dict(l=0, r=0, t=0, b=0),
        width = 600,
        height = 200
    )   
    fig.update_yaxes(
        range=[0,3],
        showticklabels=False
    )
    fig.update_xaxes(
        range=[0,9], 
        showticklabels=False
    )
    img_bytes = fig.to_image("png")
    encoding = b64encode(img_bytes).decode()
    return encoding

def get_radar(teams):
    output={}
    categories = [
        "Auton Low",
        "Auton Mid",
        "Auton High",
        "Teleop Low",
        "Teleop Mid",
        "Teleop High"
    ]
    for team in teams:
        data = []
        analyzer = analytics(team)
        for period in ["auton", "teleop"]:
            for level in ["L", "M", "H"]:
                data.append(get_average(analyzer.get_list_cargo_general(level, period)))
        output[team] = data
    return radar_helper(output, categories)

