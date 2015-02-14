import sys
import csv
import psycopg2

from utils.psql_utils import connect_to_psql
from utils.config_utils import main_config
from utils.config_utils import job_config


def load_query(file_name):
    with open('./sql/{0}'.format(file_name), 'r') as file:
        return file.read()


def main():
    main, _ = main_config(sys.argv[1:])
    job, _ = job_config(sys.argv[1:])

    conn, cursor = connect_to_psql(main['database_url'])

    query = load_query(job['sql']['train_export'])

    try:
        cursor.execute(query)
    except psycopg2.ProgrammingError:
        sys.exit("SQL error in query: {0}".format(job['sql']['train_export']))

    output_file = './export/{0}'.format(job['export']['train'])

    with open(output_file, 'w+') as file:
        writer = csv.writer(file)

        writer.writerow(tuple(d[0] for d in cursor.description))

        for row in cursor:
            writer.writerow(row)


if __name__ == '__main__':
    main()
