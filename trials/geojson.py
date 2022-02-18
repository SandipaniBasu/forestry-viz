# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 12:20:52 2022

@author: basus
"""
import plotly.io as pio
from urllib.request import urlopen
import numpy as np
import pandas as pd
import plotly.express as px
import json
import sqlite3
from plotly.offline import plot
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# import geopandas as gpd


connection = sqlite3.connect('D:\\Study\\UGA\\SQLite_FIADB_GA\\FIADB_GA.db')
cursor=connection.cursor()
unitwise_Query = """select A.statecd || substr('00000' || A.rowstr,-3,3) as countycd,B.COUNTYNM , C.MEANING REGION,colstr,estimated_value from(
SELECT case 1 when 1 then '`0001 None`' end as pagestr, cond.statecd,cond.countycd as rowstr, case cond.cond_status_cd*100+coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0) when 101 then '`0001 Timberland' when 102 then '`0001 Timberland' when 103 then '`0001 Timberland' when 104 then '`0001 Timberland' when 105 then '`0001 Timberland' when 106 then '`0001 Timberland' when 107 then '`0003 Other forestland' when 111 then '`0002 Reserved Forestland' when 112 then '`0002 Reserved Forestland' when 113 then '`0002 Reserved Forestland' when 114 then '`0002 Reserved Forestland' when 115 then '`0002 Reserved Forestland' when 116 then '`0002 Reserved Forestland' when 117 then '`0002 Reserved Forestland' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),199) then '`0011 Forest (bad reservcd or siteclcd)' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),299) then '`0004 Nonforest' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),399) then '`0005 Non-Census water' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),499) then '`0006 Census water' else case cond.cond_nonsample_reasn_cd when 1 then '`0007 Outside U.S. boundary' when 2 then '`0008 Denied access' when 3 then '`0009 Hazardous' else '`0010 Other' end end as colstr, SUM((COALESCE(SCCM.SUBPTYP_PROP_CHNG / 4 * CASE COND.PROP_BASIS WHEN 'MACR' THEN POP_STRATUM.ADJ_FACTOR_MACR ELSE POP_STRATUM.ADJ_FACTOR_SUBP END, 0))*POP_STRATUM.EXPNS) AS ESTIMATED_VALUE FROM POP_STRATUM POP_STRATUM JOIN POP_PLOT_STRATUM_ASSGN POP_PLOT_STRATUM_ASSGN ON (POP_PLOT_STRATUM_ASSGN.STRATUM_CN = POP_STRATUM.CN) JOIN PLOT PLOT ON (POP_PLOT_STRATUM_ASSGN.PLT_CN = PLOT.CN) JOIN PLOTGEOM PLOTGEOM ON (PLOT.CN = PLOTGEOM.CN) JOIN COND COND ON (COND.PLT_CN = PLOT.CN) JOIN COND PCOND ON (PCOND.PLT_CN = PLOT.PREV_PLT_CN) JOIN SUBP_COND_CHNG_MTRX SCCM ON (SCCM.PLT_CN = COND.PLT_CN AND SCCM.PREV_PLT_CN = PCOND.PLT_CN AND SCCM.CONDID = COND.CONDID AND SCCM.PREVCOND = PCOND.CONDID) WHERE COND.CONDPROP_UNADJ IS NOT NULL AND ((SCCM.SUBPTYP = 3 AND COND.PROP_BASIS = 'MACR') OR (SCCM.SUBPTYP = 1 AND COND.PROP_BASIS = 'SUBP')) AND COALESCE(COND.COND_NONSAMPLE_REASN_CD, 0) = 0 AND COALESCE(PCOND.COND_NONSAMPLE_REASN_CD, 0) = 0 AND (COND.COND_STATUS_CD = 1 AND PCOND.COND_STATUS_CD = 1) AND ((pop_stratum.rscd=33 and pop_stratum.evalid=131903)) and 1=1 GROUP BY case 1 when 1 then '`0001 None`' end,cond.statecd,cond.countycd ,case cond.cond_status_cd*100+coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0) when 101 then '`0001 Timberland' when 102 then '`0001 Timberland' when 103 then '`0001 Timberland' when 104 then '`0001 Timberland' when 105 then '`0001 Timberland' when 106 then '`0001 Timberland' when 107 then '`0003 Other forestland' when 111 then '`0002 Reserved Forestland' when 112 then '`0002 Reserved Forestland' when 113 then '`0002 Reserved Forestland' when 114 then '`0002 Reserved Forestland' when 115 then '`0002 Reserved Forestland' when 116 then '`0002 Reserved Forestland' when 117 then '`0002 Reserved Forestland' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),199) then '`0011 Forest (bad reservcd or siteclcd)' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),299) then '`0004 Nonforest' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),399) then '`0005 Non-Census water' when min(cond.cond_status_cd*100 +coalesce(cond.reservcd,0)*10+coalesce(cond.siteclcd,0),499) then '`0006 Census water' else case cond.cond_nonsample_reasn_cd when 1 then '`0007 Outside U.S. boundary' when 2 then '`0008 Denied access' when 3 then '`0009 Hazardous' else '`0010 Other' end end 
) A LEFT JOIN COUNTY B ON A.ROWSTR = B.COUNTYCD
LEFT JOIN REF_UNIT C ON B.UNITCD = C.VALUE; 
"""
cursor.execute(unitwise_Query)
unitwise = cursor.fetchall()
df = pd.DataFrame(unitwise,columns=['Fips','CountyName','Region','LandUse' ,'EstimatedValue'])
df = df[df.LandUse=='`0001 Timberland']
regions = df.Region.unique()
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("Regions:"),
    dcc.Dropdown(
        id='regions', 
        options=[{'value': x, 'label': x} 
                 for x in regions],
        value=regions[0],
        clearable=False
    ),
    dcc.Graph(id="choropleth"),
],  style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle','float':'right'},
    )

@app.callback(
    Output("choropleth", "figure"), 
    [Input("regions", "value")])
def display_choropleth(region):
    fig = px.choropleth(df[df.Region==region], geojson=counties, locations='Fips', color='EstimatedValue',
                                color_continuous_scale="Viridis",                            
                                #range_color=(100000, 12),
                                scope="usa",
                                basemap_visible=False,
                                center={"lat":32.6836,"lon":-83.4644},
                                hover_data = ["CountyName"],
                                labels={'EstimatedValue':'Estimated Value'},
                                fitbounds='locations',
                              )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)

# fig = px.choropleth(df, geojson=counties, locations='Fips', color='EstimatedValue',
#                             color_continuous_scale="Viridis",                            
#                             #range_color=(100000, 12),
#                             scope="usa",
#                             basemap_visible=False,
#                             center={"lat":32.6836,"lon":-83.4644},
#                             hover_data = ["CountyName"],
#                             labels={'EstimatedValue':'Estimated Value'},
#                             fitbounds='locations',
#                           )
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()
# plot(fig)