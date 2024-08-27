import itertools
from fastapi import HTTPException, status

def is_valid_route(route, matrix, time_limit):
    total_time = 0
    for i in range(len(route) - 1):
        total_time += matrix.loc[route[i], route[i+1]]
        if total_time > time_limit:
            return False
    return True

def check_point_repetition(variant):
    visited_points = set()
    for route, _ in variant:
        for point in route[1:-1]:
            if point in visited_points:
                return True
            visited_points.add(point)
    return False

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

def find_optimal_solution(time_matrix, distance_matrix, start_node, time_limit, days, points_sequence):
    remaining_points = set(points_sequence)
    all_routes = []
    optimal_routes = []
    total_distance = 0
    total_time = 0
    route_list_str = []
    missing_points = set()

    for day in range(1, days + 1):
        routes_info = []
        for r in range(1, len(points_sequence) + 1):
            for route in itertools.permutations(remaining_points, r):
                route = (start_node,) + route + (start_node,)
                if is_valid_route(route, time_matrix, time_limit):
                    route_time = sum(time_matrix.loc[route[i], route[i+1]] for i in range(len(route) - 1))
                    routes_info.append((route, route_time))
                    total_distance += sum(distance_matrix.loc[route[i-1], route[i]] for i in range(1, len(route)))
        routes_info.sort(key=lambda x: (len(x[0]) - 2, x[1]), reverse=True)
        for route, time in routes_info:
            all_routes.append((route, time))
            total_time += time
        if routes_info:
            optimal_route = routes_info[0][0]
            remaining_points -= set(optimal_route[1:-1])
            optimal_routes.append((optimal_route, routes_info[0][1]))
        else:
            break
    
    variants = list(itertools.permutations(all_routes, days))
    unique_variants = set(variant for variant in variants if not check_point_repetition(variant))
    optimal_variant = find_optimal_variant(unique_variants)
    
    if optimal_variant:
        # print("Решение полным перебором за несколько дней:")
        total_distance = sum(distance_matrix.loc[route[i-1], route[i]] for route, _ in optimal_variant for i in range(1, len(route)))
        route_list_str = [[point for point in route] for route, _ in optimal_variant]
        # for i, (route, time) in enumerate(optimal_variant, start=1):
        #     print(f"День: {i}, Маршрут: {route_list_str[i-1]}, Время: {time}, Расстояние: {sum(distance_matrix.loc[route[i-1], route[i]] for i in range(1, len(route)))}")
        total_route_times = [time for _, time in optimal_variant]
        total_time = sum(total_route_times)
        optimal_points = set()
        for route, _ in optimal_variant:
            optimal_points.update(route[1:-1])

        missing_points = set(points_sequence) - optimal_points
        # if missing_points:
        #     print(f"Точки не учтены: {missing_points}")
    else:
        print("Невозможно предложить решение полным перебором. Точки находятся слишком далеко")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )

    return total_time, total_distance, route_list_str, missing_points

