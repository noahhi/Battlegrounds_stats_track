import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import sqlite3 as sql
from hero_scrape import fetch_hero_list

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__) #, external_stylesheets=external_stylesheets

def update_table():
    with sql.connect("example.db") as conn:
        df = pd.read_sql_query("SELECT * FROM runs", conn)
    return df.to_dict('records')


app.layout = html.Div(children=[
    html.H1('BG Tracker'),

    html.Div('Made using Dash: A web application framework for Python.'),

    # hero selection
    dcc.Dropdown(
        options=[{'label':hero, 'value':hero} for hero in fetch_hero_list()],
        id="dropdown_hero",
        style={"margin-top":"20px", "margin-bottom":"20px"},
        searchable=False,
        clearable=False
    ),

    dcc.RadioItems(
    options=[
        {'label': '1st', 'value': '1'},
        {'label': '2nd', 'value': '2'},
        {'label': '3rd', 'value': '3'},
        {'label': '4th', 'value': '4'},
        {'label': '5th', 'value': '5'},
        {'label': '6th', 'value': '6'},
        {'label': '7th', 'value': '7'},
        {'label': '8th', 'value': '8'}
    ],
    labelStyle={'display': 'inline-block'},
    id="position_radio"
    ),

    # # position selection
    # dcc.Slider(
    #     min=1,
    #     max=8,
    #     value=8,
    #     marks={
    #         1: "1st",
    #         2: "2nd",
    #         3: "3rd",
    #         4: "4th",
    #         5: "5th",
    #         6: "6th",
    #         7: "7th",
    #         8: "8th"
    #     },
    #     step=None,
    #     included=False,
    #     updatemode="drag",
    #     id="position_slider"
    # ),

    # submit new run button
    html.Button('Submit', id='button',
        className="submit_button"),

    # ackknledgment of successful submission to DB
    html.Div(id='submit_ack'),

    html.Div(id="my-div"),

    html.Div(id="err", style={"color":"red"}),

    dash_table.DataTable(
        id='table',
        columns=[{"name":"date","id":"date"},{"name":"hero","id":"hero"},{"name":"place","id":"place"}],
        data=update_table(),
        sort_action='native',
        style_cell={"textAlign":"center", "padding":"5px"},
        style_header={'fontWeight': 'bold'},
        #filter_action='native',
        page_action='native',
        page_size=10,
        editable=True,
        #row_deletable=True,
        style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        },
        # {
        #     'if': {'column_id':'place', 'filter_query':'{place} eq "1"'},
        #     'backgroundColor': 'rgb(127,255,0)'
        # }
        ]
    ),

    dcc.Graph(
        id='avg-pos-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Average Hero Position'
            }
        }
    )
], style={"width":"50%", "margin":"auto"})


# @app.callback(
#     Output(component_id='my-div', component_property='children'),
#     [Input(component_id='dropdown_hero', component_property='value'),
#     Input(component_id="position_radio", component_property="value")]
# )
# def update_output_div(hero,position):
#     return f"you came in {position}th place with {hero}"

@app.callback(
    Output('avg-pos-graph', 'figure'),
    [Input('table','data')]
)
def update_graph(table_data):
    results_by_hero = {}
    for row in table_data:
        hero = row['hero']
        place = row['place']
        if hero in results_by_hero:
            results_by_hero[hero].append(place)
        else:
            results_by_hero[hero]=[place]

    avgs_by_hero = {}
    for hero in results_by_hero:
        avgs_by_hero[hero] = sum(results_by_hero[hero])/len(results_by_hero[hero])

    fig = {'data':[]}
    #fig['data'] = {'x': [hero], 'y':[avgs_by_hero[hero]]} for hero in avgs_by_hero
    fig['data'].append({})
    fig['data'][0]['x'] = [hero for hero in results_by_hero]
    fig['data'][0]['y'] = [9-avgs_by_hero[hero] for hero in fig['data'][0]['x']]
    fig['data'][0]['type'] = 'bar'

    return fig


@app.callback(
    [Output(component_id="submit_ack", component_property="children"),
    Output("err","children"),
    Output("table","data")],
    [Input(component_id="button", component_property="n_clicks")],
    [State("dropdown_hero", "value"),
     State("position_radio", "value")]
)
def ack_submission(n_clicks,hero,pos):
    if hero == None or pos == None:
        return dash.no_update, dash.no_update, dash.no_update #"please fill out the form first!"
    else:
        with sql.connect("example.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO runs VALUES (CURRENT_TIMESTAMP, ?, ?)", (hero, pos))
            df = pd.read_sql_query("SELECT * FROM runs", conn)
            return f"add run to DB. Postion: {pos} with {hero}", "", df.to_dict('records')

# @app.callback(
#     Output("table","data"),
#     [Input('button','n_clicks')]
# )
# def update_table(n_clicks):
#     with sql.connect("database.db") as conn:
#         df = pd.read_sql_query("SELECT * FROM runs", conn)
#     return df.to_dict('records')

# server = app.server
if __name__ == '__main__':
    app.run_server(debug=True)
