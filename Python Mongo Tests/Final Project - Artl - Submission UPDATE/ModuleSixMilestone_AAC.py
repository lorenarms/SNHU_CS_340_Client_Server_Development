#Lawrence Artl III
#CS 340 22EW6
#Final Project - AUSTIN ANIMAL SHELTER DASHBOARD
#August 11, 2022

import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import base64

import pandas as pd
import plotly.express as px
import pymongo
from pymongo import MongoClient
from bson import ObjectId

from mongoCRUD import CRUD


#############################
# Log into DB via web / local
#############################

# Username and Password for accessing db
usr = 'aacuser'
pw = 'yh0okRBJkaFVCJnw'

# connection string for accessing Atlas
#str = "mongodb+srv://" + usr + ":" + pw + "@cluster0.cyqsq." + "mongodb.net/?retryWrites=true&w=majority"
#shelter = CRUD(str, 'AAC', 'animals')

# local db
shelter = CRUD('mongodb://localhost:27017', 'AAC', 'animals')


#########################
# Dashboard Layout / View
#########################

# call for external stylesheet for fanciness
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Tab title
app.title = 'AAC'

app.layout = html.Div([

    # pull picture from website, will not pull locally
    html.A(
    href="https://www.twitter.com",
    children=[
        html.Center(html.Img(
            alt="Link to my twitter",
            src="https://learn.snhu.edu/content/enforced/1116074-CS-340-T6643-OL-TRAD-UG.22EW6/course_documents/Grazioso%20Salvare%20Logo.png?_&d2lSessionVal=CsPMdhzca7SwIyKhlTV4P6iyU&ou=1116074",
            height='130', width='100'
            ))
        ]
    ),

    #html.Center(html.Img(src='https://learn.snhu.edu/content/enforced/1116074-CS-340-T6643-OL-TRAD-UG.22EW6/course_documents/Grazioso%20Salvare%20Logo.png?_&d2lSessionVal=CsPMdhzca7SwIyKhlTV4P6iyU&ou=1116074', 
    #    height='130', width='100')),

    # Title and author information
    html.Center(html.B(html.H1('Austin Animal Center'))),
    html.Center(html.H3('Database Author: Lawrence Artl')),

    # row of buttons for filters
    html.Div(className='row',
        children=[
                html.Button(id='submit-button-one',n_clicks=0, children= 'Water Rescue'),
                html.Button(id='submit-button-two',n_clicks=0, children= 'Mountain / Wilderness Rescue'),
                html.Button(id='submit-button-three',n_clicks=0, children='Disaster Rescue / Individual Tracking'),
                html.Button(id='submit-button-four', n_clicks=0, children='reset')
        ]),

    html.Div(className="row"),

    html.Div(id='database', children=[]),

    # refresh db
    dcc.Interval(id='interval', interval=86400000 * 7, n_intervals=0),

    html.Button("Save Database", id="save-it"),
    html.Button('Add Row', id='add_row_btn', n_clicks=0),
    
    html.Div(className='row',
            children=[

            # create row for histogram and map; className allows for multiple items in row
            html.Div(id='show-histo',className='col s12 m6'),
                
            html.Div(id="show-location-map",className='col s12 m6'),
        
        ]),

    # create row for just bar graph; className expands graph to fill row
    html.Div(id='show-bar',className='col s12 m6'), 
        
    html.Div(id="placeholder")

])

#############################################
# Interaction Between Components / Controller
#############################################


# Display datatable from database
# Filter based on buttons clicked
@app.callback(Output('database', 'children'),
            [Input('interval', 'n_intervals'),
            Input('submit-button-one', 'n_clicks'),Input('submit-button-two','n_clicks'), 
            Input('submit-button-three','n_clicks'),Input('submit-button-four','n_clicks')
            ])

