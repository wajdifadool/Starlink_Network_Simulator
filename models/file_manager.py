import os
import json
from skyfield.api import load
from skyfield.iokit import parse_tle_file
import  logging
import models.utils as  utils
class FileManager:
    def __init__(self, directory: str = 'data'):
        self.directory = directory

    def load_tle_file_into_list(self):
        """Load the 3le.tle file that contains the satellites data  """
        file_name: str = utils.FILE_NAME
        script_dir = os.path.dirname(self.directory)
        file_path = os.path.join(script_dir, self.directory, file_name)

        ts = load.timescale()

        with load.open(file_path) as f:
            satellites = list(parse_tle_file(f, ts))
        logging.debug(f'loaded {file_name} that contains {len(satellites)} sats object')
        return satellites

    def load_ground_stations(self, file_name: str=utils.COORDINATE_FILE):
        """ Load station data from JSON file"""
        script_dir = os.path.dirname(self.directory)
        file_path = os.path.join(script_dir, self.directory, file_name)

        with open(file_path, "r") as file:
            station_data = json.load(file)

        logging.debug(f'loaded {file_name} that contains {len(station_data)} ground station object')
        return station_data

