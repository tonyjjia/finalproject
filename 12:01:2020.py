#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 21:36:51 2020

@author: yihaoli
"""

import pandas as pd


import numpy as np
import os

import matplotlib.pyplot as plt

import requests

from bs4 import BeautifulSoup





path = r'/Users/YIHAOLI/Desktop/Github/finalproject'

# Load the geographic information data of public high schools in Chicago District 299
chicago_school = pd.read_csv(os.path.join(path, 
                                          "Chicago_Public_Schools_-_School_Profile_Information_SY1617.csv"))

chicago_high_school = chicago_school.loc[chicago_school['Is_High_School'] == "Y"] 

chicago_high_school = chicago_high_school[['School_ID',
                                             "Short_Name",
                                             'Long_Name',
                                             'School_Type', 
                                             'Address', 
                                             'City', 
                                             'State', 
                                             'Zip']]
# Data source: https://data.cityofchicago.org/Education/Chicago-Public-Schools-School-Profile-Information-/8i6r-et8s

# Load the data of ethnicity of Chicago public high schools
                      
race = pd.read_excel (r'/Users/YIHAOLI/Desktop/Github/finalproject/school_ethnicity.xlsx')

race.columns = race.iloc[0]
race.columns.name=None
race.drop(0, axis=0, inplace=True)
race = race.drop(race.index[0])
race = race.reset_index(drop=True)
race.drop(race.columns[[0]], axis=1, inplace=True)

race.columns = ['School_ID', 'Long_Name', 'Total_Student', 'No_white', 
                'Pct_white', "No_black", 'Pct_black', 'No_pacific', 
                "Pct_pacific", 'No_native', 'Pct_native', 'No_hispanic', 
                'Pct_hispanic', 'No_multi', 'Pct_multi', 'No_asian',
                'Pct_asian', 'No_hawaiian', 'Pct_hawaiian', 'No_unknown', 
                'Pct_unknown']

race['School_ID'] = race['School_ID'].astype(np.int64)

race_geo = pd.merge(race,
                 chicago_high_school,
                 on=['School_ID','Long_Name'], how='inner')




# Load the US News 2020 data about how well each school prepared its students for college
college_readiness = pd.read_csv(os.path.join(path, "data_college_readiness.csv"))
college_readiness = college_readiness.rename(columns={'School Name': 'Long_Name'})

race_geo_college_readiness = pd.merge(race_geo, 
                                      college_readiness, 
                                      on = 'Long_Name', 
                                      how = 'inner')



# Plot the Relation between Share of Black Students and College Readiness



plt.scatter(race_geo_college_readiness['College Readiness Index'],race_geo_college_readiness['Pct_black'], color = 'black')
plt.title('Scatter plot pythonspot.com')
plt.xlabel('x')
plt.ylabel('y')
plt.show()


















