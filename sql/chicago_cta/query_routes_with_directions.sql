SELECT          'chicago-cta' as system,
                r.route_id as id,
                r.route_long_name as name,
                'train' as type,
                'n/a' as directions
FROM            chicago_cta_routes as r
JOIN            chicago_cta_trips as t
                ON r.route_id = t.route_id
WHERE           r.route_type = 1
GROUP BY        r.route_id

UNION

SELECT          'chicago-cta' as system,
                r.route_id as id,
                r.route_long_name as name,
                'bus' as type,
                string_agg(DISTINCT lower(t.direction), ', ') as directions
FROM            chicago_cta_routes as r
JOIN            chicago_cta_trips as t
                ON r.route_id = t.route_id
WHERE           r.route_type = 3
GROUP BY        r.route_id
ORDER BY        type,
                id,
                directions
