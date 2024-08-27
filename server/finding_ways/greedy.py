from itertools import permutations

def generate_routes(points_sequence):
    routes = []
    for r in range(len(points_sequence), 0, -1):
        routes.extend(permutations(points_sequence, r))
    return routes

def greedy_algorithm(time_matrix, distance_matrix, start_point, points_sequence, days, time_limit):
    routes_per_day = []
    time_per_day = []
    any_day_possible = False
    unsatisfied_points = set(points_sequence)
    
    for _ in range(days):
        sorted_routes = sorted(generate_routes(unsatisfied_points), key=len, reverse=True)
        
        for route in sorted_routes:
            route = [start_point] + list(route) + [start_point]
            time = sum(time_matrix.loc[route[i], route[i+1]] for i in range(len(route)-1))
            
            if time <= time_limit:
                routes_per_day.append(route)
                time_per_day.append(time)
                
                for point in route[1:-1]:
                    unsatisfied_points.remove(point)
                any_day_possible = True
                break

    return routes_per_day, time_per_day, any_day_possible, unsatisfied_points


def calculate_total_distance(route, distance_matrix):
    total_distance = sum(distance_matrix.loc[route[i - 1], route[i]] for i in range(1, len(route))) + distance_matrix.loc[route[-1], route[0]]
    return total_distance
