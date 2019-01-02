from models.route import Route

print('Initializing')
route = Route.initialize()
print('Initial Cost: {}'.format(route.cost()))

print('Solving with Concorde.')
route.solve_by_concorde(time=5.0)
print('Concorde Cost: {}'.format(route.cost()))

print('Start improve_9th.')
route.improve_9th()
print('Improve 9th Cost: {}'.format(route.cost()))
