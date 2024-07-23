
import os
import requests
import folium
import random
import warnings

warnings.filterwarnings("ignore")

def get_route(start_coords, end_coords, profile):
    api_key = "5b3ce3597851110001cf6248cd705541dbc34c099699bd5fc04bcf64"
    url = f"https://api.openrouteservice.org/v2/directions/{profile}?api_key={api_key}&start={start_coords[1]},{start_coords[0]}&end={end_coords[1]},{end_coords[0]}"
    response = requests.get(url)
    data = response.json()
    if 'features' in data:
        route = data['features'][0]
        geometry = route['geometry']['coordinates']
        return geometry

profile_options = {
    '1': 'driving-car',
    '2': 'foot-walking',
    '3': 'cycling-regular'
}

print("Выберите профиль:")
for key, value in profile_options.items():
    print(f"{key}. {value}")

profile_choice = input("Введите цифру, соответствующую раннее использованному профилю: ")
profile = profile_options.get(profile_choice)
if not profile:
    print("Неверный выбор профиля.")
    exit()

points_folder = 'best_routes'
for file_name in os.listdir(points_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(points_folder, file_name)
        with open(file_path, 'r') as f:
            points = [tuple(map(float, line.strip()[1:-1].split(','))) for line in f]

        m = folium.Map(location=[points[0][0], points[0][1]], zoom_start=13)

        # точки
        for i, point in enumerate(points[:-1]):
            popup_text = f"Точка {i+1}"
            color = 'green' if i == 0 else 'orange'
            if i != 0 and point != points[0]:  # пропуск нумерации начальной точки, если она встречается не в начале
                folium.Marker(location=[point[0], point[1]], icon=folium.DivIcon(html=f"<div style='background-color: {color}; border-radius: 50%; width: 20px; height: 20px; display: flex; justify-content: center; align-items: center;'><div style='font-size: 12pt; color: black;'>{i+1}</div></div>")).add_to(m)
            else:
                folium.Marker(location=[point[0], point[1]], icon=folium.Icon(color='green')).add_to(m)

        # маршрут
        route_colors = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(len(points)-1)]
        for i in range(len(points)-1):
            route_geometry = get_route(points[i], points[i+1], profile)
            if route_geometry:
                folium.PolyLine(locations=[(coord[1], coord[0]) for coord in route_geometry], color=route_colors[i]).add_to(m)

        m.save(f"routes/{os.path.splitext(file_name)[0]}.html")
