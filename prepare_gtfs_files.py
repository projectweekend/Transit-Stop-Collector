import sys
import csv

from utils.config_utils import job_config


# GTFS files have inconsistent formatting, this cleans up the rows
def clean_up_row(row):
	clean_row = {}
	for k, v in row.iteritems():
		k = k.strip()
		if isinstance(v, str):
			v = v.strip()
		clean_row[k] = v
	return clean_row


def strip_columns(row, columns_to_keep):
	return {k: v for k, v in row.iteritems() if k in columns_to_keep}


def process_gtfs_file(input_file, output_file, columns_to_keep):
	with open( input_file, 'r' ) as in_file:
		with open(output_file, 'w+') as out_file:

			reader = csv.DictReader(in_file)
			writer = csv.DictWriter(out_file, fieldnames=columns_to_keep)

			writer.writeheader()

			for row in reader:
				clean_row = clean_up_row(row)
				stripped_row = strip_columns(clean_row, columns_to_keep)
				writer.writerow(stripped_row)


def main():
	config, _ = job_config(sys.argv[1:])

	for k in config['gtfs'].keys():
		in_file = './gtfs/in/{0}'.format(config['gtfs'][k]['file'])
		out_file = './gtfs/out/{0}'.format(config['gtfs'][k]['file'])
		columns_to_keep = config['gtfs'][k]['columns']

		process_gtfs_file(in_file, out_file, columns_to_keep)


if __name__ == '__main__':
	main()
