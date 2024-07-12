import sys
import os
import unittest
from datetime import datetime

# Add the directory containing csv_project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csv_project.event import Event, Race, EventDivision
from csv_project.base import Projection

class TestEvent(unittest.TestCase):
    def setUp(self):
        self.event = Event(name="Test Event", date=datetime.now(), location="Test Location", onlookers=Projection(100, 50, 45))

    def test_initialization(self):
        self.assertEqual(self.event.name, "Test Event")
        self.assertIsInstance(self.event.date, datetime)
        self.assertEqual(self.event.location, "Test Location")
        self.assertIsInstance(self.event.onlookers, Projection)

    def test_get_csv_data(self):
        csv_data = self.event.get_csv_data()
        self.assertEqual(csv_data[0]['name'], "Test Event")
        self.assertEqual(csv_data[0]['location'], "Test Location")
        self.assertIsInstance(csv_data[0]['onlookers'], dict)

    def test_get_csv_fieldnames(self):
        fieldnames = self.event.get_csv_fieldnames()
        self.assertEqual(fieldnames, ['name', 'date', 'location', 'onlookers'])

class TestRace(unittest.TestCase):
    def setUp(self):
        self.event = Event(name="Test Event", date=datetime.now(), location="Test Location", onlookers=Projection(100, 50, 45))
        self.race = Race(event=self.event, sport="Running", name="Test Race", registrations=Projection(200, 150, 100), start_time=datetime.now())

    def test_initialization(self):
        self.assertEqual(self.race.event, self.event)
        self.assertEqual(self.race.sport, "Running")
        self.assertEqual(self.race.name, "Test Race")
        self.assertIsInstance(self.race.registrations, Projection)
        self.assertIsInstance(self.race.start_time, datetime)

    def test_get_csv_data(self):
        csv_data = self.race.get_csv_data()
        self.assertEqual(csv_data[0]['event'], str(self.event))
        self.assertEqual(csv_data[0]['sport'], "Running")
        self.assertEqual(csv_data[0]['name'], "Test Race")
        self.assertIsInstance(csv_data[0]['registrations'], dict)

    def test_get_csv_fieldnames(self):
        fieldnames = self.race.get_csv_fieldnames()
        self.assertEqual(fieldnames, ['event', 'sport', 'name', 'registrations', 'start_time'])

class TestEventDivision(unittest.TestCase):
    def setUp(self):
        self.event = Event(name="Test Event", date=datetime.now(), location="Test Location", onlookers=Projection(100, 50, 45))
        self.race = Race(event=self.event, sport="Running", name="Test Race", registrations=Projection(200, 150, 100), start_time=datetime.now())
        self.division = EventDivision(race=self.race, name="Test Division", qualification="Top 10")

    def test_initialization(self):
        self.assertEqual(self.division.race, self.race)
        self.assertEqual(self.division.name, "Test Division")
        self.assertEqual(self.division.qualification, "Top 10")

    def test_get_csv_data(self):
        csv_data = self.division.get_csv_data()
        self.assertEqual(csv_data[0]['race'], str(self.race))
        self.assertEqual(csv_data[0]['name'], "Test Division")
        self.assertEqual(csv_data[0]['qualification'], "Top 10")

    def test_get_csv_fieldnames(self):
        fieldnames = self.division.get_csv_fieldnames()
        self.assertEqual(fieldnames, ['race', 'name', 'qualification'])

if __name__ == "__main__":
    unittest.main()
