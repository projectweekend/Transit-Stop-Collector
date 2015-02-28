SELECT          trim(s.stop_name) as name,
                trim(lower(r.route_id)) as route_id,
                trim(r.route_long_name) as route_name,
                0 as order
FROM            chicago_metra_routes as r
JOIN            chicago_metra_trips as t
                ON t.route_id = r.route_id
JOIN            chicago_metra_stop_times as st
                ON st.trip_id = t.trip_id
JOIN            chicago_metra_stops as s
                ON s.stop_id = st.stop_id
GROUP BY        s.stop_name,
                r.route_id
ORDER BY        route_name,
                name
