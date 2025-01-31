import io
import os

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from flask import Flask
from flask_restful import Resource, Api
# import boto3

class HealthCheck(Resource):
    def get(self):
        return {'up': 'OK'}

server = Flask('plotly_dash')
app = Dash(server=server)
api = Api(server)
api.add_resource(HealthCheck, '/health')

src = os.environ['INPUT_DIR']
df = pd.read_csv(f'{src}/gapminder_unfiltered.csv')

app.layout = html.Div([
    html.H1(children='Visualization App', style={'textAlign':'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)