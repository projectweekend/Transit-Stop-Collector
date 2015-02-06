CREATE TABLE IF NOT EXISTS nyc_mta_subway_stops (
    stop_id             char(50),
    stop_name           char(100),
    stop_lat            NUMERIC(14, 11),
    stop_lon            NUMERIC(14, 11),
    CONSTRAINT          nyc_mta_subway_stop_id_pk PRIMARY KEY(stop_id)
);


CREATE TABLE IF NOT EXISTS nyc_mta_subway_routes (
    route_id            char(50),
    route_short_name    char(100),
    route_long_name     char(250),
    route_type          integer,
    CONSTRAINT          nyc_mta_subway_route_id_pk PRIMARY KEY(route_id)
);


CREATE TABLE IF NOT EXISTS nyc_mta_subway_trips (
    trip_id             char(50),
    route_id            char(50),
    trip_headsign       char(50),
    CONSTRAINT          nyc_mta_subway_trip_id_pk PRIMARY KEY(trip_id),
    FOREIGN KEY         (route_id) REFERENCES nyc_mta_subway_routes (route_id)
);


CREATE TABLE IF NOT EXISTS nyc_mta_subway_stop_times (
    trip_id             char(50),
    stop_id             char(50),
    stop_sequence       integer,
    FOREIGN KEY         (trip_id) REFERENCES nyc_mta_subway_trips (trip_id),
    FOREIGN KEY         (stop_id) REFERENCES nyc_mta_subway_stops (stop_id)
);
