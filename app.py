# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 23:56:31 2022

@author: basus
"""

import os
from urllib.request import urlopen
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import sqlite3

# ------------------------------------------------------ APP ------------------------------------------------------
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#EBEBEB',
    'text': '#030626'
}

connection = sqlite3.connect('D:\\Study\\UGA\\SQLite_FIADB_GA\\FIADB_GA.db')

print(connection.total_changes)
cursor=connection.cursor()
cursor.execute("select sum(estimated_value)from (SELECT case 1 when 1 then '`0001 None`' end as pagestr, case cond.owncd when 11 then '`0001 National Forest' when 12 then '`0001 National Forest' when 13 then '`0001 National Forest' when 21 then '`0002 National Park Service' when 22 then '`0003 Bureau of Land Mgmt' when 23 then '`0004 Fish and Wildlife Service' when 24 then '`0005 Dept of Defense' when 25 then '`0006 Other federal' when 31 then '`0007 State' when 32 then '`0008 County and Municipal' when 33 then '`0009 Other local govt' when 41 then '`0010 Private' when 42 then '`0010 Private' when 43 then '`0010 Private' when 44 then '`0010 Private' when 45 then '`0010 Private' when 46 then '`0010 Private' when -1 then '`0011 Unavailable' else '`0012 Other' end as rowstr, case cond.cond_status_cd*100+coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0) when 101 then '`0001 Timberland' when 102 then '`0001 Timberland' when 103 then '`0001 Timberland' when 104 then '`0001 Timberland' when 105 then '`0001 Timberland' when 106 then '`0001 Timberland' when 107 then '`0003 Other forestland' when 111 then '`0002 Reserved Forestland' when 112 then '`0002 Reserved Forestland' when 113 then '`0002 Reserved Forestland' when 114 then '`0002 Reserved Forestland' when 115 then '`0002 Reserved Forestland' when 116 then '`0002 Reserved Forestland' when 117 then '`0002 Reserved Forestland' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),199) then '`0011 Forest (bad reservcd or siteclcd)' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),299) then '`0004 Nonforest' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),399) then '`0005 Non-Census water' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),499) then '`0006 Census water' else case cond.cond_nonsample_reasn_cd when 1 then '`0007 Outside U.S. boundary' when 2 then '`0008 Denied access' when 3 then '`0009 Hazardous' else '`0010 Other' end end as colstr, SUM((COND.CONDPROP_UNADJ * CASE COND.PROP_BASIS WHEN 'MACR' THEN POP_STRATUM.ADJ_FACTOR_MACR ELSE POP_STRATUM.ADJ_FACTOR_SUBP END)*POP_STRATUM.EXPNS) AS ESTIMATED_VALUE FROM POP_STRATUM POP_STRATUM JOIN POP_PLOT_STRATUM_ASSGN ON (POP_PLOT_STRATUM_ASSGN.STRATUM_CN = POP_STRATUM.CN) JOIN PLOT ON (POP_PLOT_STRATUM_ASSGN.PLT_CN = PLOT.CN) JOIN PLOTGEOM ON (PLOT.CN = PLOTGEOM.CN) JOIN COND ON (COND.PLT_CN = PLOT.CN) WHERE COND.COND_STATUS_CD = 1 AND COND.CONDPROP_UNADJ IS NOT NULL AND ((pop_stratum.rscd=33 and pop_stratum.evalid=131901)) and 1=1 GROUP BY case 1 when 1 then '`0001 None`' end,case cond.owncd when 11 then '`0001 National Forest' when 12 then '`0001 National Forest' when 13 then '`0001 National Forest' when 21 then '`0002 National Park Service' when 22 then '`0003 Bureau of Land Mgmt' when 23 then '`0004 Fish and Wildlife Service' when 24 then '`0005 Dept of Defense' when 25 then '`0006 Other federal' when 31 then '`0007 State' when 32 then '`0008 County and Municipal' when 33 then '`0009 Other local govt' when 41 then '`0010 Private' when 42 then '`0010 Private' when 43 then '`0010 Private' when 44 then '`0010 Private' when 45 then '`0010 Private' when 46 then '`0010 Private' when -1 then '`0011 Unavailable' else '`0012 Other' end ,case cond.cond_status_cd*100+coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0) when 101 then '`0001 Timberland' when 102 then '`0001 Timberland' when 103 then '`0001 Timberland' when 104 then '`0001 Timberland' when 105 then '`0001 Timberland' when 106 then '`0001 Timberland' when 107 then '`0003 Other forestland' when 111 then '`0002 Reserved Forestland' when 112 then '`0002 Reserved Forestland' when 113 then '`0002 Reserved Forestland' when 114 then '`0002 Reserved Forestland' when 115 then '`0002 Reserved Forestland' when 116 then '`0002 Reserved Forestland' when 117 then '`0002 Reserved Forestland' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),199) then '`0011 Forest (bad reservcd or siteclcd)' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),299) then '`0004 Nonforest' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),399) then '`0005 Non-Census water' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),499) then '`0006 Census water' else case cond.cond_nonsample_reasn_cd when 1 then '`0007 Outside U.S. boundary' when 2 then '`0008 Denied access' when 3 then '`0009 Hazardous' else '`0010 Other' end end )")
totalacre = cursor.fetchone()

unitwise_Query = """SELECT rowstr,sum(estimated_value) from (
SELECT case 1 when 1 then '`0001 None`' end as pagestr, case cond.owncd when 11 then '`0001 National Forest' when 12 then '`0001 National Forest' when 13 then '`0001 National Forest' when 21 then '`0002 National Park Service' when 22 then '`0003 Bureau of Land Mgmt' when 23 then '`0004 Fish and Wildlife Service' when 24 then '`0005 Dept of Defense' when 25 then '`0006 Other federal' when 31 then '`0007 State' when 32 then '`0008 County and Municipal' when 33 then '`0009 Other local govt' when 41 then '`0010 Private' when 42 then '`0010 Private' when 43 then '`0010 Private' when 44 then '`0010 Private' when 45 then '`0010 Private' when 46 then '`0010 Private' when -1 then '`0011 Unavailable' else '`0012 Other' end as rowstr, case cond.cond_status_cd*100+coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0) when 101 then '`0001 Timberland' when 102 then '`0001 Timberland' when 103 then '`0001 Timberland' when 104 then '`0001 Timberland' when 105 then '`0001 Timberland' when 106 then '`0001 Timberland' when 107 then '`0003 Other forestland' when 111 then '`0002 Reserved Forestland' when 112 then '`0002 Reserved Forestland' when 113 then '`0002 Reserved Forestland' when 114 then '`0002 Reserved Forestland' when 115 then '`0002 Reserved Forestland' when 116 then '`0002 Reserved Forestland' when 117 then '`0002 Reserved Forestland' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),199) then '`0011 Forest (bad reservcd or siteclcd)' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),299) then '`0004 Nonforest' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),399) then '`0005 Non-Census water' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),499) then '`0006 Census water' else case cond.cond_nonsample_reasn_cd when 1 then '`0007 Outside U.S. boundary' when 2 then '`0008 Denied access' when 3 then '`0009 Hazardous' else '`0010 Other' end end as colstr, SUM((COND.CONDPROP_UNADJ * CASE COND.PROP_BASIS WHEN 'MACR' THEN POP_STRATUM.ADJ_FACTOR_MACR ELSE POP_STRATUM.ADJ_FACTOR_SUBP END)*POP_STRATUM.EXPNS) AS ESTIMATED_VALUE FROM POP_STRATUM POP_STRATUM JOIN POP_PLOT_STRATUM_ASSGN ON (POP_PLOT_STRATUM_ASSGN.STRATUM_CN = POP_STRATUM.CN) JOIN PLOT ON (POP_PLOT_STRATUM_ASSGN.PLT_CN = PLOT.CN) JOIN PLOTGEOM ON (PLOT.CN = PLOTGEOM.CN) JOIN COND ON (COND.PLT_CN = PLOT.CN) WHERE COND.COND_STATUS_CD = 1 AND COND.CONDPROP_UNADJ IS NOT NULL AND ((pop_stratum.rscd=33 and pop_stratum.evalid=131901)) and 1=1 GROUP BY case 1 when 1 then '`0001 None`' end,case cond.owncd when 11 then '`0001 National Forest' when 12 then '`0001 National Forest' when 13 then '`0001 National Forest' when 21 then '`0002 National Park Service' when 22 then '`0003 Bureau of Land Mgmt' when 23 then '`0004 Fish and Wildlife Service' when 24 then '`0005 Dept of Defense' when 25 then '`0006 Other federal' when 31 then '`0007 State' when 32 then '`0008 County and Municipal' when 33 then '`0009 Other local govt' when 41 then '`0010 Private' when 42 then '`0010 Private' when 43 then '`0010 Private' when 44 then '`0010 Private' when 45 then '`0010 Private' when 46 then '`0010 Private' when -1 then '`0011 Unavailable' else '`0012 Other' end ,case cond.cond_status_cd*100+coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0) when 101 then '`0001 Timberland' when 102 then '`0001 Timberland' when 103 then '`0001 Timberland' when 104 then '`0001 Timberland' when 105 then '`0001 Timberland' when 106 then '`0001 Timberland' when 107 then '`0003 Other forestland' when 111 then '`0002 Reserved Forestland' when 112 then '`0002 Reserved Forestland' when 113 then '`0002 Reserved Forestland' when 114 then '`0002 Reserved Forestland' when 115 then '`0002 Reserved Forestland' when 116 then '`0002 Reserved Forestland' when 117 then '`0002 Reserved Forestland' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),199) then '`0011 Forest (bad reservcd or siteclcd)' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),299) then '`0004 Nonforest' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),399) then '`0005 Non-Census water' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),499) then '`0006 Census water' else case cond.cond_nonsample_reasn_cd when 1 then '`0007 Outside U.S. boundary' when 2 then '`0008 Denied access' when 3 then '`0009 Hazardous' else '`0010 Other' end end
)group by rowstr;
"""
cursor.execute(unitwise_Query)
unitwise = cursor.fetchall()
df = pd.DataFrame(unitwise,columns=['Unit','Acreage'])

forest_type = """ select B.MEANING,A.colstr,A.sum_estimated_value
from
(select pagestr,rowstr,colstr,sum(estimated_value) as sum_estimated_value from (SELECT case 1 when 1 then '`0001 None`' end as pagestr, cond.fortypcd as rowstr, case coalesce(cond.siteclcd,-1) when 1 then '`0001 225+' when 2 then '`0002 165-224' when 3 then '`0003 120-164' when 4 then '`0004 85-119' when 5 then '`0005 50-84' when 6 then '`0006 20-49' when 7 then '`0007 0-19' when -1 then '`0008 Not available' else '`0009 Other' end as colstr, SUM((COND.CONDPROP_UNADJ * CASE COND.PROP_BASIS WHEN 'MACR' THEN POP_STRATUM.ADJ_FACTOR_MACR ELSE POP_STRATUM.ADJ_FACTOR_SUBP END)*POP_STRATUM.EXPNS) AS ESTIMATED_VALUE FROM POP_STRATUM POP_STRATUM JOIN POP_PLOT_STRATUM_ASSGN ON (POP_PLOT_STRATUM_ASSGN.STRATUM_CN = POP_STRATUM.CN) JOIN PLOT ON (POP_PLOT_STRATUM_ASSGN.PLT_CN = PLOT.CN) JOIN PLOTGEOM ON (PLOT.CN = PLOTGEOM.CN) JOIN COND ON (COND.PLT_CN = PLOT.CN) WHERE COND.COND_STATUS_CD = 1 AND COND.CONDPROP_UNADJ IS NOT NULL AND ((pop_stratum.rscd=33 and pop_stratum.evalid=131901)) and 1=1 GROUP BY case 1 when 1 then '`0001 None`' end,cond.fortypcd ,case coalesce(cond.siteclcd,-1) when 1 then '`0001 225+' when 2 then '`0002 165-224' when 3 then '`0003 120-164' when 4 then '`0004 85-119' when 5 then '`0005 50-84' when 6 then '`0006 20-49' when 7 then '`0007 0-19' when -1 then '`0008 Not available' else '`0009 Other' end ) tmpzzz group by pagestr,rowstr,colstr order by pagestr, rowstr, colstr) A
LEFT JOIN (SELECT MEANING,VALUE FROM REF_FOREST_TYPE) B ON A.rowstr = B.VALUE; """

cursor.execute(forest_type)
forest = cursor.fetchall()
df_2 = pd.DataFrame(forest,columns=['ForestType','SiteProductivity','Acreage'])
df_2.reset_index(inplace=True)
ftype = df_2.ForestType.unique()

unitMap_Query = """select A.statecd || substr('00000' || A.rowstr,-3,3) as countycd,B.COUNTYNM , C.MEANING REGION,colstr,estimated_value from(
SELECT case 1 when 1 then '`0001 None`' end as pagestr, cond.statecd,cond.countycd as rowstr, case cond.cond_status_cd*100+coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0) when 101 then '`0001 Timberland' when 102 then '`0001 Timberland' when 103 then '`0001 Timberland' when 104 then '`0001 Timberland' when 105 then '`0001 Timberland' when 106 then '`0001 Timberland' when 107 then '`0003 Other forestland' when 111 then '`0002 Reserved Forestland' when 112 then '`0002 Reserved Forestland' when 113 then '`0002 Reserved Forestland' when 114 then '`0002 Reserved Forestland' when 115 then '`0002 Reserved Forestland' when 116 then '`0002 Reserved Forestland' when 117 then '`0002 Reserved Forestland' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),199) then '`0011 Forest (bad reservcd or siteclcd)' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),299) then '`0004 Nonforest' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),399) then '`0005 Non-Census water' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),499) then '`0006 Census water' else case cond.cond_nonsample_reasn_cd when 1 then '`0007 Outside U.S. boundary' when 2 then '`0008 Denied access' when 3 then '`0009 Hazardous' else '`0010 Other' end end as colstr, SUM((COALESCE(SCCM.SUBPTYP_PROP_CHNG / 4 * CASE COND.PROP_BASIS WHEN 'MACR' THEN POP_STRATUM.ADJ_FACTOR_MACR ELSE POP_STRATUM.ADJ_FACTOR_SUBP END, 0))*POP_STRATUM.EXPNS) AS ESTIMATED_VALUE FROM POP_STRATUM POP_STRATUM JOIN POP_PLOT_STRATUM_ASSGN POP_PLOT_STRATUM_ASSGN ON (POP_PLOT_STRATUM_ASSGN.STRATUM_CN = POP_STRATUM.CN) JOIN PLOT PLOT ON (POP_PLOT_STRATUM_ASSGN.PLT_CN = PLOT.CN) JOIN PLOTGEOM PLOTGEOM ON (PLOT.CN = PLOTGEOM.CN) JOIN COND COND ON (COND.PLT_CN = PLOT.CN) JOIN COND PCOND ON (PCOND.PLT_CN = PLOT.PREV_PLT_CN) JOIN SUBP_COND_CHNG_MTRX SCCM ON (SCCM.PLT_CN = COND.PLT_CN AND SCCM.PREV_PLT_CN = PCOND.PLT_CN AND SCCM.CONDID = COND.CONDID AND SCCM.PREVCOND = PCOND.CONDID) WHERE COND.CONDPROP_UNADJ IS NOT NULL AND ((SCCM.SUBPTYP = 3 AND COND.PROP_BASIS = 'MACR') OR (SCCM.SUBPTYP = 1 AND COND.PROP_BASIS = 'SUBP')) AND COALESCE(COND.COND_NONSAMPLE_REASN_CD, 0) = 0 AND COALESCE(PCOND.COND_NONSAMPLE_REASN_CD, 0) = 0 AND (COND.COND_STATUS_CD = 1 AND PCOND.COND_STATUS_CD = 1) AND ((pop_stratum.rscd=33 and pop_stratum.evalid=131903)) and 1=1 GROUP BY case 1 when 1 then '`0001 None`' end,cond.statecd,cond.countycd ,case cond.cond_status_cd*100+coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0) when 101 then '`0001 Timberland' when 102 then '`0001 Timberland' when 103 then '`0001 Timberland' when 104 then '`0001 Timberland' when 105 then '`0001 Timberland' when 106 then '`0001 Timberland' when 107 then '`0003 Other forestland' when 111 then '`0002 Reserved Forestland' when 112 then '`0002 Reserved Forestland' when 113 then '`0002 Reserved Forestland' when 114 then '`0002 Reserved Forestland' when 115 then '`0002 Reserved Forestland' when 116 then '`0002 Reserved Forestland' when 117 then '`0002 Reserved Forestland' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),199) then '`0011 Forest (bad reservcd or siteclcd)' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),299) then '`0004 Nonforest' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),399) then '`0005 Non-Census water' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),499) then '`0006 Census water' else case cond.cond_nonsample_reasn_cd when 1 then '`0007 Outside U.S. boundary' when 2 then '`0008 Denied access' when 3 then '`0009 Hazardous' else '`0010 Other' end end 
) A LEFT JOIN COUNTY B ON A.ROWSTR = B.COUNTYCD
LEFT JOIN REF_UNIT C ON B.UNITCD = C.VALUE; 
"""
cursor.execute(unitMap_Query)
unitMap = cursor.fetchall()
df_3 = pd.DataFrame(unitMap,columns=['Fips','CountyName','Region','LandUse' ,'EstimatedValue'])
df_3 = df_3[df_3.LandUse=='`0001 Timberland']
regions = df_3.Region.unique()
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

connection.close()

fig = px.pie(df, values='Acreage', names='Unit', title='% of forest cover')


app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(children="GEORGIA"),
                html.Label(
                    ["Georgia has a total forest cover of ",int(totalacre[0])," acres"],
                    style={"color": "rgb(33 36 35)"},
                ),
                html.Img(
                    src=app.get_asset_url("maple-tree-transparent-background.png"),
                    style={
                        "position": "relative",
                        "width": "100%",
                        "left": "-10px",
                        "top": "10px",
                    },
                ),
            ],
            className="side_bar",
        ),
        html.Div(
            [
                html.Div(
                    [                        
                        html.Div(
                            [
                                
                                dcc.Dropdown(
                                id="dropdown",
                                options=[{"label": x, "value": x} for x in ftype],
                                value=ftype[0],
                                clearable=False,
                            ),
                                dcc.Graph(id="bar-chart"),
                                html.Div(
                                    [html.P(id="comment")],
                                    className="box_comment",
                                ),
                    
                            ],
                            className="box",
                            style={
                                "margin": "10px",
                                "padding-top": "15px",
                                "padding-bottom": "15px",
                            }
                            ),
                            
                                    html.Div(
                                        [
                                            html.Div(
                                                dcc.Graph(
                                                             id='example-graph-2',
                                                             figure=fig
                                                             )
                                            ),
                                        ]
                                    ),
                                ],
                                style={"width": "40%","float":"left"}, 
                                className="main"
                    )
                ]
            ),
        html.Div([
            html.P("Regions:"),
            dcc.Dropdown(
                id='regions', 
                options=[{'value': x, 'label': x} 
                         for x in regions],
                value=regions[0],
                clearable=False
            ),
            dcc.Graph(id="choropleth"),
        ],  style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle','float':'left'},
            )
        ]
    )
        

@app.callback(
    Output("bar-chart" "figure"),
    [Input("dropdown", "value")],
    Output("choropleth", "figure"), 
    [Input("regions", "value")])
def update_bar_chart(ftype):
    mask = df_2['ForestType'] == ftype
    fig = px.bar(df_2[mask], x="SiteProductivity", y="Acreage",text_auto='.2s')
    return fig
def display_choropleth(region):
    fig2 = px.choropleth(df[df.Region==region], geojson=counties, locations='Fips', color='EstimatedValue',
                                color_continuous_scale="Viridis",                            
                                #range_color=(100000, 12),
                                scope="usa",
                                basemap_visible=False,
                                center={"lat":32.6836,"lon":-83.4644},
                                hover_data = ["CountyName"],
                                labels={'EstimatedValue':'Estimated Value'},
                                fitbounds='locations',
                              )
    fig2.update_geos(fitbounds="locations", visible=False)
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig2

if __name__ == "__main__":
    app.run_server(debug=True)