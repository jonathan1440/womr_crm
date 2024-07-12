import sys
import os
import unittest
from datetime import datetime

# Add the directory containing csv_project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csv_project.sponsor_benefits import SponsorTier, Benefit, TierBenefit, EventBenefit
from csv_project.resource import Resource
from csv_project.event import Event
from csv_project.base import Projection

class TestSponsorTier(unittest.TestCase):
    def setUp(self):
        self.sponsor_tier = SponsorTier(name="Gold", quantity_per_event=10, value=1000.0)

    def test_initialization(self):
        self.assertEqual(self.sponsor_tier.name, "Gold")
        self.assertEqual(self.sponsor_tier.quantity_per_event, 10)
        self.assertEqual(self.sponsor_tier.value, 1000.0)

class TestBenefit(unittest.TestCase):
    def setUp(self):
        self.resource = Resource(name="Banner", cost_per_unit=50.0, acquire_from="Vendor", notes="Test Notes")
        self.benefit = Benefit(resource=self.resource, description="Banner Display", value_per_impression=5.0)

    def test_initialization(self):
        self.assertEqual(self.benefit.resource, self.resource)
        self.assertEqual(self.benefit.description, "Banner Display")
        self.assertEqual(self.benefit.value_per_impression, 5.0)

class TestTierBenefit(unittest.TestCase):
    def setUp(self):
        self.sponsor_tier = SponsorTier(name="Gold", quantity_per_event=10, value=1000.0)
        self.resource = Resource(name="Banner", cost_per_unit=50.0, acquire_from="Vendor", notes="Test Notes")
        self.benefit = Benefit(resource=self.resource, description="Banner Display", value_per_impression=5.0)
        self.tier_benefit = TierBenefit(sponsor_tier=self.sponsor_tier, benefit=self.benefit, quantity=5)

    def test_initialization(self):
        self.assertEqual(self.tier_benefit.sponsor_tier, self.sponsor_tier)
        self.assertEqual(self.tier_benefit.benefit, self.benefit)
        self.assertEqual(self.tier_benefit.quantity, 5)

class TestEventBenefit(unittest.TestCase):
    def setUp(self):
        self.event = Event(name="Test Event", date=datetime.now(), location="Test Location", onlookers=Projection(100, 50, 45))
        self.resource = Resource(name="Banner", cost_per_unit=50.0, acquire_from="Vendor", notes="Test Notes")
        self.benefit = Benefit(resource=self.resource, description="Banner Display", value_per_impression=5.0)
        self.projection = Projection(100, 50, 45)
        self.event_benefit = EventBenefit(event=self.event, benefit=self.benefit, interactions_per_unit=self.projection)

    def test_initialization(self):
        self.assertEqual(self.event_benefit.event, self.event)
        self.assertEqual(self.event_benefit.benefit, self.benefit)
        self.assertEqual(self.event_benefit.interactions_per_unit, self.projection)

    def test_get_csv_data(self):
        csv_data = self.event_benefit.get_csv_data()
        self.assertEqual(csv_data[0]['event'], str(self.event))
        self.assertEqual(csv_data[0]['benefit'], str(self.benefit))
        self.assertEqual(csv_data[0]['interactions_per_unit'], self.projection.get_csv_data()[0])

    def test_get_csv_fieldnames(self):
        fieldnames = self.event_benefit.get_csv_fieldnames()
        self.assertEqual(fieldnames, ['event', 'benefit', 'interactions_per_unit'])

if __name__ == '__main__':
    unittest.main()
