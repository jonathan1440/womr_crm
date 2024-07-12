from datetime import datetime
import ast
import sys
import os

# Add the directory containing csv_project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csv_project.base import BaseClass, Projection

events = []
class Event(BaseClass):
    def __init__(self, name: str, date: datetime, location: str, onlookers):
        '''
        Initializes an Event object.

        Args:
            name (str): The name of the event.
            date (datetime): The date and time of the event.
            location (str): The location of the event.
            onlookers (Union[str, Projection]): The onlookers data, either as a string to be parsed or a Projection object.
        '''
        self.name = name
        self.date = date
        self.location = location

        if isinstance(onlookers, str):
            onlookers_dict = ast.literal_eval(onlookers)
            self.onlookers = Projection(**onlookers_dict)
        else:
            self.onlookers = onlookers
        
        events.append(self)

    def get_csv_data(self):
        return [{
            'name': self.name,
            'date': self.date.strftime("%Y-%m-%d %H:%M:%S"),
            'location': self.location,
            'onlookers': self.onlookers.get_csv_data()[0]
        }]

    def get_csv_fieldnames(self):
        return ['name', 'date', 'location', 'onlookers']

races = []
class Race(BaseClass):
    def __init__(self, event: Event, sport: str, name: str, registrations: Projection, start_time: datetime):
        '''
        Initializes a Race object.

        Args:
            event (Event): The event associated with the race.
            sport (str): The sport of the race.
            name (str): The name of the race.
            registrations (Projection): The registrations data for the race.
            start_time (datetime): The start time of the race.
        '''
        self.event = event
        self.sport = sport
        self.name = name
        self.registrations = registrations
        self.start_time = start_time

        races.append(self)

    def get_csv_data(self):
        return [{
            'event': str(self.event),
            'sport': self.sport,
            'name': self.name,
            'registrations': self.registrations.get_csv_data()[0],
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S")
        }]

    def get_csv_fieldnames(self):
        return ['event', 'sport', 'name', 'registrations', 'start_time']

divisions = []
class EventDivision(BaseClass):
    def __init__(self, race: Race, name: str, qualification: str):
        '''
        Initializes an EventDivision object.

        Args:
            race (Race): The race associated with the division.
            name (str): The name of the division.
            qualification (str): The qualification criteria for the division.
        '''
        self.race = race
        self.name = name
        self.qualification = qualification

        divisions.append(self)

    def get_csv_data(self):
        return [{
            'race': str(self.race),
            'name': self.name,
            'qualification': self.qualification
        }]

    def get_csv_fieldnames(self):
        return ['race', 'name', 'qualification']
