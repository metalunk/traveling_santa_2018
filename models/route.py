import io
import base64

import numpy as np
import pylab as pl
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from typing import List, Dict
from matplotlib import collections as mc
from concorde.tsp import TSPSolver
from IPython.display import HTML

from helper import load_from_pickle
from models.city import City, AreaMap
from models.edge import Edge


class Route:
    def __init__(self, stops: List[City], area_map: AreaMap):
        # List of City
        self.stops: List[City] = stops
        # Dict of city_id -> index
        self.city_to_idx: Dict[int, int] = self.initialize_city_to_idx(self.stops)

        self.area_map: AreaMap = area_map

    @staticmethod
    def initialize():
        cities = City.load_from_csv()
        area_map: AreaMap = load_from_pickle('data/area_map.pkl', lambda: AreaMap(cities))
        return Route(cities, area_map)

    @staticmethod
    def initialize_city_to_idx(stops: List[City]) -> Dict[int, int]:
        print('Creating city_to_idx.')
        city_to_idx = {}
        for i, stop in enumerate(stops):
            city_to_idx[stop.id] = i
        return city_to_idx

    def load_submission(self, submission: List[int]) -> None:
        new_stops = []
        for c in submission:
            idx = self.city_to_idx[c]
            new_stops.append(self.stops[idx])
        self.stops = new_stops
        self.city_to_idx = self.initialize_city_to_idx(self.stops)

    def size(self):
        return len(self.stops)

    def cost(self):
        return self.cost_of_path(self.stops + [self.stops[0]], 0)

    def get_city(self, idx: int) -> City:
        if idx < self.size():
            return self.stops[idx]
        elif idx == self.size():
            return self.stops[0]
        else:
            raise IndexError('Index of stops out of range.')

    def get_subpath(self, from_: int, to: int) -> List[City]:
        if to < self.size():
            return self.stops[from_:to + 1]
        elif to == self.size():
            return self.stops[from_:to] + [self.stops[0]]
        else:
            raise IndexError('Index of stops out of range.')

    def replace_city(self, idx: int, city: City) -> None:
        if idx < self.size():
            self.stops[idx] = city
        elif idx == self.size():
            self.stops[0] = city
        else:
            raise IndexError('Index of stops out of range.')

    @staticmethod
    def cost_of_path(path: List[City], first_idx: int) -> float:
        cost = 0
        for i, cur_stop in enumerate(path):
            if i + 1 >= len(path):
                return cost
            cost += Edge.get_edge_cost(i + first_idx, cur_stop, path[i + 1])

    def get_tenth_steps(self):
        """
        Get the cities of all 10th steps
        """
        return [c for s, c in enumerate(self.stops) if (s + 1) % 10 == 0]

    def improve_9th(self):
        for i in range(self.size()):
            idx = i + 1
            if idx % 10 == 9:
                city = self.get_city(i)
                neighbor_primes = city.get_neighbor_primes(self.area_map)
                self.try_swap(idx, neighbor_primes)

    def try_swap(self, idx: int, cities: List[City]) -> None:
        best_diff = 0
        best_subpath = None
        for city in cities:
            target_idx = self.city_to_idx[city.id]
            edge_a = Edge(idx - 1, self.get_city(idx - 1), self.get_city(idx))
            edge_b = Edge(target_idx, self.get_city(target_idx), self.get_city(target_idx + 1))
            swapped_subpath, diff = self.calc_swap(edge_a, edge_b)

            if diff is not None and diff < best_diff:
                best_diff = diff
                best_subpath = swapped_subpath

        if best_subpath is not None:
            # if round(previous_cost + best_diff, 3) != round(self.cost(), 3):
            #     raise RuntimeError('Bug is hidden.')
            print('Swapping idx: {}, improving {}'.format(idx, best_diff))
            self.replace_subpath(idx - 1, best_subpath)

    def calc_swap(self, edge_a: Edge, edge_b: Edge):
        """
        :param edge_a:
        :param edge_b:
        :return: (subpath, diff)
            diff: smaller is better
        """
        # Currently I don't implement former swap
        if edge_a.idx > edge_b.idx:
            return [], None

        # Currently I don't implement too close swap
        if edge_a.idx + 1 >= edge_b.idx:
            return [], None

        swapped_subpath = self.get_swapped_subpath(edge_a, edge_b)
        diff = self.cost_of_path(swapped_subpath, edge_a.idx) \
               - self.cost_of_path(self.get_subpath(edge_a.idx, edge_b.idx + 1), edge_a.idx)

        return swapped_subpath, diff

    def replace_subpath(self, from_idx: int, subpath: List[City]) -> None:
        for i in range(len(subpath)):
            city = subpath.pop(0)
            self.replace_city(from_idx + i, city)
            self.city_to_idx[city.id] = from_idx + i

    def get_swapped_subpath(self, edge_a: Edge, edge_b: Edge) -> List[City]:
        swapped_subpath = [edge_a.first_city]
        tmp = self.get_subpath(edge_a.idx + 1, edge_b.idx)
        tmp.reverse()
        swapped_subpath += tmp
        swapped_subpath.append(edge_b.second_city)
        return swapped_subpath

    def solve_by_concorde(self, time: float):
        """
        Solve the problem with concorde solver
        """
        x = [c.x for c in self.stops[:-1]]
        y = [c.y for c in self.stops[:-1]]

        # Instantiate solver
        solver = TSPSolver.from_data(x, y, norm="EUC_2D")

        # solve
        tour_data = solver.solve(time_bound=time, verbose=True, random_seed=42)

        # Reorder the route with concorde solution
        order = np.append(tour_data.tour, [0])
        new_route = [self.stops[i] for i in order]
        self.stops = new_route
        self.city_to_idx = self.initialize_city_to_idx(self.stops)

    def plot(self, show_primes=False, show_10th_step=False, show_intersection=False):
        """
        Plot the route
        """
        lwidth, lalpha = 0.4, 0.6
        lines = [[self.stops[i].get_coord(), self.stops[i + 1].get_coord()] for i in range(0, self.size() - 1)]
        lc = mc.LineCollection(lines, linewidths=lwidth, alpha=lalpha, colors='red')
        fig, ax = pl.subplots(figsize=(20, 20))

        ax.set_aspect('equal')
        ax.add_collection(lc)
        ax.autoscale()

        if show_primes:
            x_list = []
            y_list = []
            for stop in self.stops:
                if stop.is_prime:
                    x_list.append(stop.x)
                    y_list.append(stop.y)
            pc = plt.scatter(x=x_list, y=y_list, c='green', s=3, alpha=0.3)
            ax.add_collection(pc)

    def animation(self, steps=500):
        """
        Creates a route animation
        """
        lwidth, lalpha = 0.4, 0.6
        lines = [[self.stops[i].get_coord(), self.stops[i + 1].get_coord()] for i in range(0, self.size() - 1)]
        fig, ax = pl.subplots(figsize=(15, 15))
        line, = ax.plot([], [], linewidth=lwidth, alpha=lalpha, color='red')
        ax.set_ylim(0, 3650)
        ax.set_xlim(0, 5250)

        def animate(i):
            s = int(i + 1) * steps
            try:
                data = lines[s - steps:s]
            except IndexError:
                data = lines
            lc = mc.LineCollection(data, linewidths=lwidth, alpha=lalpha, colors='red')
            ax.add_collection(lc)

        ani = animation.FuncAnimation(fig, animate, frames=int(len(lines) / steps), repeat=True)
        ani.save('test.gif', writer='imagemagick', fps=20)
        plt.close(1)
        filename = 'test.gif'
        video = io.open(filename, 'r+b').read()
        encoded = base64.b64encode(video)
        return HTML(data='''<img src="data:image/gif;base64,{0}" type="gif" />'''.format(encoded.decode('ascii')))
