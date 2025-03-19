import io
import os

from dash import Dash, html
import plotly.express as px
import pandas as pd
from flask import Flask
from flask_restful import Resource, Api
from dash import html
from dash import Input, Output
import dash_bootstrap_components as dbc
import dash
from boto3 import client as boto3_client

class HealthCheck(Resource):
    def get(self):
        return {'up': 'OK'}
    
class StopInstance(Resource):
    def post(self, workflowInstanceUuid):
        response = stop_instance(workflowInstanceUuid)
        return response

def stop_instance(workflowInstanceUuid):
    isLocal = os.environ['IS_LOCAL']
    if isLocal == 'true':
        return {}

    print(f'stopping serving requests for: {workflowInstanceUuid}')
    ecs_client = boto3_client("ecs", region_name=os.environ['REGION'])
    return ecs_client.update_service(
        cluster=os.environ['CLUSTER_NAME'],
        service=os.environ['CONTAINER_NAME'],
        desiredCount=0
    )

server = Flask('visualization_app')
# Initialize the app - incorporate css
external_stylesheets = [dbc.themes.CERULEAN]

app = Dash(server=server,
            external_stylesheets=external_stylesheets,
              use_pages=True,
                suppress_callback_exceptions=True)
api = Api(server)
api.add_resource(HealthCheck, '/health')
api.add_resource(StopInstance, '/<workflowInstanceUuid>/stop')

app.layout = html.Div([
    dash.page_container
])

 # List files based on drop-down selection
@app.callback(
        Output("files-controls-and-radio-item", "options"),
        Output("files-controls-and-radio-item", "value"),
        Input("dropdown", "value"))
def list_all_files(folder_name):
    if folder_name is None:
        return [], ""
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