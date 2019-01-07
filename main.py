from helper import load_from_pickle
from models.route import Route

print('Loading initial route from pkl.')
route: Route = load_from_pickle('data/initial_route.pkl', Route.initialize)
print('Initial Cost: {}'.format(route.cost()))

print('Loading Concorde 30 route from pkl.')
route: Route = load_from_pickle('data/concorde_30.pkl', lambda: route.solve_by_concorde(30.0 * 60.0))
print('Concorde 30 Cost: {}'.format(route.cost()))

print('Start improve_9th.')
route.improve_9th()
print('Improve 9th Cost: {}'.format(route.cost()))
