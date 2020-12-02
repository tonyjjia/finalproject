#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 21:36:51 2020

@author: yihaoli
"""

import pandas as pd
import pandas_dedupe


import numpy as np
import os

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import matplotlib.pyplot as plt

import requests

############################################################################################################

# Data Loading and Cleaning

############################################################################################################


# Load the geographic information data of public high schools in Chicago 
# District 299:

# Data source: https://data.cityofchicago.org/Education/Chicago-Public-Schools-School-Profile-Information-/8i6r-et8s

def prepare_data (path):
    chicago_school = pd.read_csv(os.path.join(path, 
                                          "Chicago_Public_Schools_-_School_Profile_Information_SY1617.csv"))
    df = chicago_school.loc[chicago_school['Is_High_School'] == "Y"] 
    df = df[['School_ID',
             "Short_Name", 
             'Long_Name', 
             'School_Type', 
             'Address', 
             'City', 
             'State', 
             'Zip']]
    return df

chicago_high_school = prepare_data(r'/Users/YIHAOLI/Desktop/Github/finalproject')


# Load the data of ethnicity of Chicago public high schools
        
def ethnicity_geography(excel):
    
    race = pd.read_excel (excel)
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
    
    df = pd.merge(race,
                 chicago_high_school,
                 on=['School_ID','Long_Name'], how='inner')
    
    df['Long_Name'] = df['Long_Name'].str.replace('HS','High School')
    
    return df

race_geo = ethnicity_geography(r'/Users/YIHAOLI/Desktop/Github/finalproject/school_ethnicity.xlsx')


# Load the US News 2020 data about how well each school prepared its students for college
path = r'/Users/YIHAOLI/Desktop/Github/finalproject'
college_readiness = pd.read_csv(os.path.join(path, "data_college_readiness.csv"))


# Cleaning up school names

def fuzzy_merge(df_1, df_2, key1, key2, threshold=88, limit=10):
    
    s = df_2[key2].tolist()

    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))    
    df_1['matches'] = m

    m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df_1['matches'] = m2
    
    df_1['matches'] = df_1['matches'].replace(['Chicago Military Academy High School, Chicago Academy High School'],
                                    'Chicago Military Academy High School')

    df_1['matches'] = df_1['matches'].replace(['Chicago Academy High School, Chicago Military Academy High School, Chicago Technology Academy High School'],
                                    'Chicago Academy High School')
    
    df_1 = df_1.drop(76)
    df_1 = df_1.drop(124)
    df_1 = df_1.drop(44)
    
    df_1['matches'] = df_1['matches'].replace(['Chicago Technology Academy High School, Chicago Academy High School'],
                                    'Chicago Technology Academy High School')

    df_1 = df_1.rename(columns={'matches': 'School Name'})
    
    final_df = pd.merge(df_1,
                        college_readiness, 
                        on = 'School Name',
                        how = 'inner')

    return final_df

race_geo_college_readiness = fuzzy_merge(race_geo,
                                         college_readiness, 
                                         "Long_Name", 
                                         'School Name')

################################################################################################################

#Data Visualization

################################################################################################################


# Plot the Relation between Share of Black Students and College Readiness
plt.scatter(race_geo_college_readiness['Pct_black'],
            race_geo_college_readiness['College Readiness Index'], 
            color = 'black')
plt.title('Scatter Plot')
plt.xlabel("School Share of Black Students")
plt.ylabel('College Readiness Index')
plt.show()


# Plot the Relation between Share of Hispanic Students and College Readiness
plt.scatter(race_geo_college_readiness['Pct_hispanic'],
            race_geo_college_readiness['College Readiness Index'], 
            color = 'black')
plt.title('Scatter Plot')
plt.xlabel("School Share of Hispanic Students")
plt.ylabel('College Readiness Index')
plt.show()


















