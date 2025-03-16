#%%
import pandas as pd
import geopandas as gpd
import os
import matplotlib.pyplot as plt

#set file locations for import
shp_loc = os.getcwd() + '/raw_data/' + 'Official_NPUs_with_Current_Demographic_Data/' + 'Official_NPUs_with_Current_Demographic_Data.shp'
marta_loc = os.getcwd() + '/raw_data/' + 'MARTA_Rail_Stations/' + 'MARTA_Rail_Stations.shp'
bus_loc = os.getcwd() + '/raw_data/' + 'MARTA_Stops/' + 'MARTA_Stops.shp'

#read in shapefiles
npu = gpd.read_file(shp_loc)
marta = gpd.read_file(marta_loc)
bus = gpd.read_file(bus_loc)
#%%

#fix the coordinate system between the two shapefiles to match
npu = npu.to_crs(marta.crs)
bus = bus.to_crs(marta.crs)


#initiate empty figure
fig, ax = plt.subplots(1, 1)

#create transit chloropleth
npu.plot(column = 'commute__4', legend = True, ax = ax)
marta.plot(ax = ax, color='red', markersize=10)
#its hard to visualize the bus stops because they are dense
#bus.plot(ax = ax, color = 'grey', markersize=.1)
ax.set_axis_off()
plt.title('Marta Stations and % Transit Commuters')
plt.show()

#%%
#calculate the approx number of commuters per NPU
#ignoring differences in age dist by npu
npu['transit_commuters'] = npu['commute__4'] * npu['populati_1']
#%%

#recreate figure by pop size instead of proportion commuters
#initiate empty figure
fig, ax = plt.subplots(1, 1)
#create transit chloropleth
npu.plot(column = 'transit_commuters', legend = True, ax = ax)
marta.plot(ax = ax, color='red', markersize=10)
#its hard to visualize the bus stops because they are dense
#bus.plot(ax = ax, color = 'grey', markersize=.1)
ax.set_axis_off()
plt.title('Marta Stations and # Transit Commuters')
plt.show()
# %%

#now the train routes correspond more with the # riders
#west side still looks like an outlier - large number of people are taking transit without easy access

#count number of bus stops in each npu
combined = gpd.sjoin(bus, npu, predicate='within')

# Count points per polygon
points_per_polygon = combined.groupby(combined.index_right).size().reset_index()
points_per_polygon.columns = ['index_right', 'point_count']

# merge count of bus stations with npu df
npu_with_counts = npu.reset_index().rename(columns={'index': 'index_right'})
npu_with_counts = npu_with_counts.merge(points_per_polygon, on='index_right', how='left')

npu_with_counts['point_count'] = npu_with_counts['point_count'].fillna(0).astype(int)

# plot chloropleth of bus stops per npu
fig, ax = plt.subplots(1, 1)
npu_with_counts.plot(column='point_count', legend=True, ax=ax)
ax.set_axis_off()
plt.title('Bus stops per NPU')
plt.show()
# %%
