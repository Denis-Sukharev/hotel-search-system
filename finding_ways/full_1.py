import itertools

def brute_force_algorithm(time_matrix, start_point, points_sequence, max_time_day):
    shortest_route = 0
    shortest_time = float('inf')

    all_permutations = itertools.permutations(points_sequence)

    for perm in all_permutations:
        route = [start_point] + list(perm) + [start_point]
        time = sum(time_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        
        if time <= max_time_day:
            if time < shortest_time:
                shortest_route = route
                shortest_time = time

    return shortest_route, shortest_time, bool(shortest_route)

