import sys
import csv
import yaml


def strip_columns(row, columns_to_keep):
	for k in row.keys():
		if k not in columns_to_keep:
			del row[k]


def process_gtfs_file(input_file, output_file, columns_to_keep):
	with open( input_file, 'r' ) as in_file:
		with open(output_file, 'w+') as out_file:

			reader = csv.DictReader(in_file)
			writer = csv.DictWriter(out_file, fieldnames=columns_to_keep)

			writer.writeheader()

			for row in reader:
				strip_columns(row, columns_to_keep)
				writer.writerow(row)


def main():
	try:
		config_file = './config/{0}.yml'.format(sys.argv[1:][0])
	except IndexError:
		sys.exit("Job name is a required argument. Example: chicago_cta")

	try:
		with open(config_file, 'r') as file:
			config = yaml.safe_load(file)
	except IOError:
		sys.exit("Missing config file for job: '{0}'".format(config_file))


	try:
		to_process = (
			(
				'./gtfs/in/{0}'.format(config['routes']['file']),
				'./gtfs/out/{0}'.format(config['routes']['file']),
				config['routes']['columns'],
			),
			(
				'./gtfs/in/{0}'.format(config['stops']['file']),
				'./gtfs/out/{0}'.format(config['stops']['file']),
				config['stops']['columns'],
			),
			(
				'./gtfs/in/{0}'.format(config['trips']['file']),
				'./gtfs/out/{0}'.format(config['trips']['file']),
				config['trips']['columns'],
			),
			(
				'./gtfs/in/{0}'.format(config['stop_times']['file']),
				'./gtfs/out/{0}'.format(config['stop_times']['file']),
				config['stop_times']['columns'],
			),
		)
	except KeyError:
		sys.exit("Config file '{0}' is not formatted properly".format(config_file))

	for item in to_process:
		process_gtfs_file(item[0], item[1], item[2])


if __name__ == '__main__':
	main()
