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
app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
states = [
    dbc.DropdownMenuItem("Georgia"),
]
measures = [
    dbc.DropdownMenuItem("Area of Forest land"),
]

connection = sqlite3.connect('D:\\Study\\UGA\\SQLite_FIADB_GA\\FIADB_GA.db')
cursor=connection.cursor()
unitwise_Query = """select 'Georgia' as State,A.statecd || substr('00000' || A.rowstr,-3,3) as countycd,B.COUNTYNM , C.MEANING REGION,colstr,estimated_value from(
SELECT case 1 when 1 then '`0001 None`' end as pagestr, cond.statecd,cond.countycd as rowstr, 
case cond.cond_status_cd*100+coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0) 
when 101 then '`0001 Timberland' when 102 then '`0001 Timberland' when 103 then '`0001 Timberland' when 104 then '`0001 Timberland' when 105 then '`0001 Timberland' when 106 then '`0001 Timberland' when 107 then '`0003 Other forestland' when 111 then '`0002 Reserved Forestland' when 112 then '`0002 Reserved Forestland' when 113 then '`0002 Reserved Forestland' when 114 then '`0002 Reserved Forestland' when 115 then '`0002 Reserved Forestland' when 116 then '`0002 Reserved Forestland' when 117 then '`0002 Reserved Forestland' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),199) then '`0011 Forest (bad reservcd or siteclcd)' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),299) then '`0004 Nonforest' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),399) then '`0005 Non-Census water' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),499) then '`0006 Census water' else case cond.cond_nonsample_reasn_cd when 1 then '`0007 Outside U.S. boundary' when 2 then '`0008 Denied access' when 3 then '`0009 Hazardous' else '`0010 Other' end end as colstr, SUM((COALESCE(SCCM.SUBPTYP_PROP_CHNG / 4 * CASE COND.PROP_BASIS WHEN 'MACR' THEN POP_STRATUM.ADJ_FACTOR_MACR ELSE POP_STRATUM.ADJ_FACTOR_SUBP END, 0))*POP_STRATUM.EXPNS) AS ESTIMATED_VALUE FROM POP_STRATUM POP_STRATUM JOIN POP_PLOT_STRATUM_ASSGN POP_PLOT_STRATUM_ASSGN ON (POP_PLOT_STRATUM_ASSGN.STRATUM_CN = POP_STRATUM.CN) JOIN PLOT PLOT ON (POP_PLOT_STRATUM_ASSGN.PLT_CN = PLOT.CN) JOIN PLOTGEOM PLOTGEOM ON (PLOT.CN = PLOTGEOM.CN) JOIN COND COND ON (COND.PLT_CN = PLOT.CN) JOIN COND PCOND ON (PCOND.PLT_CN = PLOT.PREV_PLT_CN) JOIN SUBP_COND_CHNG_MTRX SCCM ON (SCCM.PLT_CN = COND.PLT_CN AND SCCM.PREV_PLT_CN = PCOND.PLT_CN AND SCCM.CONDID = COND.CONDID AND SCCM.PREVCOND = PCOND.CONDID) WHERE COND.CONDPROP_UNADJ IS NOT NULL AND ((SCCM.SUBPTYP = 3 AND COND.PROP_BASIS = 'MACR') OR (SCCM.SUBPTYP = 1 AND COND.PROP_BASIS = 'SUBP')) AND COALESCE(COND.COND_NONSAMPLE_REASN_CD, 0) = 0 AND COALESCE(PCOND.COND_NONSAMPLE_REASN_CD, 0) = 0 AND (COND.COND_STATUS_CD = 1 AND PCOND.COND_STATUS_CD = 1) AND ((pop_stratum.rscd=33 and pop_stratum.evalid=131903)) and 1=1 GROUP BY case 1 when 1 then '`0001 None`' end,cond.statecd,cond.countycd ,case cond.cond_status_cd*100+coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0) when 101 then '`0001 Timberland' when 102 then '`0001 Timberland' when 103 then '`0001 Timberland' when 104 then '`0001 Timberland' when 105 then '`0001 Timberland' when 106 then '`0001 Timberland' when 107 then '`0003 Other forestland' when 111 then '`0002 Reserved Forestland' when 112 then '`0002 Reserved Forestland' when 113 then '`0002 Reserved Forestland' when 114 then '`0002 Reserved Forestland' when 115 then '`0002 Reserved Forestland' when 116 then '`0002 Reserved Forestland' when 117 then '`0002 Reserved Forestland' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),199) then '`0011 Forest (bad reservcd or siteclcd)' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),299) then '`0004 Nonforest' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),399) then '`0005 Non-Census water' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),499) then '`0006 Census water' else case cond.cond_nonsample_reasn_cd when 1 then '`0007 Outside U.S. boundary' when 2 then '`0008 Denied access' when 3 then '`0009 Hazardous' else '`0010 Other' end end 
) A LEFT JOIN COUNTY B ON A.ROWSTR = B.COUNTYCD
LEFT JOIN REF_UNIT C ON B.UNITCD = C.VALUE; 
"""
yearwise_Query = """ select 'Georgia' as State,A.statecd || substr('00000' || A.rowstr,-3,3) as countycd,B.COUNTYNM , C.MEANING REGION,colstr as Year,estimated_value from(
SELECT case 1 when 1 then '`0001 None`' end as pagestr, cond.statecd, cond.countycd as rowstr, case coalesce(plot.invyr, 0) when 2030 then '`0001 2030' when 2029 then '`0002 2029' when 2028 then '`0003 2028' when 2027 then '`0004 2027' when 2026 then '`0005 2026' when 2025 then '`0006 2025' when 2024 then '`0007 2024' when 2023 then '`0008 2023' when 2022 then '`0009 2022' when 2021 then '`0010 2021' when 2020 then '`0011 2020' when 2019 then '`0012 2019' when 2018 then '`0013 2018' when 2017 then '`0014 2017' when 2016 then '`0015 2016' when 2015 then '`0016 2015' when 2014 then '`0017 2014' when 2013 then '`0018 2013' when 2012 then '`0019 2012' when 2011 then '`0020 2011' when 2010 then '`0021 2010' when 2009 then '`0022 2009' when 2008 then '`0023 2008' when 2007 then '`0024 2007' when 2006 then '`0025 2006' when 2005 then '`0026 2005' when 2004 then '`0027 2004' when 2003 then '`0028 2003' when 2002 then '`0029 2002' when 2001 then '`0030 2001' when 2000 then '`0031 2000' when 1999 then '`0032 1999' when 1998 then '`0033 1998' when 1997 then '`0034 1997' when 1996 then '`0035 1996' when 1995 then '`0036 1995' when 1994 then '`0037 1994' when 1993 then '`0038 1993' when 1992 then '`0039 1992' when 1991 then '`0040 1991' when 1990 then '`0041 1990' when 1989 then '`0042 1989' when 1988 then '`0043 1988' when 1987 then '`0044 1987' when 1986 then '`0045 1986' when 1985 then '`0046 1985' when 1984 then '`0047 1984' when 1983 then '`0048 1983' when 1982 then '`0049 1982' when 1981 then '`0050 1981' when 1980 then '`0051 1980' else '`0023 Other' end as colstr, SUM((COALESCE(SCCM.SUBPTYP_PROP_CHNG / 4 * CASE COND.PROP_BASIS WHEN 'MACR' THEN POP_STRATUM.ADJ_FACTOR_MACR ELSE POP_STRATUM.ADJ_FACTOR_SUBP END, 0))*POP_STRATUM.EXPNS) AS ESTIMATED_VALUE FROM POP_STRATUM POP_STRATUM JOIN POP_PLOT_STRATUM_ASSGN POP_PLOT_STRATUM_ASSGN ON (POP_PLOT_STRATUM_ASSGN.STRATUM_CN = POP_STRATUM.CN) JOIN PLOT PLOT ON (POP_PLOT_STRATUM_ASSGN.PLT_CN = PLOT.CN) JOIN PLOTGEOM PLOTGEOM ON (PLOT.CN = PLOTGEOM.CN) JOIN COND COND ON (COND.PLT_CN = PLOT.CN) JOIN COND PCOND ON (PCOND.PLT_CN = PLOT.PREV_PLT_CN) JOIN SUBP_COND_CHNG_MTRX SCCM ON (SCCM.PLT_CN = COND.PLT_CN AND SCCM.PREV_PLT_CN = PCOND.PLT_CN AND SCCM.CONDID = COND.CONDID AND SCCM.PREVCOND = PCOND.CONDID) WHERE COND.CONDPROP_UNADJ IS NOT NULL AND ((SCCM.SUBPTYP = 3 AND COND.PROP_BASIS = 'MACR') OR (SCCM.SUBPTYP = 1 AND COND.PROP_BASIS = 'SUBP')) AND COALESCE(COND.COND_NONSAMPLE_REASN_CD, 0) = 0 AND COALESCE(PCOND.COND_NONSAMPLE_REASN_CD, 0) = 0 AND (COND.COND_STATUS_CD = 1 AND PCOND.COND_STATUS_CD = 1) AND ((pop_stratum.rscd=33 and pop_stratum.evalid=131903)) and 1=1 GROUP BY case 1 when 1 then '`0001 None`' end,cond.statecd,cond.countycd ,case coalesce(plot.invyr, 0) when 2030 then '`0001 2030' when 2029 then '`0002 2029' when 2028 then '`0003 2028' when 2027 then '`0004 2027' when 2026 then '`0005 2026' when 2025 then '`0006 2025' when 2024 then '`0007 2024' when 2023 then '`0008 2023' when 2022 then '`0009 2022' when 2021 then '`0010 2021' when 2020 then '`0011 2020' when 2019 then '`0012 2019' when 2018 then '`0013 2018' when 2017 then '`0014 2017' when 2016 then '`0015 2016' when 2015 then '`0016 2015' when 2014 then '`0017 2014' when 2013 then '`0018 2013' when 2012 then '`0019 2012' when 2011 then '`0020 2011' when 2010 then '`0021 2010' when 2009 then '`0022 2009' when 2008 then '`0023 2008' when 2007 then '`0024 2007' when 2006 then '`0025 2006' when 2005 then '`0026 2005' when 2004 then '`0027 2004' when 2003 then '`0028 2003' when 2002 then '`0029 2002' when 2001 then '`0030 2001' when 2000 then '`0031 2000' when 1999 then '`0032 1999' when 1998 then '`0033 1998' when 1997 then '`0034 1997' when 1996 then '`0035 1996' when 1995 then '`0036 1995' when 1994 then '`0037 1994' when 1993 then '`0038 1993' when 1992 then '`0039 1992' when 1991 then '`0040 1991' when 1990 then '`0041 1990' when 1989 then '`0042 1989' when 1988 then '`0043 1988' when 1987 then '`0044 1987' when 1986 then '`0045 1986' when 1985 then '`0046 1985' when 1984 then '`0047 1984' when 1983 then '`0048 1983' when 1982 then '`0049 1982' when 1981 then '`0050 1981' when 1980 then '`0051 1980' else '`0023 Other' end
) A LEFT JOIN COUNTY B ON A.ROWSTR = B.COUNTYCD
LEFT JOIN REF_UNIT C ON B.UNITCD = C.VALUE
"""

