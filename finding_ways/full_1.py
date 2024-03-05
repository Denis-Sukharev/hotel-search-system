import itertools
import pandas as pd

def brute_force_algorithm(time_matrix, start_point, points_sequence, max_time_day):
    shortest_route = 0
    shortest_time = float('inf')
    unsatisfied_points = set(points_sequence)

    all_permutations = itertools.permutations(points_sequence)

    for perm in all_permutations:
        route = [start_point] + list(perm) + [start_point]
        time = sum(time_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        
        if time <= max_time_day:
            if time < shortest_time:
                shortest_route = route
                shortest_time = time
            unsatisfied_points -= set(route[1:-1])

    return shortest_route, shortest_time, bool(shortest_route), unsatisfied_points

