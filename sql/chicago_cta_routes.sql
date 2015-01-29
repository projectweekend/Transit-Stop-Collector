SELECT          'chicago-cta' as system,
                trim(lower(r.route_id)) as id,
                trim(r.route_long_name) as name,
                'train' as type,
                '' as directions
FROM            chicago_cta_routes as r
JOIN            chicago_cta_trips as t
                ON r.route_id = t.route_id
WHERE           r.route_type = 1
GROUP BY        r.route_id

UNION

SELECT          'chicago-cta' as system,
                trim(lower(r.route_id)) as id,
                trim(r.route_long_name) as name,
                'bus' as type,
                string_agg(DISTINCT lower(trim(t.direction)), ', ') as directions
FROM            chicago_cta_routes as r
JOIN            chicago_cta_trips as t
                ON r.route_id = t.route_id
WHERE           r.route_type = 3
GROUP BY        r.route_id
ORDER BY        type,
                id,
                directions