cursor.execute(unitwise_Query)
unitwise = cursor.fetchall()
df = pd.DataFrame(unitwise,columns=['State','Fips','CountyName','Region','=-' ,'EstimatedValue'])
#df = df[df.LandUse=='`0001 Timberland']
regions = df.Region.unique()
df['CountyEstimatedValue'] = df.groupby(['State','Fips','CountyName','Region'])['EstimatedValue'].transform('sum')
df['RegionEstimatedValue'] = df.groupby(['Region'])['EstimatedValue'].transform('sum')

cursor.execute(yearwise_Query)
yearwise = cursor.fetchall()
df2 = pd.DataFrame(yearwise,columns=['State','Fips','CountyName','Region','Year' ,'EstimatedValue'])
county = df2.CountyName.unique()
df2[['Dummy','Year']] = df2['Year'].str.split(expand=True)
overallState = df2.groupby(['State','Year']).sum('EstimatedValue').reset_index()
overallRegions = df2.groupby(['State','Region','Year']).sum('EstimatedValue').reset_index()
connection.close()


#geodf = gpd.read_file('D:\\Study\\UGA\\Spring 2022\\Dr.Dwivedi\\cb_2018_us_region_500k\\cb_2018_us_region_500k.shp')
#geodf.to_file("D:\\Study\\UGA\\Spring 2022\\Dr.Dwivedi\\usa_regions.json", driver = "GeoJSON")
# with open('D:\\Study\\UGA\\Spring 2022\\Dr.Dwivedi\\cb_2018_us_region_500k.geojson') as geofile:
#     regions = json.load(geofile)
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
            dbc.Col(html.Div([dcc.Dropdown(
            id="states",
            options=[
                {'label': 'Georgia', 'value': 'Georgia'},
                {'label': 'Alabama', 'value': 'Alabama'},
                {'label': 'Florida', 'value': 'Florida'}
            ],
            className ="nav-link dropdown-toggle",
            placeholder="Select a state",
            )],
            #style={"display": "flex", "flexWrap": "wrap","width":"20%","margin-left":"10px"}
            )
                    ),
            ]),
        html.Br(),       
        dbc.Row([
            dbc.Col(html.Div([dcc.Dropdown(
            id="spatial",
            options=[
                {'label': 'Statewide', 'value': 'State'},
                {'label': 'Region/FIA-Unit wide', 'value': 'Region'},
                {'label': 'Countywide', 'value': 'County'}
            ],
            className ="nav-link dropdown-toggle",
            placeholder="Spatial resolution",
            )],
            #style={"display": "flex", "flexWrap": "wrap","width":"20%","margin-left":"10px"}
            )
                    ),
            
            dbc.Col(html.Div([dcc.Dropdown(
            options=[
                {'label': 'Area of Forest land', 'value': 'forest'},                
            ],
            className ="nav-link dropdown-toggle",
            value='forest',
            disabled=True
            )],
            #style={"display": "flex", "flexWrap": "wrap","width":"20%","margin-left":"10px"}
            )
                    )
            ],justify="center"),
        dbc.Row([html.Button('Visualise !!', id='viz', n_clicks=0),
            ]),html.Br(), html.Br(),       
        dbc.Row([
            dbc.Col(dcc.Graph(id="choropleth")),
            dbc.Col(html.Div([
                html.Div([dcc.Dropdown(
                    id='regions', 
                    options=[{'value': x, 'label': x} 
                              for x in regions],
                    value=regions[0],
                    clearable=False
                ),
                    ]),
                html.Div([dcc.Dropdown(
                    id='counties', 
                    options=[{'value': x, 'label': x} 
                              for x in county],
                    value=county[0],
                    clearable=False
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
    fig = px.choropleth(locationmode="USA-states", color=[1], scope="usa")
    #fig2 = px.bar(df2[df2.State == state],x='Year',y='EstimatedValue')
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'viz' in changed_id and state == "Georgia" and spatial == "State":
        print(state)
        fig = px.choropleth(df[df.State == state], geojson=counties, locations='Fips',                                     
                                     color_discrete_sequence = ["green"],                                
                                     scope="usa",
                                     basemap_visible=False,
                                     center={"lat":32.6836,"lon":-83.4644},
                                     hover_data = ["CountyName","CountyEstimatedValue"],
                                     #labels={'EstimatedValue':'Estimated Value'},
                                     fitbounds='locations',
                                   )

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_layout({"plot_bgcolor":"rgba(0,0,0,0)",
                           "paper_bgcolor":"rgba(0,0,0,0)"})        
    
    elif 'viz' in changed_id and state == "Georgia" and spatial == "Region":        
        print(spatial)
        fig = px.choropleth(df, geojson=counties, locations='Fips',                                     
                                     color = "RegionEstimatedValue",                                
                                     scope="usa",
                                     basemap_visible=False,
                                     center={"lat":32.6836,"lon":-83.4644},
                                     hover_data = ["CountyName","CountyEstimatedValue"],
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
    fig = px.choropleth(locationmode="USA-states", color=[1], scope="usa")
    #fig2 = px.bar(df2[df2.State == state],x='Year',y='EstimatedValue')
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'viz' in changed_id and state == "Georgia" and spatial == "State":
        print(state)
        fig = px.line(overallState,x='Year',y='EstimatedValue')        
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_layout({"plot_bgcolor":"rgba(0,0,0,0)",
                           "paper_bgcolor":"rgba(0,0,0,0)"})        
    
    elif 'viz' in changed_id and state == "Georgia" and spatial == "Region":
        style_dict_region = {'display': 'block'}
        style_dict_county = {'display': 'none'} 
        print(spatial)
        fig = px.line(overallRegions[overallRegions.Region == regions],x='Year',y='EstimatedValue')           
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_layout({"plot_bgcolor":"rgba(0,0,0,0)",
                           "paper_bgcolor":"rgba(0,0,0,0)"})        
        
    elif 'viz' in changed_id and state == "Georgia" and spatial == "County":
        style_dict_region = {'display': 'none'} 
        style_dict_county = {'display': 'block'} 
        print(county)
        fig = px.line(df2[df2.CountyName == county],x='Year',y='EstimatedValue') 
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_layout({"plot_bgcolor":"rgba(0,0,0,0)",
                           "paper_bgcolor":"rgba(0,0,0,0)"})        
    return fig,style_dict_region,style_dict_county
    #return {'display': 'block'},fig

# @app.callback(    
#     Output("region", "style"),
#     [Input("viz","n_clicks")],
#     [State("states","value")],
#     [State("spatial","value")]  
#     )
# def enable_regions(n_clicks,state,spatial):
#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     if 'viz' in changed_id and state == "Georgia" and spatial == "Region":    
#         return {"display":"block"}
#     else:
#         return {"display":"none"}

# 5. Start the Dash server
if __name__ == "__main__":
    app.run_server()