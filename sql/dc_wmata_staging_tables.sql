CREATE TABLE IF NOT EXISTS dc_wmata_stops (
    stop_id             char(50),
    stop_name           char(100),
    stop_lat            NUMERIC(14, 11),
    stop_lon            NUMERIC(14, 11),
    CONSTRAINT          dc_wmata_stop_id_pk PRIMARY KEY(stop_id)
);


CREATE TABLE IF NOT EXISTS dc_wmata_routes (
    route_id            char(50),
    route_short_name    char(100),
    route_long_name     char(250),
    route_type          integer,
    CONSTRAINT          dc_wmata_route_id_pk PRIMARY KEY(route_id)
);


CREATE TABLE IF NOT EXISTS dc_wmata_trips (
    trip_id             char(50),
    route_id            char(50),
    trip_headsign       char(75),
    direction_id        integer,
    CONSTRAINT          dc_wmata_trip_id_pk PRIMARY KEY(trip_id),
    FOREIGN KEY         (route_id) REFERENCES dc_wmata_routes (route_id)
);


CREATE TABLE IF NOT EXISTS dc_wmata_stop_times (
    trip_id             char(50),
    stop_id             char(50),
    stop_sequence       integer,
    FOREIGN KEY         (trip_id) REFERENCES dc_wmata_trips (trip_id),
    FOREIGN KEY         (stop_id) REFERENCES dc_wmata_stops (stop_id)
);
