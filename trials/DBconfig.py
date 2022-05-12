# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sqlite3
import pandas as pd

masterdf = pd.read_csv('D:\\Study\\UGA\\Spring 2022\\Dr.Dwivedi\\FIA_DataMart\\forestry-viz\\trials\\DBQueries.csv')
allstatesdf = pd.DataFrame(columns=['Year','State','Fips','CountyName','Region','EstimatedValue'])
for index,row in masterdf.iterrows():
    print('Extracting data for State',row['State'])
    connection = sqlite3.connect(row['Path'])
    cursor=connection.cursor()
    df = pd.DataFrame(columns=['Year','State','Fips','CountyName','Region','EstimatedValue'])
    for year in range(10,22):    
        unitwise_Query = row['Query'].format(str(year),str(year))        
        cursor.execute(unitwise_Query)
        unitwise = cursor.fetchall()
        temp = pd.DataFrame(unitwise,columns=['Year','State','Fips','CountyName','Region','EstimatedValue'])    
        df = df.append(temp)
    df['EstimatedValue'] = df.EstimatedValue.round(2)
    allstatesdf = allstatesdf.append(df)

allstatesdf['Fips'] = allstatesdf['Fips'].astype(str)
allstatesdf.to_csv('allstates.csv')

connection.close()



