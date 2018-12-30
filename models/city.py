import math


class City:
    def __init__(self, id_, x, y):
        self.x = x
        self.y = y
        self.id = id_
        self.is_visited = False
        self.is_prime = self._check_prime()

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

    def visit(self):
        """
        Mark city as visited
        """
        self.is_visited = True

    def get_coord(self):
        return self.x, self.y

    def __repr__(self):
        """
        Prints all the properties of the object. idea is to be as verbose as possible.
        Implementing __repr__ or __str__ will make it easy to print and inspect in the notebook.
        """
        fmt_str = 'CityId: {} \nCoordinates: {}\nIs prime: {}\nIs visited: {}'
        return fmt_str.format(self.id, self.get_coord(), self.is_prime, self.is_visited)
