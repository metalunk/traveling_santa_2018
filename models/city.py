import math


class City:
    def __init__(self, id_, x, y):
        self.x = x
        self.y = y
        self.coord = (x, y)
        self.id = id_
        self.is_visited = False
        self.is_prime = self.check_prime()

    def check_prime(self):
        """
        Checks if a city is prime
        """
        if self.id % 2 == 0 and self.id > 2:
            return False
        return all(self.id % i for i in range(3, int(math.sqrt(self.id)) + 1, 2))

    def visit(self):
        """
        Mark city as visited
        """
        self.is_visited = True

    def __repr__(self):
        """
        Prints all the properties of the object. idea is to be as verbose as possible.
        Implementing __repr__ or __str__ will make it easy to print and inspect in the notebook.
        """
        fmt_str = 'CityId: {} \nCoordinates: {}\nIs prime: {}\nIs visited: {}'
        return fmt_str.format(self.id, self.coord, self.is_prime, self.is_visited)
