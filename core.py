import csv
from pyproj import Transformer

class ProcessCsv:
	def __init__(self, f_input, f_output, epsg_source, epsg_target):
		self.input = f_input # the input CSV file path
		self.output = f_output # the output CSV file path
		self.epsg_source = epsg_source # the source coordinate system
		self.epsg_target = epsg_target # the target coordinate system
		self.transformer = Transformer.from_crs(epsg_source, epsg_target, always_xy=True) # initializes the coordinate transformer
		
		# open file and assign fieldnames to self.input_fieldnames
		# this is necessary to replace self.output_fieldnames in child classes
		with open(self.input, 'r') as f:
			reader = csv.DictReader(f)
			self.input_fieldnames = reader.fieldnames

	def process(self):
		'''
		for each row in the input file apply a transformation by calling self.trans()
		'''

		# based in self.replace_map we determine the output fieldnames in
		self.output_fieldnames = [self.replace_map.get(col, col) for col in self.input_fieldnames]

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
		'''
		transforms a row by applying the coordinate transformation and returns the new row with the transformed coordinates
		'''
		old_system = list(self.replace_map.keys())
		new_system = list(self.replace_map.values())

		x, y = self.transformer.transform(float(row[old_system[0]]), float(row[old_system[1]]))

		row[new_system[0]] = round(x, 3)
		row[new_system[1]] = round(y, 3)
		del row[old_system[0]]
		del row[old_system[1]]
		return row

class GeoToUtm(ProcessCsv):
	def __init__(self, f_input, f_output, epsg_source='EPSG:4326', epsg_target='EPSG:31983'):
		super().__init__(f_input, f_output, epsg_source, epsg_target)
		self.replace_map = {'lon': 'easting', 'lat': 'northing'}

class UtmToGeo(ProcessCsv):
	def __init__(self, f_input, f_output, epsg_source='EPSG:31983', epsg_target='EPSG:4326'):
		super().__init__(f_input, f_output, epsg_source, epsg_target)
		self.replace_map = {'easting': 'lon', 'northing': 'lat'}
