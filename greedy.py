import numpy as np
import pandas as pd
from itertools import permutations

def generate_routes(points_sequence):
    routes = []
    for r in range(len(points_sequence), 0, -1):
        routes.extend(permutations(points_sequence, r))
    return routes

def shortest_route(time_matrix, start_point, points_sequence, max_time):
    min_time = float('inf')
    best_route = 0
    all_routes = generate_routes(points_sequence)
    for route in all_routes:
        route = [start_point] + list(route) + [start_point]
        time = sum(time_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        if time <= max_time and time < min_time:
            min_time = time
            best_route = route
    return best_route, min_time

def greedy_algorithm(time_matrix, start_point, points_sequence, days, max_time_per_day):
    routes_per_day = []
    time_per_day = []
    any_day_possible = False
    unsatisfied_points = set(points_sequence)
    for _ in range(days):
        sorted_routes = sorted(generate_routes(unsatisfied_points), key=len, reverse=True)
        for route in sorted_routes:
            route = [start_point] + list(route) + [start_point]
            time = sum(time_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
            if time <= max_time_per_day:
                routes_per_day.append(route)
                time_per_day.append(time)
                for point in route[1:-1]:
                    unsatisfied_points.remove(point)
                any_day_possible = True
                break
    return routes_per_day, time_per_day, any_day_possible, unsatisfied_points

def calculate_total_distance(route, distance_matrix):
    total_distance = sum(distance_matrix[route[i - 1]][route[i]] for i in range(1, len(route))) + distance_matrix[route[-1]][route[0]]
    return total_distance

time_matrix = pd.read_csv('D:\\vkrb\\csv\\time_matrix.csv', header=None).values
distance_matrix = pd.read_csv('D:\\vkrb\\csv\\distance_matrix.csv', header=None).values

start_point = 0
points_sequence = [1, 2, 3]
days = 2
max_time_per_day = 30

routes, times, possible, unsatisfied_points = greedy_algorithm(time_matrix, start_point, points_sequence, days, max_time_per_day)

if possible:
    for i in range(len(routes)):
        total_distance = calculate_total_distance(routes[i], distance_matrix)
        print(f"День: {i+1}, Маршрут: {routes[i]}, Время: {times[i]}, Расстояние: {total_distance}")
    if unsatisfied_points:
        print(f"Точки невозможно соблюсти: {unsatisfied_points}")
else:
    print(f"Невозможно построить маршруты в указанные дни")
