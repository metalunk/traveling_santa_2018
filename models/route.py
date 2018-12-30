import io
import base64
import math
import numpy as np
import pandas as pd
import pylab as pl
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import collections as mc
from concorde.tsp import TSPSolver
from IPython.display import HTML


class Route:
    def __init__(self, world):
        # Init path with just the North Pole
        self.world = world
        self.stops = [self.world.north_pole()]
        self.tenth_steps = []
        self.prime_tenth_steps = self.get_prime_tenth_steps()

    @staticmethod
    def distance(a, b):
        """
        calculates the euclidian distance between 2 cities
        """
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    def size(self):
        """
        Calculates the number of stops in the path
        """
        return len(self.stops)

    def add(self, ids):
        """
        Add stop to path
        """
        if isinstance(ids, type(list())):
            for id_ in ids:
                self.stops.append(self.world.get_city(id_))
        elif isinstance(ids, type(int())):
            self.stops.append(self.world.get_city(ids))

    def add_world(self):
        """
        Adds all cities in the world to the route
        """
        self.add(list(range(1, self.world.size())))

    def cost(self):
        """
        Calculates the Path Cost Function - penalized distance of the full path
        """
        dist = 0
        l = self.size()
        for idx, stop in enumerate(self.stops):
            curr_ = stop
            step_number = idx + 1
            if step_number < l:
                next_ = self.stops[step_number]
            if step_number % 10 == 0 and not curr_.is_prime:
                dist += self.distance(curr_, next_) * 1.1
            else:
                dist += self.distance(curr_, next_)
        return dist

    def euclidean_cost(self):
        """
        Calculates the Path Cost Function - without penalties
        """
        dist = 0
        l = self.size()
        for idx, stop in enumerate(self.stops):
            curr_ = stop
            step_number = idx + 1
            if step_number < l:
                next_ = self.stops[step_number]
            dist += self.distance(curr_, next_)
        return dist

    def penalty(self):
        """
        Total penalty by not going to prime cities
        """
        return self.cost() - self.euclidean_cost()

    def get_tenth_steps(self):
        """
        Get the cities of all 10th steps
        """
        self.tenth_steps = [c for s, c in enumerate(self.stops) if (s + 1) % 10 == 0]
        return self.tenth_steps

    def get_prime_tenth_steps(self):
        """
        Get cities in 10th steps that are prime
        """
        primes = self.world.primes()
        self.prime_tenth_steps = [c for c in self.tenth_steps if c in primes]
        return self.prime_tenth_steps

    def get_ids(self):
        """
        Get a ordered list of all city ids in the path.
        """
        return [c.id for c in self.stops]

    def concorde(self, time):
        """
        Solve the problem with concorde solver. Without penalization of prime cities.
        """
        x = [c.x for c in self.stops[:-1]]
        y = [c.y for c in self.stops[:-1]]

        # Instantiate solver
        solver = TSPSolver.from_data(x, y, norm="EUC_2D")

        # solve
        tour_data = solver.solve(time_bound=float(time), verbose=True, random_seed=42)

        # Reorder the route with concorde solution
        order = np.append(tour_data.tour, [0])
        new_route = [self.stops[i] for i in order]
        self.stops = new_route

    def plot(self, show_primes=False, show_10th_step=False, show_intersection=False):
        """
        Plot the route
        """
        lwidth, lalpha = 0.4, 0.6
        lines = [[self.stops[i].coord, self.stops[i + 1].coord] for i in range(0, self.size() - 1)]
        lc = mc.LineCollection(lines, linewidths=lwidth, alpha=lalpha, colors='red')
        fig, ax = pl.subplots(figsize=(20, 20))

        ax.set_aspect('equal')
        ax.add_collection(lc)
        ax.autoscale()

        if show_primes:
            # get coords of prime cities
            coords = self.world.df[self.world.df['is_prime']]
            # plot
            pc = plt.scatter(x=coords.x, y=coords.y, c='green', s=3, alpha=0.3)
            ax.add_collection(pc)

        if show_10th_step:
            # get coords of each 10th stop
            coords = [c.coord for c in self.tenth_steps]
            coords = pd.DataFrame(coords, columns=['x', 'y'])
            # plot
            pc = plt.scatter(x=coords.x, y=coords.y, c='blue', s=3, alpha=0.3)
            ax.add_collection(pc)
        if show_intersection:
            # get coords of each 10th stop
            coords = [c.coord for c in self.prime_tenth_steps]
            coords = pd.DataFrame(coords, columns=['x', 'y'])
            # plot
            pc = plt.scatter(x=coords.x, y=coords.y, c='black', s=4, alpha=0.5)
            ax.add_collection(pc)
            return

    def animation(self, steps=500):
        """
        Creates a route animation
        """
        lwidth, lalpha = 0.4, 0.6
        lines = [[self.stops[i].coord, self.stops[i + 1].coord] for i in range(0, self.size() - 1)]
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

    def load(self, path):
        """
        Loads external solution from csv file
        """
        df = pd.read_csv(path)
        ids = df['Path'].values.tolist()
        self.stops = []
        for id_ in ids:
            self.stops.append(self.world.get_city(id_))

    def submit(self, filename):
        """
        Export the path as a csv, on the required submission format
        """
        dataframe = pd.DataFrame(self.stops, columns=['city'])
        dataframe['Path'] = dataframe.apply(lambda x: x.iloc[0].id, axis=1).astype(int)
        dataframe[['Path']].to_csv(filename, index=False)
