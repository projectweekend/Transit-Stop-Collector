import csv


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
	routes_columns = ['route_id', 'route_short_name', 'route_long_name', 'route_type']
	stops_columns = ['stop_id', 'stop_name', 'stop_lat', 'stop_lon']
	trips_columns = ['trip_id', 'route_id']
	stop_times_columns = ['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence']

	to_process = (
		('./gtfs/in/routes.txt', './gtfs/out/routes.txt', routes_columns,),
		('./gtfs/in/stops.txt', './gtfs/out/stops.txt', stops_columns,),
		('./gtfs/in/trips.txt', './gtfs/out/trips.txt', trips_columns,),
		('./gtfs/in/stop_times.txt', './gtfs/out/stop_times.txt', stop_times_columns,),
	)

	for item in to_process:
		process_gtfs_file(item[0], item[1], item[2])


if __name__ == '__main__':
	main()
