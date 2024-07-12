import sys
import os

# Add the directory containing csv_project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csv_project.base import BaseClass

locations = []
class Location(BaseClass):
    def __init__(self, name: str, street_address: str, street_address_2: str, city: str, state: str, zip_code: str, notes: str):
        '''
        Initializes a Location object.

        Args:
            name (str): The name of the location.
            street_address (str): The street address of the location.
            street_address_2 (str): The secondary street address of the location.
            city (str): The city of the location.
            state (str): The state of the location.
            zip_code (str): The zip code of the location.
            notes (str): Additional notes about the location.
        '''
        self.name = name
        self.street_address = street_address
        self.street_address_2 = street_address_2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.notes = notes

        locations.append(self)

    def get_csv_data(self):
        return [{
            'name': self.name,
            'street_address': self.street_address,
            'street_address_2': self.street_address_2,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'notes': self.notes
        }]

    def get_csv_fieldnames(self):
        return ['name', 'street_address', 'street_address_2', 'city', 'state', 'zip_code', 'notes']

courses = []
class Course(BaseClass):
    def __init__(self, gpx_file: str, distance: float, elevation: float, start: Location, finish: Location = None):
        '''
        Initializes a Course object.

        Args:
            gpx_file (str): The GPX file of the course.
            distance (float): The distance of the course.
            elevation (float): The elevation of the course.
            start (Location): The starting location of the course.
            finish (Location): The finishing location of the course. Defaults to start.
        '''
        self.gpx_file = gpx_file
        self.distance = distance
        self.elevation = elevation
        self.start = start
        self.finish = finish if finish is not None else start

        courses.append(self)

    def get_csv_data(self):
        return [{
            'gpx_file': self.gpx_file,
            'distance': self.distance,
            'elevation': self.elevation,
            'start': self.start.name,
            'finish': self.finish.name
        }]

    def get_csv_fieldnames(self):
        return ['gpx_file', 'distance', 'elevation', 'start', 'finish']