def populate_datatable(n_intervals,bt1,bt2,bt3,bt4):
    print(n_intervals)

    df = None
    df = pd.DataFrame(list(shelter.readAll({})))
    #Drop the _id column generated automatically by Mongo
    df = df.iloc[:, 1:]

    # water rescue
    if (bt1 > 0):
        df = pd.DataFrame(list(shelter.readAll( {"breed": { "$in": ["Labrador Retriever Mix", 
                            "Chesapeake Bay Retriever", "Newfoundland"]},
                            "sex_upon_outcome" : { "$in": ["Intact Female"]},
                            "age_upon_outcome_in_weeks":{"$lte":156},
                            "age_upon_outcome_in_weeks":{"$gte":20}
                            })))
        df = df.iloc[:, 1:]
        bt1 = 0
        
    # mountain rescue
    if (bt2 > 0):
        df = pd.DataFrame(list(shelter.readAll( {"breed": { "$in": ["German Shepherd", 
                            "Alaskan Malamute", "Old English Sheepdog" , "Siberian Husky" , "Rottweiler"]},
                            "sex_upon_outcome" : { "$in": ["Intact Male"]},
                            "age_upon_outcome_in_weeks":{"$lte":156},
                            "age_upon_outcome_in_weeks":{"$gte":26}
                            })))
        df = df.iloc[:, 1:]
        bt2 = 0

    # disaster rescue
    if (bt3 > 0):
        df = pd.DataFrame(list(shelter.readAll( {"breed": { "$in": ["Doberman Pinscher", 
                            "German Shepherd", "Golden Retriever" , "Bloodhound" , "Rottweiler"]},
                            "sex_upon_outcome" : { "$in": ["Intact Male"]},
                            "age_upon_outcome_in_weeks":{'$lte':300},
                            "age_upon_outcome_in_weeks":{"$gte":20}
                            })))
        df = df.iloc[:, 1:]
        bt3 = 0

    # reset db
    if (bt4 > 0):
        df = pd.DataFrame(list(shelter.readAll({})))
        df = df.iloc[:, 1:]
        bt4 = 0


    # display only necessary information to keep db from being crowded / cluttered
    dft = df[["animal_id", "animal_type", "color", "date_of_birth", 
    "outcome_type", "sex_upon_outcome", "age_upon_outcome", "name"]]

    return [
        dash_table.DataTable(
            id='current_db_table',
            columns=[{'name': x,'id': x,} for x in dft.columns],
            data=df.to_dict('records'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            filter_options={"case": "sensitive"},
            sort_action="native", 
            sort_mode="single",
            row_selectable="single",
            selected_columns=[],
            selected_rows=[],
            page_current=0,
            page_size=10,
            style_cell={'textAlign': 'left', 'minWidth': '100px',
                        'width':'50px', 'maxWidth': '100px'},
        ),
        
    ]




# Add new row for adding information
@app.callback(
    Output('current_db_table', 'data'),
    [Input('add_row_btn', 'n_clicks')],
    [State('current_db_table', 'data'),
     State('current_db_table', 'columns')],
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


# Save new DataTable data to the database
@app.callback(
    Output("placeholder", "children"),
    Input("save-it", "n_clicks"),
    State("current_db_table", "data"),
    prevent_initial_call=True
)
def save_data(n_clicks, data):
    dff = pd.DataFrame(data)
    # call the refresh method to save the new database
    shelter.refresh(dff.to_dict('records'))
    return ""

# Highlight a row that's selected by a user

@app.callback(
    Output('datatable_id', 'style_data_conditional'),
    [Input('datatable_id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


################################
# Data Visualizations and Graphs
################################


# Create map of location data
@app.callback(
    Output('show-location-map', "children"),
    Input('current_db_table', 'data')
)
def build_location_map(data):
    df_map = pd.DataFrame(data)
    fig_map = px.scatter_mapbox(
                        df_map,lat="location_lat", 
                        lon = "location_long",
                        hover_name="animal_id",
                        zoom=11.5,
                        height=700,
                        title='Location of Found Animals',
                        center=dict(lat=30.54, lon=-97.50), 
                        mapbox_style="open-street-map"
                        )
    return [
        html.Div(children=[dcc.Graph(figure=fig_map)], className ="six columns")
    ]

# Show historgram graph
@app.callback(
    Output('show-histo', 'children'),
    Input('current_db_table', 'data')
)
def show_histo(data):
    df_graph = pd.DataFrame(data)
    fig1 = px.histogram(
                        df_graph, 
                        x='animal_type',
                        height=700,
                        color="outcome_type",
                        title='Animal Outcomes'
                        )
    return [
        html.Div(children=[dcc.Graph(figure=fig1)], className="six columns")
    ]

# Show bar graph
@app.callback(
    Output('show-bar', 'children'),
    Input('current_db_table', 'data')
)
def show_bar(data):
    df_graph = pd.DataFrame(data)
    fig2 = px.histogram(df_graph, 
                        x="date_of_birth",
                        title='Animal Date of Birth',
                        height=500,
                        )
    return [
        html.Div(children=[dcc.Graph(figure=fig2)], className="col s12 m6")
    ]


# Run the app in the browser
if __name__ == '__main__':
    app.run_server(debug=True)