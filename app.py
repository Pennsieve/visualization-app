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
import dash

class HealthCheck(Resource):
    def get(self):
        return {'up': 'OK'}

server = Flask('visualization_app')
# Initialize the app - incorporate css
external_stylesheets = [dbc.themes.CERULEAN]

app = Dash(server=server, external_stylesheets=external_stylesheets, use_pages=True, suppress_callback_exceptions=True)
api = Api(server)
api.add_resource(HealthCheck, '/health')

app.layout = html.Div([
    dash.page_container
])

 # List files based on drop-down selection
@app.callback(
        Output("files-controls-and-radio-item", "options"),
        Output("files-controls-and-radio-item", "value"),
        Input("dropdown", "value"))
def list_all_files(folder_name):
    # logger.info(folder_name)
    file_names = []
    for file_name in os.listdir(folder_name):
        full_path = os.path.join(folder_name, file_name)
        file_names.append(full_path)

    return file_names, file_names[0]

# View selected file (e.g. csv)
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