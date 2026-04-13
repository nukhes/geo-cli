import csv
from pyproj import Transformer

class ProcessCsv:
	def __init__(self, f_input, f_output, epsg_source, epsg_target):
		self.f_input = f_input
		self.f_output = f_output
		self.epsg_source = epsg_source
		self.epsg_target = epsg_target
		self.transformer = Transformer.from_crs(epsg_source, epsg_target, always_xy=True)
		self.fields_in = []
		self.fields_out = []

	def run(self):
		if self.fields_in is None or self.fields_out is None:
			raise NotImplementedError("fields_in and fields_out must be defined in subclasses.")

		with open(self.f_input, mode='r', encoding='utf-8') as f_input, \
			open(self.f_output, mode='w', newline='', encoding='utf-8') as f_output:
			reader = csv.DictReader(f_input)

			output_fieldnames = [f for f in reader.fieldnames if f not in self.fields_in] + self.fields_out

			writer = csv.DictWriter(f_output, fieldnames=output_fieldnames, extrasaction='ignore')
			writer.writeheader()
			for row in reader:
				new_line = self.__trans(row)
				if new_line:
					writer.writerow(new_line)

	def __trans(self, row):
		row_copy = row.copy()
		output_x, output_y = self.transformer.transform(
			float(row_copy[self.fields_in[0]]),
			float(row_copy[self.fields_in[1]])
		)

		row_copy[self.fields_out[0]] = round(output_x, 3)
		row_copy[self.fields_out[1]] = round(output_y, 3)

		return row_copy

class GeoToUtm(ProcessCsv):
	def __init__(self, f_input, f_output, epsg_source='EPSG:4326', epsg_target='EPSG:31983'):
		super().__init__(f_input, f_output, epsg_source, epsg_target)
		self.fields_in = ['lon', 'lat']
		self.fields_out = ['easting', 'northing']

class UtmToGeo(ProcessCsv):
	def __init__(self, f_input, f_output, epsg_source='EPSG:31983', epsg_target='EPSG:4326'):
		super().__init__(f_input, f_output, epsg_source, epsg_target)
		self.fields_in = ['easting', 'northing']
		self.fields_out = ['lon', 'lat']
