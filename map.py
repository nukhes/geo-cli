import csv
import folium

def generate_map(input_file, zoom_start=2):
  map = folium.Map(location=[0, 0], zoom_start=zoom_start)
  

  with open(input_file, mode='r') as f_in:
    reader = csv.DictReader(f_in)

    # determine if CSV has geographic or UTM coordinates and set search_for accordingly
    search_for = list()
    if 'lat' in reader.fieldnames and 'lon' in reader.fieldnames:
      search_for = ['lat', 'lon']
    elif 'easting' in reader.fieldnames and 'northing' in reader.fieldnames:
      search_for = ['easting', 'northing']
    else:
      raise ValueError('O arquivo CSV deve conter as colunas "lat" e "lon" ou "easting" e "northing".')

    # if there is no field id, we create one with the line number
    if 'id' not in reader.fieldnames:
      for i, row in enumerate(reader):
        folium.Marker(location=[row[search_for[0]], row[search_for[1]]], popup=i).add_to(map)
    else:
      for row in reader:
        folium.Marker(location=[row[search_for[0]], row[search_for[1]]], popup=row['id']).add_to(map)

  map.save('map.html')