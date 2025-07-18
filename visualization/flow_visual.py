import os
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from models.graph_utils import GraphUtils
from  models.satellite import  Satellite
from  models.ground_control import  GroundControl
import  pickle
import numpy as np

class FlowVisual():
    def __init__(self , ground_control:GroundControl):
        # Load the data for max flow

        f1 = "max_flow_full_day_s2s_20_global_5000"
        f2="max_flow_full_day_s2s_20_USA_5000"
        f3="max_flow_full_day_s2s_20_usa_ca_aus_eu_5000"

        f4 = "max_flow_full_day_s2s_200_global_5000"
        f5 = "max_flow_full_day_s2s_200_USA_5000"
        f6 = "max_flow_full_day_s2s_200_usa_ca_aus_eu_5000"

        self.gc = ground_control
        with open("max_flow_full_day_s2s_20_global_5000", 'rb') as file:
            m_flows =  pickle.load(file)

        for k in range(9):
            self.max_flow_nodes = m_flows[k]["flow_sats"]

            time = m_flows[k]["time"]
            mmax_flow  = m_flows[k]["flow_value_GB"]
            capacity = m_flows[k]["capacity"]
            s2s, s2g , s2u =capacity["s2s"] ,capacity["s2g"],capacity["s2u"]

            print(f"max_FLOW_GB{mmax_flow}")

            # self.plot_flow_on_map_with_analysis()
        #
            self.plot_satellite_flow_distribution(self.max_flow_nodes ,mmax_flow   ,time,s2s ,  1000)

    def plot_flow_on_map_with_analysis(self):
        """
        Plot satellites and flow values on a static map using real positions.
        Analyze the flow distribution and print statistics.
        """

        flows = self.max_flow_nodes
        # # Analyze flow data
        min_flow = flows[-1].total_flow

        max_flow = flows[0].total_flow
        mid_flow = (min_flow + max_flow) / 2



        # Determine flow value range for normalization
        norm = Normalize(vmin=min_flow, vmax=max_flow)
        cmap = cm.get_cmap('RdYlGn_r')  # Reverse the colormap to make red maximum and green minimum

        # Set up the map with maximized figure size
        # fig = plt.figure(figsize=(20, 12))  # Larger figure size for full screen
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_global()  # Ensure the map is global
        ax.stock_img()
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        ax.add_feature(cfeature.COASTLINE)

        # Plot satellites on the map
        for sat in flows :
            lat, lon = sat.latitude , sat.longitude
            color = cmap(norm(sat.total_flow))  # Map flow value to color
            ax.scatter(
                lon,
                lat,
                color=color,
                s=5,  # Smaller size for the points
                transform=ccrs.PlateCarree(),
                marker="o",
            )

        # Add a compact colorbar inside the map
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])  # Required for matplotlib colorbar
        cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', pad=0.05, aspect=50, shrink=0.5)  # Compact colorbar
        cbar.set_label('Flow Value', fontsize=10)  # Smaller font size for the label
        cbar.ax.tick_params(labelsize=8)  # Smaller font size for tick labels

        plt.tight_layout(rect=[0, 0, 1, 0.95])  # Maximize the map usage


        # plot ground stations
        my_gc = self.gc.my_ground_stations

        lats = [gs.latitude for gs in my_gc]
        longs = [gs.longitude for gs in my_gc]

        # Plot stations as blue squares
        ax.scatter(
            longs,
            lats,
            color="blue",
            s=2,
            transform=ccrs.PlateCarree(),
            marker="s",
        )

        plt.show()

    def plot_satellite_flow_distribution(self, node_flow_list , max_flow , simulation_time , s2s , total_sats):
        """
        Plots a heatmap of satellite flow distribution using Cartopy.
        """

        # ✅ Format Date to "YYYY-MM-DD HH:MM"
        simulation_time = simulation_time.utc_iso().split('T')[0] + " " + simulation_time.utc_iso().split('T')[1][:5]

        # ✅ 1. Filter out invalid lat/lon values
        valid_nodes = []
        for sat in node_flow_list:
            if sat.latitude is None or sat.longitude is None:
                continue  # Skip missing values

            lat, lon = sat.latitude, sat.longitude

            # ✅ Avoid projection errors by limiting extreme values
            if not (-89.9 <= lat <= 89.9 and -179.9 <= lon <= 179.9):
                print(f"⚠️ Skipping invalid coordinates: {lat}, {lon}")
                continue
            valid_nodes.append(sat)

        if not valid_nodes:
            print("⚠️ No valid satellites to plot!")
            return

        # ✅ 2. Extract lat/lon and flow values
        lats = np.array([sat.latitude for sat in valid_nodes])
        lons = np.array([sat.longitude for sat in valid_nodes])
        flows = np.array([sat.total_flow for sat in valid_nodes])

        # ✅ 3. Setup Cartopy map
        fig, ax = plt.subplots(figsize=(12, 6), subplot_kw={'projection': ccrs.PlateCarree()})
        ax.set_global()

        # ✅ 4. Add map features
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, linewidth=0.5)
        ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')

        # ✅ 5. Scatter plot with flow intensity
        scatter = ax.scatter(lons, lats, c=flows, cmap='Reds', alpha=0.75, edgecolors='k', s=30,
                             transform=ccrs.PlateCarree())

        # ✅ 6. Add colorbar
        plt.colorbar(scatter, label="Total Flow per Satellite")
        plt.title("Satellite Load Distribution (Flow Intensity)")


        # ✅ 7. Add max flow and date inside the figure
        # ax.text(-170, -75, f"Max Flow: {max_flow}", fontsize=12, bbox=dict(facecolor='white', alpha=0.7),
        #         transform=ccrs.PlateCarree())
        # ax.text(-170, -85, f"Date: {simulation_time}", fontsize=12, bbox=dict(facecolor='white', alpha=0.7),
        #         transform=ccrs.PlateCarree())

        fig.text(0.15, 0.92, f"Max Flow: {max_flow}", fontsize=12, bbox=dict(facecolor='white', alpha=0.7))
        fig.text(0.15, 0.88, f"Date: {simulation_time} , Satellite capacity: {s2s}GB, Total Satellites: {total_sats}" , fontsize=12, bbox=dict(facecolor='white', alpha=0.7))


        # ✅ 8. Show the plot
        plt.show()






