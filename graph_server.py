import plotly.graph_objects as go
import pandas as pd
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dotenv import load_dotenv
load_dotenv(".env")
PSQL_URI = os.environ.get("PSQL_URI")

from dash.dependencies import Output, Input
from postgres_ops import PsqlOps
app = dash.Dash()


psql_obj = PsqlOps(PSQL_URI=PSQL_URI)
# df = pd.read_sql_query("select * from candlestick;",psql_obj.db)

# fig = go.Figure(data=go.Ohlc(x=df['time'],
#                     open=df['open'],
#                     high=df['highest'],
#                     low=df['lowest'],
#                     close=df['close']))

# app.layout = html.Div([
#     dcc.Graph(figure=fig)
# ])

app.layout = html.Div(
    [
        html.Div(children=[
            dcc.Interval(
                id='interval_component',
                interval=2000,
                
            ),
            
        ]),
        html.Div(id='output-graph'),
    ],
    
)

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    Input(component_id='interval_component', component_property='interval'))
def update_graph(interval):
    df = pd.read_sql_query("select * from candlestick;",psql_obj.db)
    fig = go.Figure(data=go.Ohlc(x=df['time'],
                    open=df['open'],
                    high=df['highest'],
                    low=df['lowest'],
                    close=df['close']))

    return dcc.Graph(figure=fig,animate=True)
app.run_server(debug=True, dev_tools_hot_reload=True)