

import os
import requests
import subprocess
import yaml
from concurrent.futures import ThreadPoolExecutor
import random
import string

def get_proxy_ip(proxy):
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxy)
        if response.status_code == 200:
            data = response.json()
            return data['origin']
        else:
            print("Не удалось получить IP-адрес. Код состояния:", response.status_code)
            return None
    except Exception as e:
        print("Произошла ошибка:", str(e))
        return None

def update_params_file(params_file, api_key, profile):
    with open(params_file, 'r') as file:
        params = yaml.safe_load(file)
    
    params['api_key'] = api_key
    params['profile'] = profile

    with open(params_file, 'w') as file:
        yaml.dump(params, file)

def create_params_file(proxy_data, profile):
    proxy = {"http": proxy_data['http']}
    proxy_ip = get_proxy_ip(proxy)
    
    if proxy_ip:
        print(f"proxy ip", proxy_ip)

        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        params_file = f"params/params_proxy_{proxy_ip.replace('.', '_')}_{suffix}.yaml"

        params = {
            'output_format': 'geojson',
            'profile': profile,
            'units': 'm',
            'api_key': proxy_data["api_key"]
        }

        with open(params_file, 'w') as file:
            yaml.dump(params, file)

        return params_file

def execute_script_through_proxy(script_path, input_file, output_file, params_file, type_arg, proxy, start_index):
    try:
        command = f'python "{script_path}" -i "{input_file}" -o "{output_file}" -p "{params_file}" -t "{type_arg}" -s {start_index}'
        os.environ['HTTP_PROXY'] = proxy["http"]
        subprocess.run(command, shell=True)
        print(f"Выполнение скрипта через прокси {params_file} успешно")
    except Exception as e:
        print("Произошла ошибка:", str(e))
    finally:
        del os.environ['HTTP_PROXY']

if __name__ == "__main__":
    profile_options = {
        '1': 'driving-car',
        '2': 'foot-walking',
        '3': 'cycling-regular'
    }
    
    print("Выберите профиль:")
    for key, value in profile_options.items():
        print(f"{key}. {value}")

    profile_choice = input("Введите цифру, соответствующую профилю: ")
    profile = profile_options.get(profile_choice)
    if not profile:
        print("Неверный выбор профиля.")
        exit()

    proxy_list = [
        {"http": "http://TLV44n:PVj4q4@194.67.223.74:9346", "api_key": "5b3ce3597851110001cf62482c0997000b5d40f7ab497596cb1ec777"},
        # {"http": "http://TLV44n:PVj4q4@194.67.223.132:9878", "api_key": "5b3ce3597851110001cf6248ad28d11a7ae1445db5ec3be45d6ab0f4"},
        # {"http": "http://TLV44n:PVj4q4@194.67.221.21:9273", "api_key": "5b3ce3597851110001cf624827a2df637b8943859a9441cc7f22d691"},
    ]
    
    with ThreadPoolExecutor(max_workers=len(proxy_list)) as executor:
        params_files = list(executor.map(lambda proxy: create_params_file(proxy, profile), proxy_list))

    script_path = "create_matrix/main_part.py"
    input_file = "csv/all_points_test.csv"
    output_file = "csv/matrix_test.csv"
    type_arg = "matrix"
    start_index = 1  # начальный индекс

    with ThreadPoolExecutor(max_workers=len(proxy_list)) as executor:
        for params_file in params_files:
            executor.submit(
                execute_script_through_proxy, 
                script_path, input_file, output_file, params_file, type_arg, {"http": ""}, start_index
            )
            start_index += 1  # увеличиваем начальный индекс на start_index для следующего прокси