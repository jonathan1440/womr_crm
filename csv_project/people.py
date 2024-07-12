from datetime import datetime
from enum import Enum
import sys
import os

# Add the directory containing csv_project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csv_project.geography import Location
from csv_project.base import BaseClass

class Gender(Enum):
    M = "M"
    F = "F"

persons = []
class Person(BaseClass):
    def __init__(self, first: str, last: str, birthdate: datetime, gender: Gender, email: str, phone: int, notes: str, home: Location):
        '''
        Initializes a People object.

        Args:
            first (str): The first name.
            last (str): The last name.
            birthdate (datetime): The birthdate.
            gender (Gender): The gender.
            email (str): The email address.
            phone (int): The phone number.
            notes (str): Additional notes.
            home (Location): The home location.
        '''
        self.first = first
        self.last = last
        self.birthdate = birthdate
        self.gender = gender
        self.email = email
        self.phone = phone
        self.notes = notes
        self.home = home

        persons.append(self)

    def get_csv_data(self):
        return [{
            'first': self.first,
            'last': self.last,
            'birthdate': self.birthdate.strftime('%Y-%m-%d'),
            'gender': self.gender.value,
            'email': self.email,
            'phone': self.phone,
            'notes': self.notes,
            'home': self.home.get_csv_data()
        }]

    def get_csv_fieldnames(self):
        return ['first', 'last', 'birthdate', 'gender', 'email', 'phone', 'notes', 'home']
    
jobs = []
class Job(BaseClass):
    def __init__(self, event: Event, description: str, person: Person, source: str, location: Location, duration: float, rate: float):
        '''
        Initializes a Job object.

        Args:
            event (Event): The event associated with the job.
            description (str): The description of the job.
            person (Person): The person assigned to the job.
            source (str): The source of the job.
            location (Location): The location of the job.
            duration (float): The duration of the job.
            rate (float): The rate of the job.
        '''
        self.event = event
        self.description = description
        self.person = person
        self.source = source
        self.location = location
        self.duration = duration
        self.rate = rate

        jobs.append(self)

    def get_csv_data(self):
        return [{
            'event': str(self.event),
            'description': self.description,
            'person': str(self.person),
            'source': self.source,
            'location': str(self.location),
            'duration': self.duration,
            'rate': self.rate
        }]

    def get_csv_fieldnames(self):
        return ['event', 'description', 'person', 'source', 'location', 'duration', 'rate']

