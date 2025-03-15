#%%
import pandas as pd
import geopandas as gpd
import os
import matplotlib.pyplot as plt

#set file locations for import
shp_loc = os.getcwd() + '/raw_data/' + 'Official_NPUs_with_Current_Demographic_Data/' + 'Official_NPUs_with_Current_Demographic_Data.shp'
marta_loc = os.getcwd() + '/raw_data/' + 'MARTA_Rail_Stations/' + 'MARTA_Rail_Stations.shp'

#read in shapefiles
npu = gpd.read_file(shp_loc)
marta = gpd.read_file(marta_loc)
#%%

#fix the coordinate system between the two shapefiles to match
npu = npu.to_crs(marta.crs)

#initiate empty figure
fig, ax = plt.subplots(1, 1)

#create transit chloropleth
npu.plot(column = 'commute__4', legend = True, ax = ax)
marta.plot(ax = ax, color='red', markersize=10)
#plt.title('Combined Chloropleth Map with Points')
plt.show()

#next: recreate plot using approx # commuters instead of by %

#%%
