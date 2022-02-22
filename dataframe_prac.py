# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 13:15:22 2022

@author: basus
"""


"""
Created on Thu Feb  3 16:20:28 2022

@author: basus
"""

# 1. Import Dash
import pandas as pd


df = pd.read_csv('unitWise_GA.csv')
#df = df[df.LandUse=='`0001 Timberland']
regions = df.Region.unique()
df['CountyEstimatedValue'] = df.groupby(['State','Fips','CountyName','Region'])['EstimatedValue'].transform('sum')
df['RegionEstimatedValue'] = df.groupby(['Region'])['EstimatedValue'].transform('sum')

df2 = pd.read_csv('yearWise_GA.csv')
county = df2.CountyName.unique()
df2[['Dummy','Year']] = df2['Year'].str.split(expand=True)
df2.sort_values(by='Year',inplace=True)
df2['CumEstimatedValue'] = df2[['CountyName','Year','EstimatedValue']].groupby('CountyName').cumsum()
overallState = df2.groupby(['State','Year']).sum('EstimatedValue').reset_index()
overallState['CumEstimatedValue'] = overallState['EstimatedValue'].cumsum()
overallRegions = df2[['State','Region','Year','EstimatedValue']].groupby(['State','Region','Year']).sum('EstimatedValue').reset_index()
overallRegions['CumEstimatedValue'] = overallRegions[['Region','Year','EstimatedValue']].groupby(['Region']).cumsum()
df2 = df2.astype({'Year':'int'})