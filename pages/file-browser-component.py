import io
import os
import dash

from dash import Dash, html, dash_table, callback
from dash import dcc
import plotly.express as px
import pandas as pd
from flask import Flask
from flask_restful import Resource, Api
from dash import html
from dash import Input, Output
import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template='/filebrowser/<workflowInstanceUuid>')

def layout(workflowInstanceUuid=None, **kwargs):
    # TODO: inject output dir into components
    src = f'{os.environ['BASE_DIR']}/output/{workflowInstanceUuid}'
    if not os.path.isdir(src):
        return html.Div(f"This workflow instance ID was not found: {workflowInstanceUuid}.")

    dir_items = []
    for file_name in os.listdir(src):
        full_path = os.path.join(src, file_name)
        dir_items.append(full_path)

    # logger.info(dir_items)    

    # Filter out only directories
    folders = [item for item in dir_items if os.path.isdir(os.path.join(src, item))]
    folders.append(src)

    layout = [
        dbc.Row([
            html.Div('File Browser', className="text-primary text-center fs-3")
        ]),

        dbc.Row([
            html.Div(children=[
            dcc.Dropdown(
                id="dropdown",
                options=[{"label": x, "value": x} for x in folders],
                value=folders[0],
            )])
        ]), 

        dbc.Row([
            html.Div(children=[
                dcc.RadioItems(options=[], id='files-controls-and-radio-item', value='')
            ])
        ]),

        dbc.Row([
            html.Div(children=[dash_table.DataTable(data=[], page_size=10, id='file-viewer')])
        ])
    ]
        
    return layout