SELECT          'dc-wmata' as system,
                trim(initcap(s.stop_name)) as name,
                s.stop_lat as latitude,
                s.stop_lon as longitude,
                trim(lower(r.route_id)) as route_id,
                trim(r.route_long_name) as route_name,
                'train' as route_type,
                'n/a' as route_direction
FROM            dc_wmata_routes as r
JOIN            dc_wmata_trips as t
                ON t.route_id = r.route_id
JOIN            dc_wmata_stop_times as st
                ON st.trip_id = t.trip_id
JOIN            dc_wmata_stops as s
                ON s.stop_id = st.stop_id
WHERE           r.route_type = 1
GROUP BY        s.stop_name,
                s.stop_lat,
                s.stop_lon,
                r.route_id

UNION

SELECT          'dc-wmata' as system,
                trim(initcap(s.stop_name)) as name,
                s.stop_lat as latitude,
                s.stop_lon as longitude,
                trim(lower(r.route_id)) as route_id,
                trim(COALESCE(r.route_long_name, r.route_short_name)) as route_name,
                'bus' as route_type,
                trim(initcap(t.trip_headsign)) as route_direction
FROM            dc_wmata_routes as r
JOIN            dc_wmata_trips as t
                ON t.route_id = r.route_id
JOIN            dc_wmata_stop_times as st
                ON st.trip_id = t.trip_id
JOIN            dc_wmata_stops as s
                ON s.stop_id = st.stop_id
WHERE           r.route_type = 3
GROUP BY        s.stop_id,
                r.route_id,
                t.trip_headsign
ORDER BY        route_type,
                route_id,
                name,
                route_direction
