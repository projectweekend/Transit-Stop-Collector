import psycopg2
from urlparse import urlparse


def connect_to_psql(database_url):
	result = urlparse(database_url)
	connection = psycopg2.connect(
		database=result.path[1:],
		user=result.username,
		password=result.password,
		host=result.hostname
	)
	return connection, connection.cursor()
