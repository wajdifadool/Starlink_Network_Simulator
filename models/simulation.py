from models.graph_utils import  GraphUtils
from  models.ground_control import  GroundControl
from skyfield.api import load
from datetime import timedelta
from  models.file_manager import  FileManager
from  models.satellite import  Satellite
import  re
import numpy as np
import  pickle
from random import  shuffle
import models.utils as utils
from  models.user import  User
from models.file_manager import  FileManager
from models.graph_utils import  CAPACITY
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature

class Simulation:

    def __init__(self, gc:GroundControl , users):
        self.gc = gc
        # self.users_list = users
        self.users = users
        self.users_length = len(self.users)
        self.res = []
        self.fm = FileManager()

        self.sats_list  = self.fm.load_tle_file_into_list()
        self.simulate_timestamps()


    def simulate_timestamps(self):
        # Initialize timescale

        ts = load.timescale()

        now = ts.now()  # Current time in Skyfield format

        time_intervals = [now + (5 * i) / (24 * 60) for i in range(18)]  # Convert minutes to days
        for i, t in enumerate(time_intervals):
            print(f"Step {i}: {t.utc_iso()}")

        print(len(time_intervals))
        # print(f"len of time tamps = {len(time_stamps)}")

        # create the max flow
        sats = []
        flows = []

        for m_time in time_intervals:
            # Create sats

            # sats_i = []

            # sat_i = self._create_my_satellites(m_time)
            sat_i = self._create_my_satellites(m_time)

            # build max flow graph
            graph_utils = None
            graph_utils = GraphUtils(ground_control= self.gc, ground_users=self.users, sats=sat_i )

            flow_sats = graph_utils.get_max_flow_satellites()
            flow_value = graph_utils.get_max_flow_value()

            self.plot_satellite_flow_distribution(flow_sats , flow_value,m_time , 200 , len(sat_i))



        current_flow_holder = {
            "time":now,
            "flow_sats": flow_sats,
            "flow_value_GB": flow_value ,
            "user_group_count" : self.users_length,
            "capacity" : {
                "s2s" : CAPACITY.S2S.value ,
                "s2g": CAPACITY.S2G.value,
                "s2u": CAPACITY.S2U.value,
            }
        }



            # self.res.append(current_flow_holder)

        globall = "global"
        usa = "USA"
        usa_ca_aus_eu = "usa_ca_aus_eu"


        file_name = f"max_flow_full_day_s2s_{CAPACITY.S2S.value}_{usa}_{self.users_length}"
        with open(file_name, 'wb') as file:
            pickle.dump(self.res, file)

    def _create_my_satellites(self , m_time ):
        temp = []
        for sat in self.sats_list:
            geometry = sat.at(m_time)
            subpoint = geometry.subpoint()
            sat_elevation = subpoint.elevation.km

            if 700 > sat_elevation > 450:

                sat_lat = subpoint.latitude.degrees
                sat_lng = subpoint.longitude.degrees
                sat_xyz = geometry.position.km

                sat_name = re.search(r"-(\d+)$", sat.name).group(1) # "Starlink-1008" will be now "1008", faster
                satellite = Satellite(sat_name, latitude=sat_lat, longitude=sat_lng,
                                      altitude=sat_elevation, sat_xyz=sat_xyz,
                                      total_flow=None)
                temp.append(satellite)

        shuffle(temp)
        print(f"Simulation::_create_my_satellites(), my_satellites count={len(temp)}")
        return temp

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

        # my_gc = self.gc.my_ground_stations
        # # ✅ 1. Extract lat/lon for ground stations
        # lats2 = [gs.latitude for gs in my_gc]
        # longs2 = [gs.longitude for gs in my_gc]
        #
        # # ✅ 2. Plot ground stations as BLUE markers
        # ax.scatter(longs2, lats2, c='blue', marker='^', edgecolors='k', s=80,
        #            label="Ground Stations", transform=ccrs.PlateCarree())
        #
        # # ✅ 3. Add a legend for clarity
        # ax.legend(loc="upper right")


        # ✅ 6. Add colorbar
        plt.colorbar(scatter, label="Total Flow per Satellite")
        plt.title("Satellite Load Distribution (Flow Intensity)")


        # ✅ 7. Add max flow and date inside the figure
        # ax.text(-170, -75, f"Max Flow: {max_flow}", fontsize=12, bbox=dict(facecolor='white', alpha=0.7),
        #         transform=ccrs.PlateCarree())
        # ax.text(-170, -85, f"Date: {simulation_time}", fontsize=12, bbox=dict(facecolor='white', alpha=0.7),
        #         transform=ccrs.PlateCarree())

        fig.text(0.15, 0.92, f"Max Flow: {max_flow} GB", fontsize=12, bbox=dict(facecolor='white', alpha=0.7))
        fig.text(0.15, 0.88, f"Date: {simulation_time} , Satellite capacity: 200 GB, Total Satellites: {total_sats}" , fontsize=12, bbox=dict(facecolor='white', alpha=0.7))


        # ✅ 8. Show the plot
        plt.show()
