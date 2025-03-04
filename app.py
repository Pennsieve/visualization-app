import io
import os

from dash import Dash, html, dash_table
from dash import dcc
import plotly.express as px
import pandas as pd
from flask import Flask
from flask_restful import Resource, Api
from dash import html
from dash import Input, Output
import dash_bootstrap_components as dbc

class HealthCheck(Resource):
    def get(self):
        return {'up': 'OK'}

server = Flask('plotly_dash')
# Initialize the app - incorporate css
external_stylesheets = [dbc.themes.CERULEAN]

app = Dash(server=server, external_stylesheets=external_stylesheets)
api = Api(server)
api.add_resource(HealthCheck, '/health')

src = f'{os.environ['BASE_DIR']}/output'
# all_items = os.listdir(src)

all_items2 = []
for file_name in os.listdir(src):
    full_path = os.path.join(src, file_name)
    all_items2.append(full_path)

app.logger.info(all_items2)


# Filter out only directories
folders = [item for item in all_items2 if os.path.isdir(os.path.join(src, item))]
folders.append(src)

controls = [
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in folders],
        value=folders[0],
    )
]

df = pd.read_csv(f'{os.environ['BASE_DIR']}/output/gapminder2007.csv') # test
app.layout = [
    dbc.Row([
        html.Div('File Browser', className="text-primary text-center fs-3")
    ]),

    dbc.Row([
        html.Div(children=controls)
    ]), 

    dbc.Row([
        html.Div(children=[
            dcc.RadioItems(options=[], id='files-controls-and-radio-item', value='')
        ])
    ]),

    dbc.Row([
        html.Div(children=[dash_table.DataTable(data=[], page_size=10, id='file-viewer')])
    ]),

    dbc.Row([
        html.Div(children=[
        dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'],
                        value='lifeExp',
                       inline=True,
                       id='controls-and-radio-item')
        ])
    ]),

    dbc.Row([
        dcc.Graph(figure={}, id='controls-and-graph')
    ])
]


# Add controls to build the interaction - Demo
@app.callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(input_chosen):
    fig = px.histogram(df, x='continent', y=input_chosen, histfunc='avg')
    return fig

# Real world example
@app.callback(
        Output("files-controls-and-radio-item", "options"),
         Output("files-controls-and-radio-item", "value"),
           Input("dropdown", "value"))
def list_all_files(folder_name):
    app.logger.info(folder_name)
    file_names = []
    for file_name in os.listdir(folder_name):
        full_path = os.path.join(folder_name, file_name)
        file_names.append(full_path)

    return file_names, file_names[0]

# control to view csv file when selected
@app.callback(
    Output(component_id='file-viewer', component_property='data'),
    Input("files-controls-and-radio-item", "value")
)
def update_viewer(input_chosen):
    if 'csv' in input_chosen:
        df = pd.read_csv(input_chosen)
        return df.to_dict('records')
    else:
        return []

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)