import pandas as pd

from models.city import City
from models.edge import Edge
from models.route import Route

df = pd.read_csv('data/sample_cities.csv')
cities = City.load_from_csv('data/sample_cities.csv')
route = Route(cities)
print('Cost: {}'.format(route.cost()))

edge_a = Edge(1, route.stops[1], route.stops[2])
edge_b = Edge(3, route.stops[3], route.stops[0])
route.swap_if_better(edge_a, edge_b)

print('Cost: {}'.format(route.cost()))
