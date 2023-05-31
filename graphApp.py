import plotly.graph_objs as go
import pandas as pd
import dash
from dash import dcc
from dash import html
from analyst import analytics
import backend
import json

config = json.load(open('assets/config.json'))
qual_number = config['qual_number']
options = [
    {'label': 'Auton', 'value': 'auton'},
    {'label': 'Teleop', 'value': 'teleop'},
    {'label': 'Endgame', 'value': 'endgame'},
    {'label': 'Cones', 'value':'cones'},
    {'label': 'Cubes', 'value':'cubes'},
    {'label': 'Pieces', 'value':'pieces'},
    {'label': 'Total', 'value':'total'},
]

def get_df(category):
    df = {}
    teams = backend.allTeams()
    for team in teams:
        team_data = analytics(team).get_point_progression_list(category)
        df[team] = team_data + [float('nan')] * (qual_number-len(team_data))
    df = dict(sorted(df.items()))
    df['x'] = range(1, qual_number+1)
    return pd.DataFrame(df)

def generate_line_plot(df, columns):
    layout = go.Layout(
        width=1500,  
        height=750
    )
    fig = go.Figure(layout=layout)
    fig.update_xaxes(
        range=[0, qual_number]
    )
    fig.update_layout(
        xaxis_title='Qual Number',
        yaxis_title='Points'
    )
    for column in columns:
        fig.add_trace(go.Scatter(x=df['x'], y=df[column], name=column))
    return fig

def update_graph(fig, df, selected_columns):
    fig.data = []
    for column in selected_columns:
        fig.add_trace(go.Scatter(x=df['x'], y=df[column], name=column))
    return fig

initial_columns = ['624']
df = get_df("total")
fig = generate_line_plot(df, initial_columns)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='team-selector',
        options=[{'label': column, 'value': column} for column in df.columns[:-1]],
        value=initial_columns,
        multi=True
    ),
    dcc.Dropdown(
        id='category-dropdown',
        options=options,
        value='total',
        style={
            'width': '100px', 
            'font-size': '15px'
        }
    ),
    dcc.Graph(
        id='graph',
        figure=fig
    ),
])

@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('team-selector', 'value'),
     dash.dependencies.Input('category-dropdown', 'value')])
def update_output(selected_columns, value):
    global df
    df = get_df(value)
    return update_graph(fig, df[selected_columns + ['x']], selected_columns)

def run_graph_app():
    app.run_server()

if __name__ == '__main__':
    run_graph_app()
