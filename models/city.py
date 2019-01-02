import math
import os
import pickle
from typing import List, Dict

import pandas as pd


class City:
    def __init__(self, city_id, x, y, prime_cities: List[bool]):
        self.x: float = float(x)
        self.y: float = float(y)
        self.id: int = int(city_id)

        self.is_prime = self._is_prime(prime_cities)
        self.neighbors = None
        self.neighbor_primes = None

    @staticmethod
    def sieve_of_eratosthenes(n: int) -> List[bool]:
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

    N_NEIGHBORS = 5
    N_NEIGHBOR_PRIMES = 5

    def get_neighbors(self, area_map: 'AreaMap') -> List['City']:
        if self.neighbors is not None:
            return self.neighbors

        self.neighbors = area_map.get_neighbors(self, self.N_NEIGHBORS, only_prime=False)
        return self.neighbors

    def get_neighbor_primes(self, area_map: 'AreaMap') -> List['City']:
        if self.neighbor_primes is not None:
            return self.neighbor_primes

        self.neighbor_primes = area_map.get_neighbors(self, self.N_NEIGHBOR_PRIMES, only_prime=True)
        return self.neighbor_primes

    @staticmethod
    def distance(a: 'City', b: 'City') -> float:
        """
        calculates the euclidean distance between 2 cities
        """
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    @staticmethod
    def load_from_csv(cities_path='data/cities.csv', prime_numbers_path='data/prime_numbers.pkl') -> List['City']:
        print('Loading cities from CSV.')
        df = pd.read_csv(cities_path)

        if os.path.exists(prime_numbers_path):
            with open(prime_numbers_path, 'rb') as f:
                prime_numbers = pickle.load(f)
        else:
            print('Finding prime numbers.')
            prime_numbers = City.sieve_of_eratosthenes(max(df.CityId))
            with open(prime_numbers_path, 'wb') as f:
                pickle.dump(prime_numbers, f)

        print('Generating City objects.')
        city_list = [City(l['CityId'], l['X'], l['Y'], prime_numbers) for _, l in df.iterrows()]
        return city_list

    def __repr__(self):
        """
        Prints all the properties of the object. idea is to be as verbose as possible.
        Implementing __repr__ or __str__ will make it easy to print and inspect in the notebook.
        """
        fmt_str = 'CityId: {} \nCoordinates: {}\nIs prime: {}\n'
        return fmt_str.format(self.id, self.get_coord(), self.is_prime)


class AreaMap:
    # These numbers are specific to cities.csv
    X_MIN = 1.87192466558405
    X_MAX = 5099.50214180651
    Y_MIN = 0.0
    Y_MAX = 3397.80982412656
    N_DIVISION = 50

    def __init__(self, cities: List[City], x_min=X_MIN, x_max=X_MAX, y_min=Y_MIN, y_max=Y_MAX, n_division=N_DIVISION):
        self.x_min: float = x_min
        self.x_max: float = x_max
        self.y_min: float = y_min
        self.y_max: float = y_max
        self.n_division: int = n_division
        self.area_map: Dict[int, List[City]] = self._make_area_map(cities)

    def _make_area_map(self, cities: List[City]) -> Dict[int, List[City]]:
        area_map = {}
        for i in range(int(math.pow(self.n_division + 1, 2))):
            area_map[i] = []

        for city in cities:
            area_id = self._get_area_id(city)
            area_map[area_id].append(city)

        return area_map

    def _get_area_id(self, city: City) -> int:
        x_width = (self.x_max - self.x_min) / self.n_division
        y_width = (self.y_max - self.y_min) / self.n_division

        x_i = int(math.floor(city.x / x_width))
        y_i = int(math.floor(city.y / y_width))

        if x_i > self.n_division or y_i > self.n_division:
            raise RuntimeError('Invalid area_id.')

        area_id = x_i * self.n_division + y_i
        return area_id

    def get_neighbors(self, city: City, limit, only_prime: bool = False) -> List[City]:
        center_area_id = self._get_area_id(city)
        neighbor_cities = self.area_map[center_area_id]
        if only_prime:
            neighbor_primes = []
            for c in neighbor_cities:
                if c.is_prime:
                    neighbor_primes.append(c)
            neighbor_cities = neighbor_primes

        if len(neighbor_cities) < limit:
            # raise RuntimeError('Not enough neighbors')
            pass

        neighbor_cities.sort(key=lambda x: City.distance(x, city))
        return neighbor_cities[:limit]
