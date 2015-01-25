import os
import psycopg2
from urlparse import urlparse


DATABASE_URL = os.getenv('DATABASE_URL', None)
assert(DATABASE_URL)

result = urlparse(DATABASE_URL)

connection = psycopg2.connect(
	database=result.path[1:],
	user=result.username,
	password=result.password,
	host=result.hostname
)

def connect_to_database():
	connection = psycopg2.connect(
		database=result.path[1:],
		user=result.username,
		password=result.password,
		host=result.hostname
	)
	return connection, connection.cursor()


def import_query(template, csv_path):
	with open(template, 'r') as file:
		data = file.read()
	return data.format(csv_path)


def main():
	gtfs_dir = '{0}/gtfs/out'.format(os.getcwd())
	query = import_query('./tpl/import_from_csv.tpl', gtfs_dir)

	conn, cursor = connect_to_database()

	cursor.execute(query)
	conn.commit()


if __name__ == '__main__':
	main()
