import math
from typing import List

import pandas as pd
from sklearn.neighbors import KDTree

from helper import load_from_pickle


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

        print('Loading prime numbers.')
        prime_numbers = load_from_pickle(prime_numbers_path, lambda: City.sieve_of_eratosthenes(max(df.CityId)))

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


class Neighbors:
    N_NEIGHBOR = 10

    def __init__(self, cities: List[City], n_neighbor=N_NEIGHBOR):
        """
        :param cities: This should be sorted by city_id
        """
        XY = []
        for city in cities:
            XY.append((city.x, city.y))
        self.kdt = KDTree(XY)

        k = n_neighbor + 1
        self.idx_list = self.kdt.query(XY, k=k, return_distance=False)[:, 1:]

    def get_neighbors(self, city_id: int) -> List[int]:
        return self.idx_list[city_id].tolist()
