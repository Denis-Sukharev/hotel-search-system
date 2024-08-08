import os
import pandas as pd
import re

def replace_poi_ids_with_coordinates(file_path, points_data):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(file_path, 'w', encoding='utf-8') as f:
        prev_line = None
        for line in lines:
            line = line.strip()
            if line:
                if '(' in line and ')' in line:
                    coordinates = re.findall(r"\(([^)]+)\)", line)[0]
                    latitude, longitude = coordinates.split(',')
                    f.write(f"({latitude},{longitude})\n")
                else:
                    poi_id = int(line)
                    if poi_id in points_data.index:
                        latitude = points_data.loc[poi_id, 'latitude']
                        longitude = points_data.loc[poi_id, 'longitude']
                        current_line = f"({latitude},{longitude})\n"
                        if current_line != prev_line:
                            f.write(current_line)
                        prev_line = current_line

if __name__ == "__main__":
    points_data = pd.read_csv('D:\\Project\\csv\\all_points.csv', index_col='poi_id')

    folder_path = 'best_routes'
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            replace_poi_ids_with_coordinates(file_path, points_data)
