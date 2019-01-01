from models.city import City


class Edge:
    def __init__(self, idx: int, first_city: City, second_city: City):
        self.idx: int = idx
        self.first_city: City = first_city
        self.second_city: City = second_city

    def cost(self) -> float:
        return self.get_edge_cost(self.idx, self.first_city, self.second_city)

    @staticmethod
    def get_edge_cost(idx: int, first_city: City, second_city: City) -> float:
        d = City.distance(first_city, second_city)
        return d * (1.0 + 0.1 * int((idx + 1) % 10 == 0) * int(not first_city.is_prime))
