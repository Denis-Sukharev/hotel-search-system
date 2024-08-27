import openrouteservice
from .geo_point import GeoPoint
from typing import List, Union
import time


class ORSWrapper:
    def __init__(self, base_url: str = None,
                 api_key: str = None,
                 output_format: str = "geojson",
                 units: str = "m",
                 profile: str = "driving-car"):

        if api_key is None and base_url is None:
            raise Exception("Provide either <base_url> of local ORS instance or <api_key> to access the cloud API")

        self.units = units
        self.output_format = output_format
        self.profile = profile

        if base_url is None:
            self.local_instance = False
            self.client = openrouteservice.Client(key=api_key)

        if base_url is not None:
            self.local_instance = True
            self.client = openrouteservice.Client(key=api_key, base_url=base_url)

    def pair_directions(self, origin: GeoPoint, destination: GeoPoint):
        coords = ((origin.longitude, origin.latitude), (destination.longitude, destination.latitude))
        if not self.local_instance:
            time.sleep(2)
            directions = self.client.directions(coords,
                                                units=self.units,
                                                format=self.output_format,
                                                profile=self.profile)
        else:
            directions = self.client.request(url=f"/v2/directions/{self.profile}/{self.output_format}",
                                             post_json={'coordinates': coords,
                                                        'profile': self.profile,
                                                        'format': self.output_format,
                                                        'units': self.units},
                                             get_params={'profile': self.profile})
        return directions

    def distance_matrix(self, locations: List[GeoPoint], metrics: Union[List[str], str] = "all"):
        coordinates = [[location.longitude, location.latitude] for location in locations]

        if metrics == "all":
            metrics = ["distance", "duration"]

        if not self.local_instance:
            matrix = self.client.distance_matrix(coordinates,
                                                 units=self.units,
                                                 profile=self.profile,
                                                 metrics=metrics)
        else:
            matrix = self.client.request(url=f"/v2/matrix/{self.profile}",
                                         post_json={'locations': coordinates,
                                                    'profile': self.profile,
                                                    'metrics': metrics,
                                                    'units': self.units},
                                         get_params={'profile': self.profile},
                                         requests_kwargs={"timeout": 600})
        return matrix