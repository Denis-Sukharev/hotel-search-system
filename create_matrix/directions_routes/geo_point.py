from pathlib import Path, PosixPath
from dataclasses import dataclass
from typing import Union, List

import pandas as pd

@dataclass
class GeoPoint:
    """Class for keeping geo points in order"""
    poi_id: Union[int, str]
    name: Union[int, str]
    latitude: float
    longitude: float

def read_points_from_file(filename: Union[PosixPath, Path]) -> List[GeoPoint]:
    """
    Reads coordinates of the points from the given files and returns as list of GeoPoints objects.
    :param filename: name of the file to read from.
    :type filename:
    :return:
    :rtype:
    """
    df_mapped_objects = pd.read_csv(filename)

    points = []
    for mapped_object in df_mapped_objects.to_dict("records"):
        if 'district_id' in mapped_object:
            del mapped_object['district_id']
        points.append(GeoPoint(**mapped_object))
    return points