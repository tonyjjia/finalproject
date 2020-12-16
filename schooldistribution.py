"""
@author: tonyjia
"""
pip install geopandas #JL: this is not code

os.chdir('/Users/tonyjia/Documents/GitHub/finalproject/finalproject')

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd


file_name1=r'/Users/tonyjia/Documents/GitHub/finalproject/finalproject/Boundaries - ZIP Codes/geo_export_a467ef04-a7d9-4917-aaff-ef95b0c3061d.shp'
file_name2=r'/Users/tonyjia/Documents/GitHub/finalproject/finalproject/Chicago_Public_Schools_-_School_Profile_Information_SY1617.csv'
school_loc=pd.read_csv(file_name2)

school_loc_short=school_loc[['Long_Name','School_Latitude','School_Longitude','School_Type','Is_High_School']]
school_loc_short=school_loc_short[school_loc_short['Is_High_School']=='Y']

import folium
import json
import requests
import os
import webbrowser

def graph_school(data1):  
    city_map=folium.Map(location=[41.8781,-87.6298],zoom_start=12) #JL: be clear on what these dimensions are if you're going to hard-code them in

    data_la=data1['School_Latitude']
    data_long=data1['School_Longitude']

    for la,long in zip(data_la,data_long):
        schools.add_child(folium.CircleMarker([la,long], radius=3,color='red',fill=True,fill_color='yellow',fill_opacity=0.5)) #JL: variable "schools" is not defined
    city_map.add_child(schools)

    neighbor_bound=gpd.read_file('/Users/tonyjia/Documents/GitHub/finalproject/finalproject/Boundaries - ZIP Codes/geo_export_a467ef04-a7d9-4917-aaff-ef95b0c3061d.shp')
    folium.GeoJson(neighbor_bound,style_function=lambda feature:{
            'fillColor':'#00FFFFFF','color':'black','weight':3}).add_to(city_map)
    return city_map

draw_map=graph_school(school_loc_short)
path=r'/Users/tonyjia/Documents/GitHub/finalproject/finalproject'
filename='school_map.html'
filename=os.path.join(path,filename)
draw_map.save(filename)
#This code helps open the html file automatically in your browser
webbrowser.open('file:///Users/tonyjia/Documents/GitHub/finalproject/finalproject/school_map.html')

#Draw a Heatmap to depict schools distribution
from folium.plugins import HeatMap

def graph_heat(data2):
    heat_map=folium.Map(location=[41.8781,-87.6298],zoom_start=11)
    heatdata=data2[['School_Latitude','School_Longitude']].values.tolist()
    HeatMap(heatdata).add_to(heat_map)
    return heat_map

draw_heat_map=graph_heat(school_loc_short)
path=r'/Users/tonyjia/Documents/GitHub/finalproject/finalproject'
filename_heat='heat_map.html'
filename_heat=os.path.join(path,filename_heat)
draw_heat_map.save(filename_heat)
webbrowser.open('file:///Users/tonyjia/Documents/GitHub/finalproject/finalproject/heat_map.html')


#Draw a distribution graph in accordance with the dominant ethnic group
school_loc_short2=school_loc_short
school_loc_short2['Demographic']=school_loc['Demographic_Description']
split_res=[]
def find_demo(demo):
    for i in range(len(demo['Demographic'])): #JL: you should not iterate manually over a dataframe column; use map
        demo_split=str(demo['Demographic'].iloc[i]).split()
        list_race=['White.','Black.','Hispanic.']
        matching=[s for s in demo_split if any(t in s for t in list_race)]
        split_res.append(matching)
        i+=1 #JL: this does nothing
    return split_res
split_res=find_demo(school_loc_short2)
split_clean=[]
def clean_punc(demo2):
    for k in demo2:
        k=str(k).replace('.', '')
        k=str(k).replace('[', '')
        k=str(k).replace(']', '')
        k=str(k).replace("'", '')
        split_clean.append(k)
split_res=clean_punc(split_res)
    
school_loc_short2['Demo']=split_clean
data_white=school_loc_short2[school_loc_short2['Demo']=='White']
data_black=school_loc_short2[school_loc_short2['Demo']=='Black']
data_hispanic=school_loc_short2[school_loc_short2['Demo']=='Hispanic']

num_map=folium.Map(location=[41.8781,-87.6298],zoom_start=11)
data_type=list(school_loc_short2['Demo'])
demo_graph=folium.map.FeatureGroup()

for la,long in zip(data_white['School_Latitude'],data_white['School_Longitude']):
    demo_graph.add_child(folium.CircleMarker([la,long],color='red',radius=3,fill=True,fill_color='yellow',fill_opacity=0.7))
    num_map.add_child(demo_graph)
for la,long in zip(data_black['School_Latitude'],data_black['School_Longitude']):
    demo_graph.add_child(folium.CircleMarker([la,long],color='black',radius=3,fill=True,fill_color='yellow',fill_opacity=0.7))
    num_map.add_child(demo_graph)
for la,long in zip(data_hispanic['School_Latitude'],data_hispanic['School_Longitude']):
    demo_graph.add_child(folium.CircleMarker([la,long],color='blue',radius=3,fill=True,fill_color='yellow',fill_opacity=0.7))
    num_map.add_child(demo_graph)
 
folium.GeoJson(neighbor_bound,style_function=lambda feature:{
        'fillColor':'#00FFFFFF','color':'black','weight':3,'dashArray':'7,7'}).add_to(demo_graph)
           
path=r'/Users/tonyjia/Documents/GitHub/finalproject/finalproject'
filename_demo='num_map.html'
filename_demo=os.path.join(path,filename_demo)
num_map.save(filename_demo)
webbrowser.open('file:///Users/tonyjia/Documents/GitHub/finalproject/finalproject/num_map.html')









