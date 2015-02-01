import os
import sys
import psycopg2

from utils.psql_utils import connect_to_psql
from utils.config_utils import main_config


def import_query(template, csv_path, file_prefix):
	with open(template, 'r') as file:
		data = file.read()
	return data.format(csv_path, file_prefix)


def main():
	config, _ = main_config(sys.argv[1:])

	try:
		file_prefix = sys.argv[1:][1]
	except IndexError:
		sys.exit("Job name is a required argument. Example: chicago_cta")

	gtfs_dir = '{0}/gtfs/out'.format(os.getcwd())
	query = import_query('./tpl/import_from_csv.tpl', gtfs_dir, file_prefix)

	conn, cursor = connect_to_psql(config['database_url'])

	try:
		cursor.execute(query)
	except psycopg2.ProgrammingError:
		sys.exit("Invalid job name, tables matching '{0}' prefix do not exist".format(file_prefix))

	conn.commit()


if __name__ == '__main__':
	main()
