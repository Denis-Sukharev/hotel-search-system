import itertools
import pandas as pd

def brute_force_algorithm(time_matrix, start_point, points_sequence, _):
    shortest_route = 0
    shortest_time = float('inf')
    unsatisfied_points = set(points_sequence)

    all_permutations = itertools.permutations(points_sequence)

    for perm in all_permutations:
        route = [start_point] + list(perm) + [start_point]
        time = sum(time_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        
        if time < shortest_time:
            shortest_route = route
            shortest_time = time
        unsatisfied_points -= set(route[1:-1])

    return shortest_route, shortest_time, bool(shortest_route), unsatisfied_points

'''if __name__ == "__main__":
    time_matrix = pd.read_csv('D:\\vkrb\\csv\\time_matrix.csv', header=None).values
    distance_matrix = pd.read_csv('D:\\vkrb\\csv\\distance_matrix.csv', header=None).values
    start_node = 0
    time_limit = 100
    days = 2
    points_sequence = [1, 2, 3]

    best_route, best_time, is_possible, unsatisfied_points = brute_force_algorithm(time_matrix, start_node, points_sequence, time_limit)

    if is_possible:
        print("Маршрут за 1 день полным перебором:")
        print(f"Маршрут: {best_route}, Время: {best_time}, Расстояние: {sum(distance_matrix[best_route[i - 1]][best_route[i]] for i in range(1, len(best_route)))}")
    # else:
    #     print("Невозможно построить маршрут полным перебором за 1 день")'''

