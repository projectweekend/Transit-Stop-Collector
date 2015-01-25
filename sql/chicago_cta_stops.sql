SELECT          'chicago-cta' as system,
                trim(s.stop_name) as name,
                s.stop_lat as latitude,
                s.stop_lon as longitude,
                trim(r.route_id) as route_id,
                trim(r.route_long_name) as route_name,
                'train' as route_type,
                'n/a' as route_direction
FROM            chicago_cta_routes as r
JOIN            chicago_cta_trips as t
                ON t.route_id = r.route_id
JOIN            chicago_cta_stop_times as st
                ON st.trip_id = t.trip_id
JOIN            chicago_cta_stops as s
                ON s.stop_id = st.stop_id
WHERE           r.route_type = 1
GROUP BY        s.stop_name,
                s.stop_lat,
                s.stop_lon,
                r.route_id

UNION

SELECT          'chicago-cta' as system,
                trim(s.stop_name) as name,
                s.stop_lat as latitude,
                s.stop_lon as longitude,
                trim(r.route_id) as route_id,
                trim(r.route_long_name) as route_name,
                'bus' as route_type,
                trim(lower(t.direction)) as route_direction
FROM            chicago_cta_routes as r
JOIN            chicago_cta_trips as t
                ON t.route_id = r.route_id
JOIN            chicago_cta_stop_times as st
                ON st.trip_id = t.trip_id
JOIN            chicago_cta_stops as s
                ON s.stop_id = st.stop_id
WHERE           r.route_type = 3
GROUP BY        s.stop_id,
                r.route_id,
                t.direction
ORDER BY        route_type,
                route_id,
                name,
                route_direction
