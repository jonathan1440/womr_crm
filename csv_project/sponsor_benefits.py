import sys
import os

# Add the directory containing csv_project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csv_project.resource import Resource
from csv_project.base import BaseClass, Projection
from csv_project.event import Event

sponsor_tiers = []
class SponsorTier(BaseClass):
    def __init__(self, name: str, quantity_per_event: int, value: float):
        '''
        Initializes a SponsorTier object.

        Args:
            name (str): The name of the sponsor tier.
            quantity_per_event (int): The quantity of benefits per event.
            value (float): The value of the sponsor tier.
        '''
        self.name = name
        self.quantity_per_event = quantity_per_event
        self.value = value

        sponsor_tiers.append(self)

benefits = []
class Benefit(BaseClass):
    def __init__(self, resource: Resource, description: str, value_per_impression: float):
        '''
        Initializes a Benefit object.

        Args:
            resource (Resource): The resource associated with the benefit.
            description (str): The description of the benefit.
            value_per_impression (float): The value per impression of the benefit.
        '''
        self.resource = resource
        self.description = description
        self.value_per_impression = value_per_impression

        benefits.append(self)

tier_benefits = []
class TierBenefit(BaseClass):
    def __init__(self, sponsor_tier: SponsorTier, benefit: Benefit, quantity: int):
        '''
        Initializes a TierBenefit object.

        Args:
            sponsor_tier (SponsorTier): The sponsor tier associated with the benefit.
            benefit (Benefit): The benefit associated with the sponsor tier.
            quantity (int): The quantity of the benefit.
        '''
        self.sponsor_tier = sponsor_tier
        self.benefit = benefit
        self.quantity = quantity

        tier_benefits.append(self)

event_benefits = []
class EventBenefit(BaseClass):
    def __init__(self, event: Event, benefit: Benefit, interactions_per_unit: Projection):
        '''
        Initializes an EventBenefit object.

        Args:
            event (Event): The event associated with the benefit.
            benefit (Benefit): The benefit associated with the event.
            interactions_per_unit (Projection): The projection of interactions per unit of the benefit.
        '''
        self.event = event
        self.benefit = benefit
        self.interactions_per_unit = interactions_per_unit

        event_benefits.append(self)

    def get_csv_data(self):
        return [{
            'event': str(self.event),
            'benefit': str(self.benefit),
            'interactions_per_unit': self.interactions_per_unit.get_csv_data()[0]
        }]

    def get_csv_fieldnames(self):
        return ['event', 'benefit', 'interactions_per_unit']


