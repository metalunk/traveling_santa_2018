import io
import base64
import numpy as np
import pylab as pl
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from typing import List
from matplotlib import collections as mc
from concorde.tsp import TSPSolver
from IPython.display import HTML

from models.city import City
from models.edge import Edge


class Route:
    def __init__(self, stops):
        # List of City
        self.stops: List[City] = stops

    def size(self):
        """
        Calculates the number of stops in the path
        """
        return len(self.stops)

    def cost(self):
        """
        Calculates the Path Cost Function - penalized distance of the full path
        """
        cost = 0
        for idx, cur_stop in enumerate(self.stops):
            next_stop = (idx + 1) % self.size()
            cost += Edge.get_edge_cost(idx, cur_stop, self.stops[next_stop])
        return cost

    def get_tenth_steps(self):
        """
        Get the cities of all 10th steps
        """
        return [c for s, c in enumerate(self.stops) if (s + 1) % 10 == 0]

    def swap_if_better(self, edge_a: Edge, edge_b: Edge):
        if edge_a.idx > edge_b.idx:
            tmp = edge_b
            edge_b = edge_a
            edge_a = tmp

        # Currently I don't implement too close swap
        if edge_a.idx + 1 >= edge_b.idx:
            return

        swapped_edge_a = Edge(edge_a.idx, edge_a.first_city, edge_b.first_city)
        swapped_edge_b = Edge(edge_b.idx, edge_a.second_city, edge_b.first_city)
        if swapped_edge_a.cost() + swapped_edge_b.cost() > edge_a.cost() + edge_b.cost():
            return

        tmp = self.stops[edge_a.idx + 1:edge_b.idx + 1]
        for i in range(edge_a.idx + 1, edge_b.idx + 1):
            self.stops[i] = tmp.pop()

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
