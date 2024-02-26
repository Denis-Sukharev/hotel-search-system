# Находит только 1 путь

import pandas as pd
import itertools

def brute_force_algorithm(time_matrix, start_point, points_sequence, days, max_time_per_day):
    shortest_route = 0
    shortest_time = float('inf')
    unsatisfied_points = set(points_sequence)

    all_permutations = itertools.permutations(points_sequence)

    for perm in all_permutations:
        route = [start_point] + list(perm) + [start_point]
        time = sum(time_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        
        if time <= max_time_per_day:
            if time < shortest_time:
                shortest_route = route
                shortest_time = time
            unsatisfied_points -= set(route[1:-1])

    return shortest_route, shortest_time, bool(shortest_route), unsatisfied_points

time_matrix = pd.read_csv('D:\\vkrb\\csv\\time_matrix.csv', header=None).values
distance_matrix = pd.read_csv('D:\\vkrb\\csv\\distance_matrix.csv', header=None).values

start_point = 0
points_sequence = [1, 2, 3]
days = 2
max_time_per_day = 100

route, time, possible, unsatisfied_points = brute_force_algorithm(time_matrix, start_point, points_sequence, days, max_time_per_day)

if possible:
    total_distance = sum(distance_matrix[route[i-1]][route[i]] for i in range(1, len(route)))
    print(f"Маршрут: {route}, Время: {time}, Расстояние: {total_distance}")
    
    if unsatisfied_points:
        print(f"Точки невозможно соблюсти: {unsatisfied_points}")

else:
    print(f"Невозможно построить маршруты в указанные дни")
    print(f"Попробуйте уменьшить количество точек или увеличить время пребывания")
