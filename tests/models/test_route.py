from models.city import City, AreaMap
from models.route import Route


def test_try_swap():
    cities = City.load_from_csv('data/sample_cities.csv')
    area_map = AreaMap(cities)
    route = Route(cities, area_map)

    assert round(route.cost(), 3) == 4.828

    route.try_swap(2, [route.stops[3]])

    assert route.cost() == 4.0
