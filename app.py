# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 16:20:28 2022

@author: basus
"""

# 1. Import Dash
import pandas as pd
import sqlite3
import dash
import plotly.express as px
from dash import dcc
from urllib.request import urlopen
import json
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State


# 2. Create a Dash app instance
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LUX])
server = app.server
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
states = [
    dbc.DropdownMenuItem("Georgia"),
]
measures = [
    dbc.DropdownMenuItem("Area of Forest land"),
]


image = 'grunge-paint-background.jpeg'
df = pd.read_csv('trials//allstates.csv',dtype={'Fips':'str'})
df = df[df.Year <= 2019]
#df = df[df.LandUse=='`0001 Timberland']
regionDict={}
for state in df.State.unique():
    print(state)
    regionDict[state] = df[df.State==state].Region.unique()
countyDict={}
for state in df.State.unique():
    countyDict[state] = df[df.State==state].CountyName.unique()
print(regionDict)
print(countyDict)
df['RegionEstimatedValue'] = df.groupby(['State','Region'])['EstimatedValue'].transform('sum')
df['Fips'] = df['Fips'].str.strip()
df2 = pd.read_csv('trials/allstates.csv',dtype={'Fips':'str'})
df2['Fips'] = df2['Fips'].str.strip()
county = df2.CountyName.unique()
df2.sort_values(by='Year',inplace=True)
overallState = df2.groupby(['State','Year']).sum('EstimatedValue').reset_index()
overallState['EstimatedValue'] = overallState.EstimatedValue.round(2)
overallRegions = df2.groupby(['State','Region','Year']).sum('EstimatedValue').reset_index()
overallRegions['EstimatedValue'] = overallRegions.EstimatedValue.round(2)
df2 = df2.astype({'Year':'int'})
print(df2.Year.unique())
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
  
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("FIA Data Mart", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),            
        ]
    ),
    color="dark",
    dark=True,
)

layout = html.Div([ 
    html.Div(     
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H5("Visualising forestry data across the country",className="text-center"),className = "mb-5 mt-5"),            
            ])
        ]),
        ),
    html.Div(
        dbc.Container([              
             dbc.Row([
                dbc.Col([
                    html.Div([
                        dcc.Dropdown(
                            id="states",
                            options=[                            
                                {'label': 'Georgia', 'value': 'Georgia'},
                                {'label': 'Alabama', 'value': 'Alabama'},
                                {'label': 'Florida', 'value': 'Florida'}
                                ],
                            className ="nav-link dropdown-toggle show",                        
                            placeholder="Select a state",                            
                            )],style = {'width' : '300%'}
                        ),
                    ],md=4)]),
            dbc.Row([            
                dbc.Col([
                html.Div([dcc.Dropdown(
                id="spatial",
                options=[
                    {'label': 'Statewide', 'value': 'State'},
                    {'label': 'Region/FIA-Unit wide', 'value': 'Region'},
                    {'label': 'Countywide', 'value': 'County'}
                ],
                className ="nav-link dropdown-toggle",
                placeholder="Spatial resolution",                
                )], style = {'width' : '300%'}       
                ),
                ],md=4),            
                ]),
            dbc.Row([            
                dbc.Col([                    
                html.Div([dcc.Dropdown(
                options=[
                    {'label': 'Area of Forest land', 'value': 'forest'},                
                ],
                className ="nav-link dropdown-toggle",
                value='forest',
                disabled=True
                )],  style = {'width' : '300%'}              
                )
                ],md=4),
            ]),
            html.Br(),               
            dbc.Row([
                dbc.Col([
                    html.Button('Visualise !!', id='viz', n_clicks=0,className = 'btn btn-success',style = {'width' : '300%'}),
                    ],md=4)
                    ])
                ,#html.Br(), html.Br(),                                              
            ]),
        style={'width': '20%', 'display': 'inline-block'}) ,
    
    html.Div(
        html.Div([
            html.Div(
                dbc.Container([
                    dbc.Row([
                        dbc.Col(dcc.Graph(id="choropleth"))
                        ])
                    ]),
                style={'width': '45%', 'display': 'inline-block'}),
            html.Div(
                dbc.Container([
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.Div([dcc.Dropdown(
                                id='regions',                    
                                clearable=False,                    
                            ),
                                ]),
                            html.Div([dcc.Dropdown(
                                id='counties', 
                                # options=[{'value': x, 'label': x} 
                                #           for x in county],
                                # value=county[0],
                                clearable=False,
                                #className ='nav-link dropdown-toggle'
                            ),
                                ]),
                            dcc.Graph(id="timeseries")
                            ])
                            ),
                        ])
                    ]),
                style={'width': '55%', 'display': 'inline-block'})
            
            
            ]),
        style={'width': '80%', 'display': 'inline-block'})
            
    ],style = {'background-image':image})

# Then we incorporate the snippet into our layout.
# This example keeps it simple and just wraps it in a Container
app.layout = html.Div([    
    navbar,
    layout
        
],
)


#print(regions["features"][0])
@app.callback(
    Output("choropleth", "figure"),
    #Output("timeseries","figure"),
    #Output("regions", "style"),
    [Input("viz","n_clicks")],
    [State("states","value")],
    [State("spatial","value")],
    #[State("regions","value")]
    )
def display_choropleth(n_clicks,state,spatial):    
    fig = px.choropleth(locationmode="USA-states", color=[1], scope="usa",template='plotly_dark')
    #fig2 = px.bar(df2[df2.State == state],x='Year',y='EstimatedValue')
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'viz' in changed_id and state == state and spatial == "State":
        print(state)
        fig = px.choropleth(df[df.State == state], geojson=counties, locations='Fips',                                     
                                     color_discrete_sequence = ["green"],                                
                                     scope="usa",
                                     template='plotly_dark',
                                     basemap_visible=False,
                                     #center={"lat":32.6836,"lon":-83.4644},
                                     hover_data = ["CountyName","EstimatedValue"],
                                     #labels={'EstimatedValue':'Estimated Value'},
                                     fitbounds='locations',
                                   )

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})             
    
    elif 'viz' in changed_id and state == state and spatial == "Region":        
        print(spatial)
        fig = px.choropleth(df[df.State == state], geojson=counties, locations='Fips',                                     
                                     color = "RegionEstimatedValue",                                
                                     scope="usa",
                                     template='plotly_dark',
                                     basemap_visible=False,
                                     #center={"lat":32.6836,"lon":-83.4644},
                                     color_continuous_scale = 'RdBu',                                
                                     hover_data = ["Region","RegionEstimatedValue"],                                     
                                     #labels={'EstimatedValue':'Estimated Value'},
                                     fitbounds='locations',                                     
                                   )
    
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        # fig.update_layout({"plot_bgcolor":"rgba(0,0,0,0)",
        #                    "paper_bgcolor":"rgba(0,0,0,0)"})        
        
    elif 'viz' in changed_id and state == state and spatial == "County":
        print(spatial)
        fig = px.choropleth(df[df.State == state], geojson=counties, locations='Fips',                                     
                                     color = "EstimatedValue",                                
                                     scope="usa",
                                     template='plotly_dark',
                                     basemap_visible=False,
                                     #center={"lat":32.6836,"lon":-83.4644},
                                     hover_data = ["CountyName","EstimatedValue"],                                    
                                     #labels={'CountyEstimatedValue':'Estimated Value'},
                                     fitbounds='locations',
                                   )

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        # fig.update_layout({"plot_bgcolor":"rgba(0,0,0,0)",
        #                    "paper_bgcolor":"rgba(0,0,0,0)"})
    
    fig.update_layout(autosize=True,
                      #coloraxis={'showscale':False},
                      legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
    return fig

@app.callback(    
    [Output("timeseries","figure"),
      Output("regions", "options"),
      Output("counties", "options"),
      Output("regions", "value"),
      Output("counties", "value"),
     Output("regions", "style"),
     Output("counties", "style")],
    [Input("viz","n_clicks")],
    [State("states","value")],
    [State("spatial","value")],
    [State("regions","value")],
    [State("counties", "value")]
    )
def display_timeseries(n_clicks,state,spatial,regions,county):
    style_dict_region = {'display': 'none'}        
    style_dict_county = {'display': 'none'}
    value_region=[{'label': i, 'value': i} for i in regionDict['Georgia']]
    value_county=[{'label': i, 'value': i} for i in countyDict['Georgia']]
    default_region=regionDict['Georgia'][0]
    default_county=countyDict['Georgia'][0]
    fig = px.choropleth(locationmode="USA-states", color=[1], scope="usa", template='plotly_dark')
    #fig2 = px.bar(df2[df2.State == state],x='Year',y='EstimatedValue')
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'viz' in changed_id and state == state and spatial == "State":
        print(state)        
        fig = px.line(overallState[overallState.State==state],x='Year',y='EstimatedValue',template='plotly_dark')                  
    
    elif 'viz' in changed_id and spatial == "Region":
        value_region = [{'label': i, 'value': i} for i in regionDict[state]]
        default_region = regions
        style_dict_region = {'display': 'inline-block','width':'100%'}
        style_dict_county = {'display': 'none'}
        print(spatial)
        fig = px.line(overallRegions.loc[(overallRegions.State == state) & (overallRegions.Region == regions)],x='Year',y='EstimatedValue',template='plotly_dark')        
        
    elif 'viz' in changed_id and spatial == "County":
        value_county = [{'label': i, 'value': i} for i in countyDict[state]]
        default_county = county
        style_dict_region = {'display': 'none'} 
        style_dict_county = {'display': 'inline-block','width':'100%'} 
        print(county)
        fig = px.line(df2.loc[(df2.State == state) & (df2.CountyName == county)],x='Year',y='EstimatedValue',template='plotly_dark')             
    return fig,value_region,value_county,default_region,default_county,style_dict_region,style_dict_county

# 5. Start the Dash server
if __name__ == "__main__":
    app.run_server(debug=True)
