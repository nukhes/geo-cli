import csv
import re
import folium
import math


def generate_map(input_file, title, id, zoom_start):
    map = folium.Map(location=[0, 0], zoom_start=zoom_start, tiles="CartoDB positron")
    map.get_root().html.add_child(folium.Element(f"<h1>{title}</h1>"))

    with open(input_file, mode="r") as f_in:
        reader = csv.DictReader(f_in)

        # determine if CSV has geographic or UTM coordinates and set search_for accordingly
        search_for = list()
        if "lat" in reader.fieldnames and "lon" in reader.fieldnames:
            search_for = ["lat", "lon"]
        elif "easting" in reader.fieldnames and "northing" in reader.fieldnames:
            search_for = ["easting", "northing"]
        else:
            raise ValueError(
                'O arquivo CSV deve conter as colunas "lat" e "lon" ou "easting" e "northing".'
            )

        # if there is no field id, we create one with the line number
        if id not in reader.fieldnames:
            for i, row in enumerate(reader):
                folium.Marker(
                    location=[row[search_for[0]], row[search_for[1]]], popup=i
                ).add_to(map)
        else:
            for row in reader:
                folium.Marker(
                    location=[row[search_for[0]], row[search_for[1]]], popup=row[id]
                ).add_to(map)

        map.save("mapa.html")


def convert_scale(scale, measure):
    try:
        scale_list = re.split(":", scale)

        if len(scale_list) != 2:
            raise ValueError("a escala deve estar no formato '1:1000'.")

        if int(scale_list[1]) == 0:
            raise ZeroDivisionError("o denominador da escala não pode ser zero.")

        key = int(scale_list[1]) / int(scale_list[0])
        return key * float(measure)
    except Exception as e:
        raise ValueError(f"erro ao converter a escala ({scale}): {e}")


def real_thickness(length, angle):
    theta = math.sin(math.radians(angle))
    print(theta)
    thickness = theta * length
    return thickness
