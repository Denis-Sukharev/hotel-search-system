from pathlib import Path
import argparse
from typing import List
from directions_routes.geo_point import GeoPoint, read_points_from_file
import yaml
from directions_routes.orswrapper import ORSWrapper
import pandas as pd
import time
import sys
import random

request_count = 0 # переменная для отслеживания количества запросов

def distance_matrix_for_point_pairs(points: List[GeoPoint], computer: ORSWrapper, output_file: str = None) -> pd.DataFrame:
    global request_count

    result = []
    
    for origin in points:
        for destination in points:
            if points.index(origin) < points.index(destination):
                try:
                    matrix = computer.distance_matrix(locations=[origin, destination])
                except Exception as e:
                    print("Превышено ограничение. Повторная отправка запросов через 24 часа")
                    time.sleep(24*60*60+1)
                    continue

                request_count += 1

                if request_count > 5000:
                    print(f"Превышено максимальное количество запросов прокси {params_file}. Процесс остановлен")
                    sys.exit()

                durations = matrix.get("durations")
                distances = matrix.get("distances")

                origin_id = origin.poi_id
                destination_id = destination.poi_id
                duration = durations[0][1]
                distance = distances[0][1]

                result.append({"mapped_object_start": origin_id,
                               "mapped_object_finish": destination_id,
                               "duration": duration,
                               "distance": distance})

                if output_file:
                    with open(output_file, 'a') as f:
                        f.write(f"{origin_id},{destination_id},{duration},{distance}\n")
                    time.sleep(random.uniform(1, 3))

    return pd.DataFrame(result)

def compute_routes_for_point_pairs(points: List[GeoPoint],
                                   target_name: str,
                                   ors_params: dict,
                                   output_file: str = None) -> pd.DataFrame:
    ors_computer = ORSWrapper(**ors_params)

    results = []

    for origin in points:
        for destination in points:
            if origin != destination:
                if target_name == "matrix":
                    result = distance_matrix_for_point_pairs([origin, destination], ors_computer, output_file)
                    results.append(result)
                else:
                    raise Exception(f"Unsupported target: {target_name}")

    if results:
        final_result = pd.concat(results, ignore_index=True)
        return final_result
    else:
        return pd.DataFrame()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, action='store', required=True,
                        help='Path to the input file')
    parser.add_argument('-o', '--output', type=str, action='store', required=True,
                        help='Path to the output file')
    parser.add_argument('-p', '--params-file', type=str, action='store', required=True,
                        help='Path to the file with parameters')
    parser.add_argument('-t', '--target-name', type=str, action='store', required=True,
                        help='Path to the file with parameters', choices=['matrix'])
    parser.add_argument('-s', '--start-index', type=int, action='store', default=1,
                        help='Starting index for data collection')
    cmd_args = parser.parse_args()

    input_file = Path(cmd_args.input)
    if not input_file.exists():
        raise Exception(f"Can not find input path: {input_file}")

    params_file = Path(cmd_args.params_file)
    with open(params_file, "r") as f:
        params = yaml.load(f, Loader=yaml.FullLoader)

    output_file = Path(cmd_args.output)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    points = read_points_from_file(input_file)

    points = points[cmd_args.start_index - 1:]

    result = compute_routes_for_point_pairs(points=points,
                                            target_name=cmd_args.target_name,
                                            ors_params=params,
                                            output_file=output_file)
    result.to_csv(output_file, index=False)
