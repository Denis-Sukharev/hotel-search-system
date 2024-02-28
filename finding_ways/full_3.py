import itertools
import pandas as pd

def is_valid_route(route, matrix, time_limit):
    total_time = 0
    for i in range(len(route) - 1):
        total_time += matrix[route[i]][route[i+1]]
        if total_time > time_limit:
            return False
    return True

# Функция, которая сверяет повторения точек между каждым вариантом маршрутов
# Например, 1) Маршрут: (0, 1, 3, 0), Время: 50, Маршрут: (0, 2, 1, 0), Время: 50, тут есть повторение точек 1 поэтому его мы в следующий раз не выводим
def check_point_repetition(variant):
    visited_points = set()
    for route, _ in variant:
        for point in route[1:-1]:
            if point in visited_points:
                return True # найдено повторение точки
            visited_points.add(point)
    return False # не найдено повторение точки

# Функция, которая после check_point_repetition среди ее резульатов будет выбирать оптимальным решением тот вариант, в котором содержится бОльшее число точек и минимальная сумма времени
def find_optimal_variant(variants):
    max_points = 0
    min_total_time = float('inf')
    optimal_variant = []

    for variant in variants:
        total_time = sum(time for _, time in variant)
        points = sum(1 for point in variant[0][0][1:-1])

        if points > max_points or (points == max_points and total_time < min_total_time):
            max_points = points
            min_total_time = total_time
            optimal_variant = variant

    return optimal_variant

def find_optimal_solution_2(time_matrix, distance_matrix, start_node, time_limit, days, points_sequence):
    remaining_points = set(points_sequence)
    all_routes = []
    optimal_routes = []
    found_solution = False 
    remaining_days = days  # переменная для отслеживания оставшихся дней

    while remaining_days > 0:
        routes_info = []
        for r in range(1, len(points_sequence) + 1):
            for route in itertools.permutations(remaining_points, r):
                route = (start_node,) + route + (start_node,)
                if is_valid_route(route, time_matrix, time_limit):
                    route_time = sum(time_matrix[route[i]][route[i+1]] for i in range(len(route) - 1))
                    routes_info.append((route, route_time))
        for route, time in routes_info:
            all_routes.append((route, time))
        if routes_info:
            optimal_route = routes_info[0][0]
            remaining_points -= set(optimal_route[1:-1])
            optimal_routes.append((optimal_route, routes_info[0][1]))
            if not remaining_points:  # если не осталось нерассмотренных точек
                found_solution = True  # True, если найдено решение
                break

        remaining_days -= 1  # уменьшение количества оставшихся дней

    if found_solution:
        print(f"\nРешение полным перебором за {days - remaining_days + 1} дней:")
        total_time = sum(time for _, time in optimal_routes)
        if total_time == 0:
            print("Оптимальный маршрут не найден")
        else:
            for i, (route, time) in enumerate(optimal_routes, start=1):
                total_distance = sum(distance_matrix[route[i-1]][route[i]] for i in range(1, len(route)))
                print(f"День: {i}, Маршрут: {route}, Время: {time}, Расстояние: {total_distance}")
            optimal_points = set()
            for route, _ in optimal_routes:
                optimal_points.update(route[1:-1])

    return found_solution

'''if __name__ == "__main__":
    time_matrix = pd.read_csv('D:\\vkrb\\csv\\time_matrix.csv', header=None).values
    distance_matrix = pd.read_csv('D:\\vkrb\\csv\\distance_matrix.csv', header=None).values
    start_node = 0
    time_limit = 40
    days = 10
    points_sequence = [1, 2, 3]
    found_solution = False

    while not found_solution and days <= 30:
        found_solution = find_optimal_solution_2(time_matrix, distance_matrix, start_node, time_limit, days, points_sequence)

        if found_solution:
            break
        else:
            days += 1
    if not found_solution:
        print(f"Не удается найти решение")'''
