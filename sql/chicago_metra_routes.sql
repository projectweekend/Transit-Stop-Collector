SELECT          'chicago-metra' as system,
                trim(lower(r.route_id)) as id,
                trim(r.route_long_name) as name,
                'train' as type,
                '' as directions
FROM            chicago_metra_routes as r
JOIN            chicago_metra_trips as t
                ON r.route_id = t.route_id
GROUP BY        r.route_id
ORDER BY        type,
                id,
                directions
