import os
import sys
import yaml

from utils.psql_utils import connect_to_psql
from utils.mongo_utils import connect_to_mongo


DATABASE_NAME = os.getenv('DATABASE_NAME', None)
assert(DATABASE_NAME)


psql_conn, psql_cursor = connect_to_psql()
mongo_conn = connect_to_mongo()

db = mongo_conn[DATABASE_NAME]


def load_query_from_file(file):
	with open('./sql/{0}'.format(file), 'r') as f:
		query = f.read()
	return query


def populate_routes(routes_query):
	query = load_query_from_file(routes_query)
	psql_cursor.execute(query)

	db.transit_routes.remove()
	db.transit_routes.insert(({
		'system': r[0],
		'id': r[1],
		'name': r[2],
		'type': r[3],
		'directions': r[4].split()
	} for r in psql_cursor))


def populate_stops(stops_query):
	query = load_query_from_file(stops_query)
	psql_cursor.execute(query)

	db.transit_stops.remove()
	db.transit_stops.insert(({
		'system': r[0],
		'name': r[1],
		'latitude': float(r[2]),
		'longitude': float(r[3]),
		'route_id': r[4],
		'route_name': r[5],
		'route_type': r[6],
		'route_direction': r[7]
	} for r in psql_cursor))


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

	populate_routes(config['sql']['routes_query'])
	populate_stops(config['sql']['stops_query'])


if __name__ == '__main__':
	main()
