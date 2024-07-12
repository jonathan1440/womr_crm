import sys
import os
import unittest
from datetime import datetime

# Add the directory containing csv_project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csv_project.resource import Resource, ResourceCategory, EventResource, ResourceAllocation, ObjHistory
from csv_project.event import Event
from csv_project.base import Projection


class TestResource(unittest.TestCase):
    def setUp(self):
        self.resource = Resource(name="Test Resource", cost_per_unit=ObjHistory(initial_obj=10.0), acquire_from="Test Source", notes="Test Notes")

    def test_initialization(self):
        self.assertEqual(self.resource.name, "Test Resource")
        self.assertEqual(self.resource.cost_per_unit.initial_obj, 10.0)
        self.assertEqual(self.resource.acquire_from, "Test Source")
        self.assertEqual(self.resource.notes, "Test Notes")
        self.assertIsInstance(self.resource.cost_per_unit.historical_costs, dict)

    def test_cost_per_unit_property(self):
        self.resource.add_to_historical_record(15.0, "2022-01-01")
        self.assertEqual(self.resource.cost_per_unit.initial_obj, 10.0)

    def test_add_to_historical_record(self):
        self.resource.add_to_historical_record(20.0, "2022-02-01")
        date_obj = datetime.strptime("2022-02-01", "%Y-%m-%d")
        self.assertEqual(self.resource.cost_per_unit.historical_costs[date_obj], 20.0)

    def test_get_cost_by_date(self):
        self.resource.add_to_historical_record(20.0, "2022-02-01")
        self.resource.add_to_historical_record(25.0, "2022-03-01")
        cost = self.resource.get_cost_by_date("2022-03-01")
        self.assertEqual(cost, 25.0)
        cost = self.resource.get_cost_by_date("2022-03-02")
        self.assertEqual(cost, 25.0)
        cost = self.resource.get_cost_by_date("2022-02-02")
        self.assertEqual(cost, 20.0)

class TestResourceCategory(unittest.TestCase):
    def setUp(self):
        self.resource_category = ResourceCategory(name="Test Category", invoice_order=1)

    def test_initialization(self):
        self.assertEqual(self.resource_category.name, "Test Category")
        self.assertEqual(self.resource_category.invoice_order, 1)

class TestEventResource(unittest.TestCase):
    def setUp(self):
        self.event = Event(name="Test Event", date=datetime.now(), location="Test Location", onlookers=Projection(100, 50, 45))
        self.resource = Resource(name="Test Resource", cost_per_unit=ObjHistory(initial_obj=10.0), acquire_from="Test Source", notes="Test Notes")
        self.event_resource = EventResource(event=self.event, resource=self.resource, invoice_line_item="Test Line Item", invoice_order=1)

    def test_initialization(self):
        self.assertEqual(self.event_resource.event, self.event)
        self.assertEqual(self.event_resource.resource, self.resource)
        self.assertEqual(self.event_resource.invoice_line_item, "Test Line Item")
        self.assertEqual(self.event_resource.invoice_order, 1)

class TestResourceAllocation(unittest.TestCase):
    def setUp(self):
        self.event = Event(name="Test Event", date=datetime.now(), location="Test Location", onlookers=Projection(100, 50, 45))
        self.resource = Resource(name="Test Resource", cost_per_unit=ObjHistory(initial_obj=10.0), acquire_from="Test Source", notes="Test Notes")
        self.event_resource = EventResource(event=self.event, resource=self.resource, invoice_line_item="Test Line Item", invoice_order=1)
        self.projection = Projection(100, 50, 45)
        self.resource_allocation = ResourceAllocation(event_resource=self.event_resource, count_quantity=True, location="Test Location", date_to_acquire=datetime.now(), quantity=self.projection, donated_by="Test Donor")

    def test_initialization(self):
        self.assertEqual(self.resource_allocation.event_resource, self.event_resource)
        self.assertTrue(self.resource_allocation.count_quantity)
        self.assertEqual(self.resource_allocation.location, "Test Location")
        self.assertIsInstance(self.resource_allocation.date_to_acquire, datetime)
        self.assertEqual(self.resource_allocation.quantity, self.projection)
        self.assertEqual(self.resource_allocation.donated_by, "Test Donor")

if __name__ == "__main__":
    unittest.main()
