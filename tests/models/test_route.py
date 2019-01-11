from models.city import City, Neighbors
from models.route import Route


def test_try_swap():
    cities = City.load_from_csv('data/sample_cities.csv')
    neighbors = Neighbors(cities)
    route = Route(cities, neighbors)

    assert round(route.cost(), 3) == 4.828

    route.try_swap(2, [route.stops[3]])

    assert route.cost() == 4.0
