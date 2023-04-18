import os
import pandas as pd
import plotly.graph_objects as go
from analyst import analytics
from base64 import b64encode
from io import BytesIO
import PIL.Image
import base64

def get_average(data):
    return round(sum(data)/len(data),2)

def get_trimmed(data, cut=2):
    data = sorted(data)[cut:-cut]
    return get_average(data)

def weighted(data, const = 1.25):
    weight = 0
    increment = 1/(len(data)-1)
    exponent = 0
    weighted_sum = 0
    for i in range(0, len(data)):
        weighted_sum+=data[i]*const**exponent
        weight+=const**exponent
        exponent+=increment
    return weighted_sum/weight

def save(data, filename, folder=""):
    if folder!="":
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder)
        if not os.path.exists(directory):
            os.makedirs(directory)
        folder+="\\"
    df = pd.DataFrame(data)
    df.to_excel(folder+filename+".xlsx", index=False, header=False)

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

def getGridDiagram(data, period):
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
    low_assets = {
        "auton":[
            PIL.Image.open("assets/cube.png"),
            PIL.Image.open("assets/cone.png"),
            PIL.Image.open("assets/failedCube.png"),
            PIL.Image.open("assets/failedCone.png"),
        ],
        "teleop":[
            PIL.Image.open("assets/cube.png"),
            PIL.Image.open("assets/cone.png"),
            PIL.Image.open("assets/cube2.png"),
            PIL.Image.open("assets/cone2.png"),
            PIL.Image.open("assets/multi.png"),
        ]
    }
    cone_assets = {
        "auton":[
            PIL.Image.open("assets/cone.png"),
            PIL.Image.open("assets/failedCone.png")
        ],
        "teleop":[
            PIL.Image.open("assets/cone.png"),
            PIL.Image.open("assets/cone2.png")
        ]
    }
    cube_assets = {
        "auton":[
            PIL.Image.open("assets/cube.png"),
            PIL.Image.open("assets/failedCube.png")
        ],
        "teleop":[
            PIL.Image.open("assets/cube.png"),
            PIL.Image.open("assets/cube2.png")
        ]
    }
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
                    asset = low_assets[period][result]
                elif index in [1, 4, 7]:
                    asset = cube_assets[period][result]
                else:
                    asset = cone_assets[period][result]
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
        width = 750,
        height = 250
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
