SELECT          r.route_id,
                r.route_long_name as route_short_name,
                r.route_long_name,
                r.route_type,
                'N/A' as direction
FROM            chicago_cta_routes as r
JOIN            chicago_cta_trips as t
                ON r.route_id = t.route_id
WHERE           r.route_type = 1
GROUP BY        r.route_id,
                r.route_short_name,
                r.route_long_name,
                r.route_type

UNION

SELECT          r.route_id,
                r.route_short_name,
                r.route_long_name,
                r.route_type,
                t.direction
FROM            chicago_cta_routes as r
JOIN            chicago_cta_trips as t
                ON r.route_id = t.route_id
WHERE           r.route_type = 3
GROUP BY        r.route_id,
                r.route_short_name,
                r.route_long_name,
                r.route_type,
                t.direction
ORDER BY        route_type,
                route_id,
                direction
