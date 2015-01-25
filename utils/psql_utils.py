import os
import psycopg2
from urlparse import urlparse


DATABASE_URL = os.getenv('DATABASE_URL', None)
assert(DATABASE_URL)

result = urlparse(DATABASE_URL)


def connect_to_psql():
	connection = psycopg2.connect(
		database=result.path[1:],
		user=result.username,
		password=result.password,
		host=result.hostname
	)
	return connection, connection.cursor()
