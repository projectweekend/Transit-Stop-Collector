import sys
import csv

from utils.config_utils import job_config


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
	config, config_file = job_config(sys.argv[1:])

	try:
		to_process = (
			(
				'./gtfs/in/{0}'.format(config['gtfs']['routes']['file']),
				'./gtfs/out/{0}'.format(config['gtfs']['routes']['file']),
				config['gtfs']['routes']['columns'],
			),
			(
				'./gtfs/in/{0}'.format(config['gtfs']['stops']['file']),
				'./gtfs/out/{0}'.format(config['gtfs']['stops']['file']),
				config['gtfs']['stops']['columns'],
			),
			(
				'./gtfs/in/{0}'.format(config['gtfs']['trips']['file']),
				'./gtfs/out/{0}'.format(config['gtfs']['trips']['file']),
				config['gtfs']['trips']['columns'],
			),
			(
				'./gtfs/in/{0}'.format(config['gtfs']['stop_times']['file']),
				'./gtfs/out/{0}'.format(config['gtfs']['stop_times']['file']),
				config['gtfs']['stop_times']['columns'],
			),
		)
	except KeyError:
		sys.exit("Config file '{0}' is not formatted properly".format(config_file))

	for item in to_process:
		process_gtfs_file(item[0], item[1], item[2])


if __name__ == '__main__':
	main()
