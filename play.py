import subprocess

def create_tables():
    subprocess.run(["python", "data_collection/create_tables.py"])

# def get_hotels():
#     subprocess.run(["python", "data_collection/get_hotels.py"])

# def get_poi():
#     subprocess.run(["python", "data_collection/get_poi.py"])

def generate_map_hotels():
    subprocess.run(["jupyter", "nbconvert", "--to", "script", "map/map_hotels.ipynb"])
    subprocess.run(["python", "map/map_hotels.py"])

def generate_map_poi():
    subprocess.run(["jupyter", "nbconvert", "--to", "script", "map/map_poi.ipynb"])
    subprocess.run(["python", "map/map_poi.py"])

def generate_map_all_points():
    subprocess.run(["jupyter", "nbconvert", "--to", "script", "map/map_all_points.ipynb"])
    subprocess.run(["python", "map/map_all_points.py"])

def generate_matrix():
    subprocess.run(["python", "create_matrix/proxy.py"])

def find_best_hotels():
    subprocess.run(["python", "finding_ways/start.py"])

def run_after_start():
    subprocess.run(["python", "finding_ways/after_start.py"])

def visualize_routes():
    subprocess.run(["python", "finding_ways/visualize_routes.py"])

def main():
    while True:
        print()
        print("Выберите действие:")
        print("1. Создать таблицы базы данных")
        # print("2. Получить данные о гостиницах")
        # print("3. Получить данные о точках интереса")
        print("2. Сгенерировать карту с гостиницами")
        print("3. Сгенерировать карту с точками к посещению")
        print("4. Сгенерировать карту с найденными гостиницами и точками к посещению")
        print("5. Сгенерировать матрицу расстояний и времени")
        print("6. Найти лучшие варианты гостиниц")
        print("7. Построить маршруты")
        print("0. Завершить")
        print()

        choice = input("Введите номер действия: ")

        if choice == "0":
            print("Программа завершена")
            break

        actions = {
            '1': create_tables,
            # '2': get_hotels,
            # '3': get_poi,
            '2': generate_map_hotels,
            '3': generate_map_poi,
            '4': generate_map_all_points,
            '5': generate_matrix,
            '6': find_best_hotels,
            '7': run_after_start
        }

        if choice in actions:
            actions[choice]()
            if choice == '7':
                visualize_routes()
                print("Готовые маршруты содержатся в папке 'routes'")
        else:
            print("Ошибка. Некорректный выбор")

if __name__ == "__main__":
    main()
