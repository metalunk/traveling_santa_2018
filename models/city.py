import math
from typing import List

import pandas as pd


class City:
    def __init__(self, city_id, x, y, prime_cities: List[bool]):
        self.x: float = float(x)
        self.y: float = float(y)
        self.id: int = int(city_id)

        self.is_prime = self._is_prime(prime_cities)
        self.neighbors = self._get_neighbors()
        self.neighbor_primes = self._get_neighbor_primes()

    @staticmethod
    def sieve_of_eratosthenes(n: int):
        primes = [True for i in range(n + 1)]  # Start assuming all numbers are primes
        primes[0] = False  # 0 is not a prime
        primes[1] = False  # 1 is not a prime
        for i in range(2, int(math.sqrt(n)) + 1):
            if primes[i]:
                k = 2
                while i * k <= n:
                    primes[i * k] = False
                    k += 1
        return primes

    def _is_prime(self, prime_cities: List):
        return prime_cities[self.id]

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

        prime_cities = City.sieve_of_eratosthenes(max(df.CityId))
        city_list = [City(l['CityId'], l['X'], l['Y'], prime_cities) for _, l in df.iterrows()]
        return city_list

    def __repr__(self):
        """
        Prints all the properties of the object. idea is to be as verbose as possible.
        Implementing __repr__ or __str__ will make it easy to print and inspect in the notebook.
        """
        fmt_str = 'CityId: {} \nCoordinates: {}\nIs prime: {}\n'
        return fmt_str.format(self.id, self.get_coord(), self.is_prime)
