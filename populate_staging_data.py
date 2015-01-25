import os
import sys

from utils.psql_utils import connect_to_psql


def import_query(template, csv_path, file_prefix):
	with open(template, 'r') as file:
		data = file.read()
	return data.format(csv_path, file_prefix)


def main():
	try:
		file_prefix = sys.argv[1:][0]
	except IndexError:
		sys.exit("Job name is a required argument. Example: chicago_cta")

	gtfs_dir = '{0}/gtfs/out'.format(os.getcwd())
	query = import_query('./tpl/import_from_csv.tpl', gtfs_dir, file_prefix)

	conn, cursor = connect_to_psql()
	cursor.execute(query)
	conn.commit()


if __name__ == '__main__':
	main()
