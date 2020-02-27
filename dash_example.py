import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import sqlite3 as sql

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns]) for i in range(min(len(dataframe), max_rows))]
    )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
    html.H1('BG Tracker'),

    html.Div('Made using Dash: A web application framework for Python.'),

    dcc.Dropdown(
        options=[
        {'label':"Yogg", 'value':"Yogg"},
        {'label':"Edwin", 'value':"Edwin"},
        {'label':"Deryl", 'value':"Deryl"}
        ],
        id="dropdown_hero",
        style={"margin-top":"20px", "margin-bottom":"20px"},
        searchable=False,
        clearable=False
    ),

    dcc.Slider(
        min=1,
        max=8,
        value=8,
        marks={
            1: "1st",
            2: "2nd",
            3: "3rd",
            4: "4th",
            5: "5th",
            6: "6th",
            7: "7th",
            8: "8th"
        },
        step=None,
        included=False,
        updatemode="drag",
        id="position_slider"
    ),

    html.Button('Submit', id='button', style={"margin-top":"20px", "margin-bottom":"20px"}),

    html.Div(id='submit_ack'),

    html.Div(id="my-div"),

    html.Div(id="err", style={"color":"red"}),

    dash_table.DataTable(
        id='table',
        columns=[{"name":"date","id":"date"},{"name":"hero","id":"hero"},{"name":"place","id":"place"}],
        style_cell={"textAlign":"center", "padding":"5px"},
        style_header={'fontWeight': 'bold'},
        style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        },
        {
            'if': {'column_id':'place', 'filter_query':'{place} eq "1"'},
            'backgroundColor': 'rgb(20,120,50)'
        }
    ]
    )
], style={"width":"50%", "margin":"auto"})


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='dropdown_hero', component_property='value'),
    Input(component_id="position_slider", component_property="value")]
)
def update_output_div(hero,position):
    return f"you came in {position}th place with {hero}"

@app.callback(
    [Output(component_id="submit_ack", component_property="children"),
    Output("err","children")],
    [Input(component_id="button", component_property="n_clicks")],
    [State("dropdown_hero", "value"),
     State("position_slider", "value")]
)
def ack_submission(n_clicks,hero,pos):
    if hero == None or pos == None:
        return dash.no_update, "please fill out the form first!"
    else:
        with sql.connect("example.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO runs VALUES (CURRENT_TIMESTAMP, ?, ?)", (hero, pos))
            return f"add run to DB. Postion: {pos} with {hero}", ""

@app.callback(
    Output("table","data"),
    [Input('button','n_clicks')]
)
def update_table(n_clicks):
    with sql.connect("example.db") as conn:
        df = pd.read_sql_query("SELECT * FROM runs", conn)
    return df.to_dict('records')

# server = app.server
if __name__ == '__main__':
    app.run_server(debug=True)
