from datetime import datetime
import ast
import sys
import os

# Add the directory containing csv_project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csv_project import csv_interface
from csv_project.base import BaseClass, Projection
from csv_project.event import Event

resources = []
class Resource(BaseClass):
    def __init__(self, name: str, cost_per_unit: float, acquire_from: str, notes: str, historical_costs=None):
        """
        Initializes a Resource object.

        Args:
            name (str): The name of the resource.
            cost_per_unit (float): The cost per unit of the resource.
            acquire_from (str): The source from where the resource is acquired.
            notes (str): Additional notes about the resource.
            historical_costs (dict, optional): A dictionary of historical costs with dates as keys. Defaults to None.
        """
        self.name = name
        self._cost_per_unit = cost_per_unit
        self.acquire_from = acquire_from
        self.notes = notes

        if historical_costs is None:
            self.historical_costs = {}
            self.add_to_historical_record(cost_per_unit)
        else:
            self.historical_costs = historical_costs

        resources.append(self)

    @property
    def cost_per_unit(self):
        if not self.historical_costs:
            return self._cost_per_unit
        latest_date = max(self.historical_costs)
        return self.historical_costs[latest_date]

    @cost_per_unit.setter
    def cost_per_unit(self, value):
        now = datetime.now()
        self.historical_costs[now] = value

    def add_to_historical_record(self, cost: float, date: str = None):
        """
        Adds a cost - date pair to the historical record of costs.
        `cost` should be a float representing the value to be recorded.
        `date` should be a string representing the date of the record.
        If `date` is None, it will be set to the current date and time.
        """
        if date is None:
            date_obj = datetime.now()
        else:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
        self.historical_costs[date_obj] = cost

    def get_cost_by_date(self, date: str):
        """
        Returns the cost added before or equal to the given date from self.historical_costs.
        `date` should be a string representing the date to query.
        """
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        relevant_dates = [d for d in self.historical_costs if d <= date_obj]
        if not relevant_dates:
            return None
        latest_date = max(relevant_dates)
        return self.historical_costs[latest_date]

    def get_csv_data(self):
        return [{
            "name": self.name,
            "cost_per_unit": self.cost_per_unit,
            "acquire_from": self.acquire_from,
            "notes": self.notes,
            "historical_costs": {date.strftime("%Y-%m-%d %H:%M:%S"): cost for date, cost in self.historical_costs.items()}
        }]

    def get_csv_fieldnames(self):
        return ["name", "cost_per_unit", "acquire_from", "notes", "historical_costs"]

resource_categories = []
class ResourceCategory(BaseClass):
    def __init__(self, name: str, invoice_order: int):
        """
        Initializes a ResourceCategory object.

        Args:
            name (str): The name of the resource category.
            invoice_order (int): The order of the resource category in the invoice.
        """
        self.name = name
        self.invoice_order = invoice_order
        resource_categories.append(self)

    def get_csv_data(self):
        return [{
            "name": self.name,
            "invoice_order": self.invoice_order
        }]

    def get_csv_fieldnames(self):
        return ["name", "invoice_order"]

event_resources = []
class EventResource(BaseClass):
    def __init__(self, event: Event, resource: Resource, invoice_line_item: str, invoice_order: int):
        """
        Initializes an EventResources object.

        Args:
            event (Event): The event associated with the resource.
            resource (Resource): The resource associated with the event.
            invoice_line_item (str): The line item description for the invoice.
            invoice_order (int): The order of the line item in the invoice.
        """
        self.event = event
        self.resource = resource
        self.invoice_line_item = invoice_line_item
        self.invoice_order = invoice_order

        event_resources.append(self)

    def get_csv_data(self):
        return [{
            "event": str(self.event),
            "resource": str(self.resource),
            "invoice_line_item": self.invoice_line_item,
            "invoice_order": self.invoice_order
        }]

    def get_csv_fieldnames(self):
        return ["event", "resource", "invoice_line_item", "invoice_order"]

resource_allocations = []
class ResourceAllocation(BaseClass):
    def __init__(self, event_resource: EventResource, count_quantity: bool, location: str, date_to_acquire: datetime, quantity: Projection, donated_by: str = None):
        """
        Initializes a ResourceAllocation object.

        Args:
            event_resource (EventResources): The event resource associated with the allocation.
            count_quantity (bool): Whether to count the quantity of the resource in the total quantity of it's associated invoice line item.
            location (str): The location where the resource is allocated.
            date_to_acquire (datetime): The date when the resource is to be acquired.
            quantity (Projection): The quantity of the resource.
            donated_by (str, optional): The donor of the resource. Defaults to None.
        """
        self.event_resource = event_resource
        self.count_quantity = count_quantity
        self.location = location
        self.date_to_acquire = date_to_acquire
        self.quantity = quantity
        self.donated_by = donated_by

        resource_allocations.append(self)

    def get_csv_data(self):
        return [{
            "event_resource": str(self.event_resource),
            "count_quantity": self.count_quantity,
            "location": self.location,
            "date_to_acquire": self.date_to_acquire.strftime("%Y-%m-%d %H:%M:%S"),
            "quantity": self.quantity.get_csv_data()[0],
            "donated_by": self.donated_by
        }]

    def get_csv_fieldnames(self):
        return ["event_resource", "count_quantity", "location", "date_to_acquire", "quantity", "donated_by"]
