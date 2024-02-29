import pandas as pd
from greedy import greedy_algorithm, calculate_total_distance
from full_1 import brute_force_algorithm
from full_2 import find_optimal_solution
from full_3 import find_optimal_solution_2

if __name__ == "__main__":
    # ВВОДНЫЕ ДАННЫЕ:
    time_matrix = pd.read_csv('D:\\vkrb\\csv\\time_matrix.csv', header=None).values
    distance_matrix = pd.read_csv('D:\\vkrb\\csv\\distance_matrix.csv', header=None).values
    start_node = 0
    time_limit = 40
    days = 2
    points_sequence = [1, 2, 3]

    # ПОЛНЫЙ ПЕРЕБОР:
    best_route_brute, best_time_brute, is_possible_brute, unsatisfied_points_brute = brute_force_algorithm(time_matrix, start_node, points_sequence, time_limit)

    if is_possible_brute:
        print("Маршрут за 1 день полным перебором:")
        print(f"Маршрут: {best_route_brute}, Время: {best_time_brute}, Расстояние: {sum(distance_matrix[best_route_brute[i - 1]][best_route_brute[i]] for i in range(1, len(best_route_brute)))}")
    else:
        find_optimal_solution(time_matrix, distance_matrix, start_node, time_limit, days, points_sequence)

    # ЖАДНЫЙ АЛГОРИТМ:
    routes_greedy, times_greedy, any_day_possible, unsatisfied_points = greedy_algorithm(time_matrix, start_node, points_sequence, days, time_limit)

    if any_day_possible:
        print("\nРешение жадным алгоритмом:")
        for i in range(len(routes_greedy)):
            total_distance_greedy = calculate_total_distance(routes_greedy[i], distance_matrix)
            print(f"День: {i+1}, Маршрут: {routes_greedy[i]}, Время: {times_greedy[i]}, Расстояние: {total_distance_greedy}")

        if unsatisfied_points:
            print(f"Точки не учтены: {unsatisfied_points}")

    else:
        print(f"Невозможно построить маршруты в указанные дни жадным алгоритмом\nПопробуйте уменьшить количество точек или увеличить дни пребывания")

    
    
    # ДОПОЛНИТЕЛЬНО. Поиск решения полным перебором с чтобы соблюсти все точки:
    found_solution = False

    while not found_solution and days <= 30:
        found_solution = find_optimal_solution_2(time_matrix, distance_matrix, start_node, time_limit, days, points_sequence)

        if found_solution:
            break
        else:
            days += 1
    if not found_solution:
        print(f"Не удается найти решение")
    
    


# # Ограничение 20, 2:
# 0,5,10,15
# 20,0,15,5
# 8,1,0,10
# 0,0,0,0
    
# # Ограничение 50, 2:
# 0,10,20,40
# 15,0,15,20
# 30,15,0,10
# 20,20,20,0

# # Ограничение 40, 3:
# 0,20,20,20
# 20,0,20,20
# 20,20,0,20
# 20,20,20,0