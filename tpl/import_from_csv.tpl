COPY {1}_routes FROM '{0}/{1}_routes.txt' DELIMITER ',' QUOTE '"' HEADER CSV;
COPY {1}_stops FROM '{0}/{1}_stops.txt' DELIMITER ',' QUOTE '"' HEADER CSV;
COPY {1}_trips FROM '{0}/{1}_trips.txt' DELIMITER ',' QUOTE '"' HEADER CSV;
COPY {1}_stop_times FROM '{0}/{1}_stop_times.txt' DELIMITER ',' QUOTE '"' HEADER CSV;
