import folium
import pandas as pd
from geopy.distance import vincenty

Chi_COORDINATES = (41.88, -87.63)
crimedata_2001_pres = pd.read_csv('2016_35th_90th_crimedata.csv', nrows=74947)
divvy_data = pd.read_csv('Divvy_Bicycle_Stations.csv', nrows=118)

# for speed purposes
#MAX_RECORDS = 1000
#p2013_RECORDS = 926258

#number of crimes near Divvy bicycle stations
s = 0
c = 0

# create empty map zoomed in on Chicago
map = folium.Map(location=Chi_COORDINATES, zoom_start=12)

#when zoom out, cluster and sum the number
my_marker_cluster = folium.MarkerCluster()

# add a marker for every record in the filtered data, use a clustered view
for each_d in divvy_data.iterrows():
    folium.CircleMarker(location = [each_d[1]['Latitude'],each_d[1]['Longitude']], radius=200, popup=each_d[1]['Station Name'], color='#3186cc', fill_color='#3186cc').add_to(map)
    s = s + 1

for each_c in crimedata_2001_pres.iterrows():
    location_c = (each_c[1]['Latitude'],each_c[1]['Longitude'])
    for each_d in divvy_data.iterrows():
        location_d = (each_d[1]['Latitude'],each_d[1]['Longitude'])  
        distance = vincenty(location_d, location_c).meters
        #crimes are near the Divvy bicycle stations
        if(distance <= 200):
            folium.Marker(location = [each_c[1]['Latitude'],each_c[1]['Longitude']]).add_to(my_marker_cluster)
            c = c + 1
map.add_children(my_marker_cluster)

map.save('divvy_crime_map.html')

print 'number of stations:\n', s
print 'number of crimes:\n', c



