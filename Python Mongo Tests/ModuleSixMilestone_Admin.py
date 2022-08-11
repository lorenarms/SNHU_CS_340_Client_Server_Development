import dash     # need Dash version 1.21.0 or higher
from dash.dependencies import Input, Output, State
#import dash_table
from dash import dash_table
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html

import pandas as pd
import plotly.express as px
import pymongo
from pymongo import MongoClient
from bson import ObjectId

from aacCRUD import CRUD


###########################
# Data Manipulation / Model
###########################

usr = 'aacuser'
pw = 'yh0okRBJkaFVCJnw'

str = "mongodb+srv://" + usr + ":" + pw + "@cluster0.cyqsq." + "mongodb.net/?retryWrites=true&w=majority"
#shelter = CRUD(str, 'AAC', 'animals')
shelter = CRUD('mongodb://localhost:27017', 'AAC', 'animals')


#########################
# Dashboard Layout / View
#########################


app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([

    html.Div(id='database', children=[]),

    # activated once/week or when page refreshed
    dcc.Interval(id='interval', interval=86400000 * 7, n_intervals=0),

    html.Button("Save to Mongo Database", id="save-it"),
    html.Button('Add Row', id='adding-rows-btn', n_clicks=0),

    html.Div(id="show-location-map", className='col s12 m6'),

    html.Div(id="show-graphs", children=[]),
    html.Div(id="placeholder")

])


#############################################
# Interaction Between Components / Controller
#############################################

#Highlight a row

@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

# Display datatable from database
@app.callback(Output('database', 'children'),
              [Input('interval', 'n_intervals')])
def populate_datatable(n_intervals):
    print(n_intervals)

    df = pd.DataFrame(list(shelter.readAll({})))
    df = df.iloc[:, 1:]

    # Only display the following columns 
    dft = df[["animal_id", "animal_type", "color", "date_of_birth", "outcome_type", "sex_upon_outcome"]]

    #Drop the _id column generated automatically by Mongo
    print(df.head(20))

    return [
        dash_table.DataTable(
            id='my-table',
            columns=[{'name': x,'id': x,} for x in dft.columns],

            data=df.to_dict('records'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            filter_options={"case": "sensitive"},
            sort_action="native", 
            sort_mode="single",
            row_selectable="multi",
            column_selectable="single",
            selected_columns=[],
            selected_rows=[],
            page_current=0,
            page_size=10,
            style_cell={'textAlign': 'left', 'minWidth': '100px',
                        'width': '100px', 'maxWidth': '100px'},
        )
    ]


# Add new row
@app.callback(
    Output('my-table', 'data'),
    [Input('adding-rows-btn', 'n_clicks')],
    [State('my-table', 'data'),
     State('my-table', 'columns')],
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


# Save new DataTable data to the database
@app.callback(
    Output("placeholder", "children"),
    Input("save-it", "n_clicks"),
    State("my-table", "data"),
    prevent_initial_call=True
)
def save_data(n_clicks, data):
    dff = pd.DataFrame(data)
    collection.delete_many({})
    collection.insert_many(dff.to_dict('records'))
    return ""


# Create graphs
@app.callback(
    Output('show-graphs', 'children'),
    Input('my-table', 'data')
)
def add_row(data):
    df_graph = pd.DataFrame(data)
    fig_hist1 = px.histogram(df_graph, x='animal_type',color="outcome_type")
    fig_hist2 = px.histogram(df_graph, x="date_of_birth")
    return [
        html.Div(children=[dcc.Graph(figure=fig_hist1)], className="six columns"),
        html.Div(children=[dcc.Graph(figure=fig_hist2)], className="six columns")
    ]

# Create map of location data
@app.callback(
    Output('show-location-map', "children"),
    Input('my-table', 'data')
)
def build_location_map(data):
    df_map = pd.DataFrame(data)
    fig_map = px.scatter_mapbox(df_map,lat="location_lat", lon = "location_long",
                        hover_name="animal_id",
                        zoom=11.5,
                        height=700,
                        title='Location',
                        center=dict(lat=30.65, lon=-97.48), 
                        mapbox_style="open-street-map"
                        )
    return [
        html.Div(children=[dcc.Graph(figure=fig_map)], className = 'col s12 m6')
    ]
    



if __name__ == '__main__':
    app.run_server(debug=True)