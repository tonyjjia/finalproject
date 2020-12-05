"""
@author: tonyjia
"""
pip install geopandas

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

file_name1=r'/Users/tonyjia/Documents/GitHub/finalproject/finalproject/Boundaries - ZIP Codes/geo_export_a467ef04-a7d9-4917-aaff-ef95b0c3061d.shp'
file_name2=r'/Users/tonyjia/Documents/GitHub/finalproject/finalproject/Chicago_Public_Schools_-_School_Profile_Information_SY1617.csv'
school_loc=pd.read_csv(file_name2)

school_loc_short=school_loc[['Long_Name','School_Latitude','School_Longitude','School_Type','Is_High_School']]
school_loc_short=school_loc_short[school_loc_short['Is_High_School']=='Y']
import folium
city_map=folium.Map(location=[41.8781,-87.6298],zoom_start=12)

data_la=school_loc_short['School_Latitude']
data_long=school_loc_short['School_Longitude']
schools=folium.map.FeatureGroup()
for la,long in zip(data_la,data_long):
    schools.add_child(folium.CircleMarker([la,long], radius=3,color='red',fill=True,fill_color='yellow',fill_opacity=0.5))
city_map.add_child(schools)

import json
import requests
import os

neighbor_bound=gpd.read_file('/Users/tonyjia/Documents/GitHub/finalproject/finalproject/Boundaries - ZIP Codes/geo_export_a467ef04-a7d9-4917-aaff-ef95b0c3061d.shp')
folium.GeoJson(neighbor_bound,style_function=lambda feature:{
        'fillColor':'#00FFFFFF','color':'black','weight':3}).add_to(city_map)

path=r'/Users/tonyjia/Documents/GitHub/finalproject/finalproject'
filename='school_map.html'
filename=os.path.join(path,filename)
city_map.save(filename)


#Draw a Heatmap to depict schools distribution
from folium.plugins import HeatMap
heat_map=folium.Map(location=[41.8781,-87.6298],zoom_start=12)
heatdata=school_loc_short[['School_Latitude','School_Longitude']].values.tolist()
HeatMap(heatdata).add_to(heat_map)

path=r'/Users/tonyjia/Documents/GitHub/finalproject/finalproject'
filename_heat='heat_map.html'
filename_heat=os.path.join(path,filename_heat)
heat_map.save(filename_heat)

#We refine our analysis, providing a new map on identifying the race of the majority
school_loc_short2=school_loc_short
school_loc_short2['Demographic']=school_loc['Demographic_Description']
split_res=[]
for i in range(len(school_loc_short2['Demographic'])): 
    demo_split=str(school_loc_short2['Demographic'].iloc[i]).split()
    list_race=['White.','Black.','Hispanic.']
    matching=[s for s in demo_split if any(t in s for t in list_race)]
    split_res.append(matching)
    i+=1  
split_clean=[]
for k in split_res:
    k=str(k).replace('.', '')
    k=str(k).replace('[', '')
    k=str(k).replace(']', '')
    k=str(k).replace("'", '')
    split_clean.append(k)
school_loc_short2['Demo']=split_clean
data_white=school_loc_short2[school_loc_short2['Demo']=='White']
data_black=school_loc_short2[school_loc_short2['Demo']=='Black']
data_hispanic=school_loc_short2[school_loc_short2['Demo']=='Hispanic']

num_map=folium.Map(location=[41.8781,-87.6298],zoom_start=12)
data_type=list(school_loc_short2['Demo'])
demo_graph=folium.map.FeatureGroup()

for la,long in zip(data_white['School_Latitude'],data_white['School_Longitude']):
    demo_graph.add_child(folium.CircleMarker([la,long],color='green',radius=3,fill=True,fill_color='yellow',fill_opacity=0.7))
    num_map.add_child(demo_graph)
for la,long in zip(data_black['School_Latitude'],data_black['School_Longitude']):
    demo_graph.add_child(folium.CircleMarker([la,long],color='black',radius=3,fill=True,fill_color='yellow',fill_opacity=0.7))
    num_map.add_child(demo_graph)
for la,long in zip(data_hispanic['School_Latitude'],data_hispanic['School_Longitude']):
    demo_graph.add_child(folium.CircleMarker([la,long],color='blue',radius=3,fill=True,fill_color='yellow',fill_opacity=0.7))
    num_map.add_child(demo_graph)
            
path=r'/Users/tonyjia/Documents/GitHub/finalproject/finalproject'
filename_demo='num_map.html'
filename_demo=os.path.join(path,filename_demo)
num_map.save(filename_demo)








