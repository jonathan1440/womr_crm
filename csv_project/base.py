from datetime import datetime
import ast
import sys
import os

# Add the directory containing csv_project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from . import csv_interface

# Abstracting common methods into a base class
class BaseClass:
    def save_to_csv(self, file_path):
        '''
        Saves the object to a csv file.
        '''
        data = self.get_csv_data()
        fieldnames = self.get_csv_fieldnames()
        csv_interface.write_csv(file_path, data, fieldnames)

    @classmethod
    def load_from_csv(cls, file_path):
        '''
        Loads all objects from a csv file.
        '''
        data = csv_interface.read_csv(file_path)
        objects = []
        for item in data:
            objects.append(cls(**item))
        return objects

    def __str__(self):
        '''
        Returns a string representation of the object.
        '''
        return f"{self.__class__.__name__}({', '.join(f'{key}={value}' for key, value in self.__dict__.items())})"

class Projection(BaseClass):
    def __init__(self, max: int, projected: int, actual: int):
        '''
        Initializes a Projection object.

        Args:
            max (int): The maximum value.
            projected (int): The projected value.
            actual (int): The actual value.
        '''
        self.max = max
        self.projected = projected
        self.actual = actual

    def get_csv_data(self):
        return [{
            'max': self.max,
            'projected': self.projected,
            'actual': self.actual
        }]

    def get_csv_fieldnames(self):
        return ['max', 'projected', 'actual']
