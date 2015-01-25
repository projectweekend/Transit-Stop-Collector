COPY routes FROM '{0}/routes.txt' DELIMITER ',' QUOTE '"' HEADER CSV;
COPY stops FROM '{0}/stops.txt' DELIMITER ',' QUOTE '"' HEADER CSV;
COPY trips FROM '{0}/trips.txt' DELIMITER ',' QUOTE '"' HEADER CSV;
COPY stop_times FROM '{0}/stop_times.txt' DELIMITER ',' QUOTE '"' HEADER CSV;
