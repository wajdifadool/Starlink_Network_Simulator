import cartopy.crs as ccrs
import cartopy.feature as cfeature
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from matplotlib.widgets import RectangleSelector
from skyfield.iokit import parse_tle_file
from skyfield.api import load

from  models.ground_control import GroundControl
from models.ground_station import   GroundStation
from models.satellite import Satellite
import  models.utils as utils


class SatelliteTracker(QMainWindow):
    def __init__(self, ground_control:GroundControl , users):
        super().__init__()
        print("SatelliteTracker Invoked")
        self.satellite_annotations = []  # Store annotations for satellites
        self.users= users
        self.update_interval:int = (utils.UPDATE_LENGTH_IN_SEC*(10**3))
        self.gc =  ground_control
        self.setWindowTitle("Real-Time Satellite Tracker")

        self.showMaximized()

        # Set up the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create Matplotlib Figure
        self.fig = Figure()

        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        # Adjust figure layout to remove margins
        self.fig.tight_layout(pad=0)  # Automatically fit elements with no extra padding
        self.fig.subplots_adjust(left=0, right=1, top=0.95, bottom=0)  # Fill the entire canvas


        # Initialize plot
        self.ax = self.fig.add_subplot(111, projection=ccrs.PlateCarree())
        self.ax.stock_img()
        self.ax.add_feature(cfeature.BORDERS, linestyle=":")
        self.ax.add_feature(cfeature.COASTLINE)
        self.ax.set_title("Real-Time Starlink Satellite Tracker" , pad=10)


        # Initial plotting
        self.satellite_scatter = None
        # self.plot_satellites()
        # self.plot_stations()
        self.plot_users()

        # Set up timer for updates
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_satellite_positions)
        # self.timer.start(self.update_interval)  # Update every X seconds

    def plot_satellites(self):
        """Plot satellites on the map."""
        # print("calling  updat e satlites ")

        # Remove old annotations if any
        for annotation in self.satellite_annotations:
            annotation.remove()
        self.satellite_annotations.clear()

        lats =[]
        longs=[]
        lats = [sat.latitude for sat  in self.gc.my_satellites]
        longs = [sat.longitude for sat in self.gc.my_satellites]

        # Plot satellites as red points
        self.satellite_scatter = self.ax.scatter(
            longs,
            lats,
            color='red',
            s=10,

            transform=ccrs.PlateCarree(),
        )

        self.plot_stations_names()
        self.canvas.draw()

    # plot stasions names , used for debuging
    def plot_stations_names(self):
        # Annotate each satellite with its name
        for sat in self.gc.my_satellites:
            # print(sat)
            annotation = self.ax.annotate(

                sat.satellite_id,
                xy=(sat.longitude, sat.latitude),
                xytext=(3, 3),  # Offset the text slightly
                textcoords='offset points',
                fontsize=6,
                color='black',
                transform=ccrs.PlateCarree(),
            )
            self.satellite_annotations.append(annotation)



    def plot_stations(self):
        my_gc = self.gc.my_ground_stations

        lats = [gs.latitude for gs in my_gc]
        longs = [gs.longitude for gs in my_gc]

        # Plot stations as blue squares
        self.ax.scatter(
            longs,
            lats,
            color="blue",
            s=20,
            transform=ccrs.PlateCarree(),
            marker="^",
        )
        self.ax.legend()

    def update_satellite_positions(self):
        print("calling update UI ")
        if self.satellite_scatter:
            self.satellite_scatter.remove()

        self.gc.refresh_my_satellites() # todo , calulate it in the background beforecalling
        self.plot_satellites()

    def plot_users(self):

        my_users = self.users

        lats = [user.latitude for user in my_users]
        longs = [user.longitude for user in my_users]

        self.ax.scatter(
            longs,
            lats,
            color="green",
            s=3,
            transform=ccrs.PlateCarree(),
            marker="s",
        )
        self.ax.legend()
