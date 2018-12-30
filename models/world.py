import pandas as pd
import matplotlib.pyplot as plt
from models.city import City


class World:
    def __init__(self):
        self.cities = dict()
        self.df = pd.DataFrame()

    def add(self, city):
        """
        Adds a single city to the world
        """
        if isinstance(city, City):
            # checks if the object type added to the world is correct
            self.cities[city.id] = city
        else:
            raise TypeError('city must be a "__main__.City" object!')
        self.update_df()

    def remove_by_id(self, id_):
        """
        Removes a single city from the world
        """
        self.cities.pop(id_)

    def bulk_add_city(self, dataframe):
        """
        Adds cities in bulk from a DataFrame
        """
        dataframe['city'] = dataframe.apply(lambda x: City(x.iloc[0], x.iloc[1], x.iloc[2]), axis=1)
        dataframe = dataframe.drop(['X', 'Y'], axis=1)
        dataframe = dataframe.set_index('CityId')
        cities = dataframe.to_dict()['city']
        self.cities.update(cities)
        self.update_df()

    def size(self):
        """
        Gets the quantity of cities in the world
        """
        return self.df.shape[0]

    def primes(self):
        """
        Gets the world prime cities
        """
        return [c for idx, c in self.cities.items() if c.is_prime]

    def nonprimes(self):
        """
        Gets the world nonprime cities
        """
        return [c for idx, c in self.cities.items() if not c.is_prime]

    def north_pole(self):
        """
        Gets the North Pole
        """
        return self.cities[0]

    def ids(self):
        """
        Gets all world cities ids
        """
        return list(self.cities.keys())

    def get_city(self, id_):
        """
        Get a city by id
        """
        return self.cities[id_]

    def update_df(self):
        """
        Get cities coordinates as a dataframe
        """
        dataframe = pd.DataFrame.from_dict(self.cities, orient='index', columns=['city'])
        dataframe['x'] = dataframe.apply(lambda x: x.iloc[0].x, axis=1)
        dataframe['y'] = dataframe.apply(lambda x: x.iloc[0].y, axis=1)
        dataframe['id'] = dataframe.apply(lambda x: x.iloc[0].id, axis=1)
        dataframe['is_prime'] = dataframe.apply(lambda x: x.iloc[0].is_prime, axis=1)
        self.df = dataframe

    def plot(self, show_primes=False):
        """
        Creates a world plot, mark the north pole. Option to show primes in different collor
        """
        self.df.plot.scatter(x='x', y='y', s=0.07, figsize=(15, 10), c='green', alpha=0.6)

        if show_primes:
            coords = self.df[self.df['is_prime']]
            plt.scatter(x=coords.x, y=coords.y, c='red', s=0.1, alpha=0.6)

        plt.scatter(self.north_pole().x, self.north_pole().y, c='blue', s=16)
        plt.axis('off')

        return plt.show()
