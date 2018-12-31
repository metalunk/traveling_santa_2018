import math
from typing import List

import pandas as pd


class City:
    def __init__(self, city_id, x, y):
        self.x = x
        self.y = y
        self.id = city_id
        self.is_prime = self._check_prime()
        self.neighbors = self._get_neighbors()
        self.neighbor_primes = self._get_neighbor_primes()

    def _check_prime(self):
        """
        Checks if a city is prime
        """
        if self.id < 2:
            return False
        for i in range(2, int(math.sqrt(self.id)) + 1, 2):
            if self.id % i == 0:
                return False
        return True

    def get_coord(self):
        return self.x, self.y

    def _get_neighbors(self):
        return {}

    def _get_neighbor_primes(self):
        return {}

    @staticmethod
    def distance(a: 'City', b: 'City') -> float:
        """
        calculates the euclidean distance between 2 cities
        """
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    @staticmethod
    def load_from_csv(cities_path='data/cities.csv') -> List['City']:
        df = pd.read_csv(cities_path)
        city_list = [City(l['CityId'], l['X'], l['Y']) for _, l in df.iterrows()]
        return city_list

    def __repr__(self):
        """
        Prints all the properties of the object. idea is to be as verbose as possible.
        Implementing __repr__ or __str__ will make it easy to print and inspect in the notebook.
        """
        fmt_str = 'CityId: {} \nCoordinates: {}\nIs prime: {}\n'
        return fmt_str.format(self.id, self.get_coord(), self.is_prime)
