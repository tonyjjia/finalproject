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

school_loc_short=school_loc[['Long_Name','School_Latitude','School_Longitude']]

import folium
city_map=folium.Map(location=[41.8781,-87.6298],zoom_start=12)

data_long=school_loc_short['School_Latitude']
data_la=school_loc_short['School_Longitude']
schools=folium.map.FeatureGroup()
for long,la in zip(data_long,data_la):
    schools.add_child(folium.CircleMarker([long,la], radius=3,color='red',fill=True,fill_color='yellow',fill_opacity=0.5))
city_map.add_child(schools)

import json
import requests

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
heatdata = school_loc_short[['School_Latitude','School_Longitude']].values.tolist()
HeatMap(heatdata).add_to(heat_map)

path=r'/Users/tonyjia/Documents/GitHub/finalproject/finalproject'
filename_heat='heat_map.html'
filename_heat=os.path.join(path,filename_heat)
heat_map.save(filename_heat)
















