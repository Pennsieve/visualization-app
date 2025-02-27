import io
import os

from dash import Dash, html
from dash import dcc
import plotly.express as px
import pandas as pd
from flask import Flask
from flask_restful import Resource, Api
from dash import html
from dash import Input, Output
# import boto3

class HealthCheck(Resource):
    def get(self):
        return {'up': 'OK'}

server = Flask('plotly_dash')
app = Dash(server=server)
api = Api(server)
api.add_resource(HealthCheck, '/health')

src = f'{os.environ['BASE_DIR']}/output'
all_items = os.listdir(src)

# Filter out only directories
folders = [item for item in all_items if os.path.isdir(os.path.join(src, item))]
folders.append(".")
controls = [
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in folders],
        value=folders[0],
    )
]

app.layout = html.Div(
    [html.H1("File Browser"), html.Div(controls), html.Div(id="folder-files")]
)

@app.callback(Output("folder-files", "children"), Input("dropdown", "value"))
def list_all_files(folder_name):
    # This is relative, but you should be able
    # able to provide the absolute path too
    print(folder_name)
    file_names = os.listdir(f'{src}/{folder_name}')

    file_list = html.Ul([html.Li(file) for file in file_names])

    return file_list

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)