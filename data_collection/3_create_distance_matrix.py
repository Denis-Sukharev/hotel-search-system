import psycopg2
import requests
import pandas as pd
import random, time

def get_all_coordinates():
    conn=psycopg2.connect(
        host="localhost",
        database="osm",
        user="postgres",
        password="postgres")

    cursor=conn.cursor()
    cursor.execute('SELECT id, poi_id, latitude, longitude FROM poi_coordinates;')
    coordinates=cursor.fetchall()
    cursor.close()
    conn.close()

    return coordinates

def main():
    profile="car" # bike, foot ???
    all_coordinates=get_all_coordinates()
    distance_matrix=build_distance_matrix(profile, all_coordinates)
    df=pd.DataFrame(distance_matrix)

    df.to_csv(r'D:\\vkrb\\csv\\distance_matrix.csv', index=False,  header=False)
    print("УСПЕШНО")

def osrm_route_request(profile, coordinates):
    base_url="http://router.project-osrm.org/route/v1"
    endpoint=f"{profile}/{coordinates}"

    params={"annotations": "distance",}
    headers={"Authorization": "Bearer"}  

    response =requests.get(f"{base_url}/{endpoint}", params=params, headers=headers)
    result =response.json()

    if "routes" in result and result["routes"]:
        distance=result["routes"][0]["distance"]
        return distance
    else:
        return None

def build_distance_matrix(profile, coordinates):
    matrix_data ={}

    for coord_i in coordinates:
        matrix_data[coord_i[1]] ={}

        for coord_j in coordinates:
            coordinates_str =f"{coord_i[3]},{coord_i[2]};{coord_j[3]},{coord_j[2]}"
            distance = osrm_route_request(profile, coordinates_str)

            pause = random.uniform(1, 2)
            time.sleep(pause)
            
            matrix_data[coord_i[1]][coord_j[1]] = distance

    return matrix_data

if __name__ == "__main__":
    main()
    