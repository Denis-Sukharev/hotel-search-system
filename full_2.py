import itertools

def is_valid_route(route, matrix, time_limit):
    total_time = 0
    for i in range(len(route) - 1):
        total_time += matrix[route[i]][route[i+1]]
        if total_time > time_limit:
            return False
    return True

# Функция, которая сверяет повторения точек между каждый вариантом маршрутов
# Например, 1) Маршрут: (0, 1, 3, 0), Время: 50, Маршрут: (0, 2, 1, 0), Время: 50, тут есть повторение точек 1 поэтому его мы в следующий раз не выводим
def check_point_repetition(variant):
    visited_points = set()
    for route, _ in variant:
        for point in route[1:-1]:
            if point in visited_points:
                return True  # Найдено повторение точки
            visited_points.add(point)
    return False  # Повторений не найдено

# Функция, которая после check_point_repetition среди ее резульатов будет выбирать оптимальным решением тот вариант в котором содержится бОльшее число точек и минимальная сумма времени
def find_optimal_variant(variants):
    max_points = 0
    min_total_time = float('inf')
    optimal_variant = None

    for variant in variants:
        total_time = sum(time for _, time in variant)
        points = sum(1 for point in variant[0][0][1:-1])

        if points > max_points or (points == max_points and total_time < min_total_time):
            max_points = points
            min_total_time = total_time
            optimal_variant = variant

    return optimal_variant

def find_optimal_solution(matrix, start_node, time_limit, days, points_sequence):
    remaining_points = set(points_sequence)
    all_routes = []
    optimal_routes = []
    min_total_time = float('inf')
    
    for day in range(1, days + 1):
        print(f"День: {day}")
        routes_info = []
        for r in range(1, len(points_sequence) + 1):
            for route in itertools.permutations(remaining_points, r):
                route = (start_node,) + route + (start_node,)
                if is_valid_route(route, matrix, time_limit):
                    route_time = sum(matrix[route[i]][route[i+1]] for i in range(len(route) - 1))
                    routes_info.append((route, route_time))
        routes_info.sort(key=lambda x: (len(x[0]) - 2, x[1]), reverse=True)
        for route, time in routes_info:
            print(f"Маршрут: {route}, Время: {time}")
            all_routes.append((route, time))
        if routes_info:
            optimal_route = routes_info[0][0]
            remaining_points -= set(optimal_route[1:-1])
            optimal_routes.append((optimal_route, routes_info[0][1]))
        else:
            print("Невозможно построить маршрут на текущий день.")
            break
    
    print("\nВсе возможные маршруты:")
    variants = list(itertools.combinations(all_routes, days))
    filtered_variants = [variant for variant in variants if not check_point_repetition(variant)]
    for i, variant in enumerate(filtered_variants, start=1):
        print(f"{i}) ", end="")
        for route, time in variant:
            print(f"Маршрут: {route}, Время: {time}", end=", ")
        print()
    
    optimal_variant = find_optimal_variant(filtered_variants)
    
    print("\nОптимальное решение:")
    for route, time in optimal_variant:
        print(f"Маршрут: {route}, Время: {time}")
    total_time = sum(time for _, time in optimal_variant)
    print(f"Суммарное время: {total_time}")

if __name__ == "__main__":
    matrix = [
        [0, 10, 20, 40],
        [15, 0, 15, 20],
        [30, 15, 0, 10],
        [20, 20, 20, 0]
    ]
    start_node = 0
    time_limit = 50
    days = 2
    points_sequence = [1, 2, 3]

    find_optimal_solution(matrix, start_node, time_limit, days, points_sequence)
