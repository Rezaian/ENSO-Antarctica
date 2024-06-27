#read ERA5 dataset mslp variable
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs  # Import cartopy coordinate reference systems
import cartopy.feature as cfeature  # To add features such as borders
import numpy as np
import pandas as pd

# read classified months
classified_months = pd.read_csv('classified_extreme_months.csv')

# Load the new dataset
file_path = 'adaptor.mars.internal-1708005678.4330814-8261-4-81f6c0fa-376b-4c88-afda-d134d14e61db.nc'  # Update this to the new file path
dataset = xr.open_dataset(file_path)

# select elnino phases based on the classified months
# select mean sea level pressure as msl from the dataset
variable_el = dataset['msl'].isel(time=classified_months['Mark']=='extreme_elnino', expver=0)
variable_la = dataset['msl'].isel(time=classified_months['Mark']=='extreme_lanina', expver=0)
variable_ne = dataset['msl'].isel(time=classified_months['Mark']=='neutral', expver=0)

# time average (axis 0 is time)
variable_el_average = np.mean(variable_el, axis=0)
variable_la_average = np.mean(variable_la, axis=0)
variable_ne_average = np.mean(variable_ne, axis=0)

#calculate the anomaly
variable_el_average_anomaly = variable_el_average - variable_ne_average
variable_la_average_anomaly = variable_la_average - variable_ne_average


# print  
# Set up the figure and axes for two side-by-side plots
fig, axes = plt.subplots(1, 2, figsize=(18, 8), subplot_kw={'projection': ccrs.SouthPolarStereo()})

# Plot the ELNINO anomaly on the first axis
ax1 = axes[0]
cbar1 = variable_el_average_anomaly.plot(ax=ax1, transform=ccrs.PlateCarree(), x='longitude', y='latitude', add_colorbar=True, cmap='BrBG')
cbar1.colorbar.set_label('MSLP [mb]')
ax1.add_feature(cfeature.COASTLINE)
ax1.gridlines(draw_labels=True, linestyle='--', color='gray')
ax1.set_title('El Niño MSLP Anomaly')

# Plot the LANINA anomaly on the second axis
ax2 = axes[1]
cbar2 = variable_la_average_anomaly.plot(ax=ax2, transform=ccrs.PlateCarree(), x='longitude', y='latitude', add_colorbar=True, cmap='BrBG')
cbar2.colorbar.set_label('MSLP [mb]')
ax2.add_feature(cfeature.COASTLINE)
ax2.gridlines(draw_labels=True, linestyle='--', color='gray')
ax2.set_title('La Niña MSLP Anomaly')

# Display the plots
plt.show()
