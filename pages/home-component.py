import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('Visualization App'),
    html.Div('To view visualizations you need to provide a workflow instance ID (as a path parameter).'),
])