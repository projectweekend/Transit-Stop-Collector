import os
import sys
import yaml

from utils.psql_utils import connect_to_psql
from utils.mongo_utils import connect_to_mongo
from utils.config_utils import job_config


DATABASE_NAME = os.getenv('DATABASE_NAME', None)
assert(DATABASE_NAME)


psql_conn, psql_cursor = connect_to_psql()
mongo_conn = connect_to_mongo()

db = mongo_conn[DATABASE_NAME]


def load_query_from_file(file):
	with open('./sql/{0}'.format(file), 'r') as f:
		query = f.read()
	return query


def route_documents(cursor):
	for r in cursor:
		document = {
			'system': r[0],
			'id': r[1],
			'name': r[2],
			'type': r[3],
			'directions': [d.strip() for d in r[4].split(',') if d],
			'urls': {
				'all_stops': '/{0}/{1}/{2}'.format(r[0], r[3], r[1])
			}
		}
		for d in document['directions']:
			document['urls']['{0}_stops'.format(d)] = '/{0}/{1}/{2}/{3}'.format(r[0], r[3], r[1], d)
		yield document


def stop_documents(cursor):
	for r in cursor:
		document = {
			'system': r[0],
			'name': r[1],
			'latitude': float(r[2]),
			'longitude': float(r[3]),
			'route_id': r[4],
			'route_name': r[5],
			'route_type': r[6],
			'route_direction': r[7]
		}
		yield document


def populate_systems(config):
	print('Populating transit_systems...')
	db.transit_systems.remove({
		'system': config['system']['code']
	})
	db.transit_systems.insert({
		'system': config['system']['code'],
		'name': config['system']['name'],
		'urls': {
			'routes': '/{0}'.format(config['system']['code'])
		}
	})


def populate_routes(config):
	print('Populating transit_routes...')
	query = load_query_from_file(config['sql']['routes_query'])
	psql_cursor.execute(query)

	db.transit_routes.remove({
		'system': config['system']['code']
	})
	db.transit_routes.insert(route_documents(psql_cursor))


def populate_stops(config):
	print('Populating transit_stops...')
	query = load_query_from_file(config['sql']['stops_query'])
	psql_cursor.execute(query)

	db.transit_stops.remove({
		'system': config['system']['code']
	})
	db.transit_stops.insert(stop_documents(psql_cursor))


def main():
	config, _ = job_config(sys.argv[1:])

	populate_systems(config)
	populate_routes(config)
	# populate_stops(config)


if __name__ == '__main__':
	main()
