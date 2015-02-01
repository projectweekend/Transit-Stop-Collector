SELECT          'chicago-metra' as system,
                trim(s.stop_name) as name,
                s.stop_lat as latitude,
                s.stop_lon as longitude,
                trim(lower(r.route_id)) as route_id,
                trim(r.route_long_name) as route_name,
                'train' as route_type,
                'n/a' as route_direction
FROM            chicago_metra_routes as r
JOIN            chicago_metra_trips as t
                ON t.route_id = r.route_id
JOIN            chicago_metra_stop_times as st
                ON st.trip_id = t.trip_id
JOIN            chicago_metra_stops as s
                ON s.stop_id = st.stop_id
GROUP BY        s.stop_name,
                s.stop_lat,
                s.stop_lon,
                r.route_id
