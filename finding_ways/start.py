import os
import pandas as pd
from greedy import greedy_algorithm, calculate_total_distance
from full_1 import brute_force_algorithm
from full_2 import find_optimal_solution

def save_best_routes(results):
    if not os.path.exists('best_routes'):
        os.makedirs('best_routes')

    for result in results[:5]:
        filename = f"best_routes/{result['hotel'].replace(' ', '_')}.csv"
        with open(filename, 'w') as f:
            if isinstance(result['route'][0], list):  # Проверяем, если данные маршруты встречаются в квадратных скобках
                for route in result['route']:
                    for point in route:
                        f.write(f"{point}\n")
                    f.write("\n")  # Добавляем пустую строку между маршрутами
            else:
                for coordinate in result['route']:
                    f.write(f"{coordinate}\n")


if __name__ == "__main__":
    hotels = pd.read_csv('D:\\vkrb\\csv\\hotels.csv')
    results = []

    hours = int(input("Введите временное ограничение (в часах): "))
    time_limit = hours * 3600
    days = int(input("Введите количество дней: "))
    poi_data = pd.read_csv('D:\\vkrb\\csv\\poi.csv')
    print("Доступные достопримечательности:")
    for index, row in poi_data.iterrows():
        print(f"{row['poi_id']}, {row['name']}")

    poi_ids_input = input("Введите до 9 ID точек через запятую: ")
    points_sequence = [int(poi_id.strip()) for poi_id in poi_ids_input.split(',') if poi_id.strip()][:9]

    for index, hotel in hotels.iterrows():
        start_node = hotel['poi_id']
        print(f"\nОбработка отеля {hotel['name']} (poi_id: {start_node}):")

        # ВВОДНЫЕ ДАННЫЕ:
        matrix = pd.read_csv('D:\\vkrb\\csv\\matrix.csv')
        time_matrix = matrix.set_index(['mapped_object_start', 'mapped_object_finish'])['duration'].unstack(fill_value=0)
        distance_matrix = matrix.set_index(['mapped_object_start', 'mapped_object_finish'])['distance'].unstack(fill_value=0)      

        # ПОЛНЫЙ ПЕРЕБОР:
        best_route_brute, best_time_brute, is_possible_brute = brute_force_algorithm(time_matrix, start_node, points_sequence, time_limit)

        if is_possible_brute:
            total_distance_brute = sum(distance_matrix[best_route_brute[i - 1]][best_route_brute[i]] for i in range(1, len(best_route_brute)))
            print("Маршрут за 1 день полным перебором:")
            print(f"Маршрут: {best_route_brute}, Время: {best_time_brute}, Расстояние: {total_distance_brute}")
            total_time_brute = best_time_brute
            route_list_str = best_route_brute
        else:
            total_time_brute, total_distance_brute, route_list_str, missing_points = find_optimal_solution(time_matrix, distance_matrix, start_node, time_limit, days, points_sequence)

        # ЖАДНЫЙ АЛГОРИТМ:
        routes_greedy, times_greedy, any_day_possible, unsatisfied_points = greedy_algorithm(time_matrix, distance_matrix, start_node, points_sequence, days, time_limit)

        if any_day_possible:
            print("\nРешение жадным алгоритмом:")
            total_distance_greedy = sum([calculate_total_distance(route, distance_matrix) for route in routes_greedy])

            for i, route in enumerate(routes_greedy, 1):
                total_distance_route = calculate_total_distance(route, distance_matrix)
                print(f"День: {i}, Маршрут: {route}, Время: {times_greedy[i-1]}, Расстояние: {total_distance_route}")

            if unsatisfied_points:
                print(f"Точки не учтены: {unsatisfied_points}")

            total_time_greedy = sum(times_greedy)

            if total_time_brute <= total_time_greedy:

                results.append({
                    'hotel': hotel['name'],
                    'route': [list(route) for route in routes_greedy] if route_list_str == [] else route_list_str,
                    'time': total_time_brute,
                    'distance': total_distance_brute,
                    'unsatisfied_points': unsatisfied_points if route_list_str == best_route_brute else (unsatisfied_points if route_list_str == [] else missing_points)
                })
            else:
                min_time = min(total_time_greedy, total_time_brute) if is_possible_brute else total_time_greedy
                results.append({
                'hotel': hotel['name'],
                'route': [list(route) for route in routes_greedy] if min_time == total_time_greedy else [list(best_route_brute)],
                'time': total_time_brute if min_time == total_time_brute else total_time_greedy,
                'distance': total_distance_brute if min_time == total_time_brute else total_distance_greedy,
                'unsatisfied_points': unsatisfied_points
            })
        else:
            print(f"\nНевозможно предложить решение жадным алгоритмом. Точки находятся слишком далеко")

    results.sort(key=lambda x: (len(x['unsatisfied_points']), x['time']))

    print("\n")
    for i, result in enumerate(results[:5], 1):
        print(f"{i}: {result['hotel']}, маршрут: {result['route']}, общее время: {result['time']}, общее расстояние: {result['distance']}, неучтенные точки : {result['unsatisfied_points']}")

    save_best_routes(results)