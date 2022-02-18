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
import geopandas as gpd


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

df = pd.read_csv('unitWise.csv')
#df = df[df.LandUse=='`0001 Timberland']
regions = df.Region.unique()
df['CountyEstimatedValue'] = df.groupby(['State','Fips','CountyName','Region'])['EstimatedValue'].transform('sum')
df['RegionEstimatedValue'] = df.groupby(['Region'])['EstimatedValue'].transform('sum')

df2 = pd.read_csv('yearWise.csv')
county = df2.CountyName.unique()
df2[['Dummy','Year']] = df2['Year'].str.split(expand=True)
overallState = df2.groupby(['State','Year']).sum('EstimatedValue').reset_index()
overallRegions = df2.groupby(['State','Region','Year']).sum('EstimatedValue').reset_index()

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
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H5("Visualising forestry data across the country",className="text-center"),className = "mb-5 mt-5"),            
            ]),
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
                        )],#style = {'left':'0px','width':'200px' }
                    ),
                ],md=4),
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
                )], #style = {'left':'0px','width':'200px' }       
                ),
                ],md=4),
                dbc.Col([                    
                html.Div([dcc.Dropdown(
                options=[
                    {'label': 'Area of Forest land', 'value': 'forest'},                
                ],
                className ="nav-link dropdown-toggle",
                value='forest',
                disabled=True
                )],  #style = {'left':'0px','width':'200px' }                
                )
                ],md=4),
            ]),
        html.Br(),               
        dbc.Row([
            dbc.Col([
                html.Button('Visualise !!', id='viz', n_clicks=0,className = 'btn btn-success'),
                ],md=2)
                ],justify='center')
            ,html.Br(), html.Br(),       
        dbc.Row([
            dbc.Col(dcc.Graph(id="choropleth")),
            dbc.Col(html.Div([
                html.Div([dcc.Dropdown(
                    id='regions', 
                    options=[{'value': x, 'label': x} 
                              for x in regions],
                    value=regions[0],
                    clearable=False,
                    className ='nav-link dropdown-toggle'
                ),
                    ]),
                html.Div([dcc.Dropdown(
                    id='counties', 
                    options=[{'value': x, 'label': x} 
                              for x in county],
                    value=county[0],
                    clearable=False,
                    className ='nav-link dropdown-toggle'
                ),
                    ]),
                dcc.Graph(id="timeseries")
                ])
                ), 
            ])
                       
        ]),            
    ])

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
    if 'viz' in changed_id and state == "Georgia" and spatial == "State":
        print(state)
        fig = px.choropleth(df[df.State == state], geojson=counties, locations='Fips',                                     
                                     color_discrete_sequence = ["green"],                                
                                     scope="usa",
                                     template='plotly_dark',
                                     basemap_visible=False,
                                     center={"lat":32.6836,"lon":-83.4644},
                                     hover_data = ["CountyName","CountyEstimatedValue"],
                                     #labels={'EstimatedValue':'Estimated Value'},
                                     fitbounds='locations',
                                   )

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})             
    
    elif 'viz' in changed_id and state == "Georgia" and spatial == "Region":        
        print(spatial)
        fig = px.choropleth(df, geojson=counties, locations='Fips',                                     
                                     color = "RegionEstimatedValue",                                
                                     scope="usa",
                                     template='plotly_dark',
                                     basemap_visible=False,
                                     center={"lat":32.6836,"lon":-83.4644},
                                     hover_data = ["Region","RegionEstimatedValue"],                                     
                                     #labels={'EstimatedValue':'Estimated Value'},
                                     fitbounds='locations',                                   
                                   )
    
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_layout({"plot_bgcolor":"rgba(0,0,0,0)",
                           "paper_bgcolor":"rgba(0,0,0,0)"})        
        
    elif 'viz' in changed_id and state == "Georgia" and spatial == "County":
        print(spatial)
        fig = px.choropleth(df[df.State == state], geojson=counties, locations='Fips',                                     
                                     color = "CountyEstimatedValue",                                
                                     scope="usa",
                                     template='plotly_dark',
                                     basemap_visible=False,
                                     center={"lat":32.6836,"lon":-83.4644},
                                     hover_data = ["CountyName","CountyEstimatedValue"],                                    
                                     #labels={'CountyEstimatedValue':'Estimated Value'},
                                     fitbounds='locations',
                                   )

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_layout({"plot_bgcolor":"rgba(0,0,0,0)",
                           "paper_bgcolor":"rgba(0,0,0,0)"})
    
    fig.update_layout(autosize=True,coloraxis={'showscale':False},legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
    return fig

@app.callback(    
    [Output("timeseries","figure"),
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
    fig = px.choropleth(locationmode="USA-states", color=[1], scope="usa", template='plotly_dark')
    #fig2 = px.bar(df2[df2.State == state],x='Year',y='EstimatedValue')
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'viz' in changed_id and state == "Georgia" and spatial == "State":
        print(state)
        fig = px.line(overallState,x='Year',y='EstimatedValue',template='plotly_dark')                  
    
    elif 'viz' in changed_id and state == "Georgia" and spatial == "Region":
        style_dict_region = {'display': 'block'}
        style_dict_county = {'display': 'none'} 
        print(spatial)
        fig = px.line(overallRegions[overallRegions.Region == regions],x='Year',y='EstimatedValue',template='plotly_dark')        
        
    elif 'viz' in changed_id and state == "Georgia" and spatial == "County":
        style_dict_region = {'display': 'none'} 
        style_dict_county = {'display': 'block'} 
        print(county)
        fig = px.line(df2[df2.CountyName == county],x='Year',y='EstimatedValue',template='plotly_dark')             
    return fig,style_dict_region,style_dict_county    

# 5. Start the Dash server
if __name__ == "__main__":
    app.run_server(debug=True)
