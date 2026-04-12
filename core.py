import csv
from pyproj import Transformer

class ProcessCsv:
		def __init__(self, f_input, f_output, epsg_source, epsg_target):
				self.input = f_input
				self.output = f_output
				self.epsg_source = epsg_source
				self.epsg_target = epsg_target
				self.transformer = Transformer.from_crs(epsg_source, epsg_target, always_xy=True)
				with open(self.input, 'r') as f:
						reader = csv.DictReader(f)
						self.input_fieldnames = reader.fieldnames

		def process(self):
				with open(self.input, mode='r') as f_in, \
				open(self.output, mode='w', newline='', encoding='utf-8') as f_out:
						reader = csv.DictReader(f_in)
						writer = csv.DictWriter(f_out, fieldnames=self.output_fieldnames, extrasaction='ignore')
						writer.writeheader()
						for row in reader:
								new_line = self.trans(row)
								if new_line:
										writer.writerow(new_line)

		def trans(self, row):
				raise NotImplementedError('you should implement this first')

class GeoToUtm(ProcessCsv):
		def __init__(self, f_input, f_output, epsg_source='EPSG:4326', epsg_target='EPSG:31983'):
				super().__init__(f_input, f_output, epsg_source, epsg_target)
				self.replace_map = {'lon': 'easting', 'lat': 'northing'}
				self.output_fieldnames = [self.replace_map.get(col, col) for col in self.input_fieldnames]

		def trans(self, row):
				print(f'processando linha: {row}')
				lon = float(row['lon'])
				lat = float(row['lat'])

				easting, northing = self.transformer.transform(lon, lat)

				row['easting'] = round(easting, 3)
				row['northing'] = round(northing, 3)
				del row['lat']
				del row['lon']
				return row

class UtmToGeo(ProcessCsv):
		def __init__(self, f_input, f_output, epsg_source='EPSG:31983', epsg_target='EPSG:4326'):
				super().__init__(f_input, f_output, epsg_source, epsg_target)
				self.replace_map = {'easting': 'lon', 'northing': 'lat'}
				self.output_fieldnames = [self.replace_map.get(col, col) for col in self.input_fieldnames]

		def trans(self, row):
				easting = float(row['easting'])
				northing = float(row['northing'])

				lon, lat = self.transformer.transform(easting, northing)

				row['lon'] = round(lon, 3)
				row['lat'] = round(lat, 3)
				del row['easting']
				del row['northing']
				return row