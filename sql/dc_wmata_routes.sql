SELECT          'dc-wmata' as system,
                trim(lower(r.route_id)) as id,
                trim(r.route_long_name) as name,
                'train' as type,
                '' as directions
FROM            dc_wmata_routes as r
JOIN            dc_wmata_trips as t
                ON r.route_id = t.route_id
WHERE           r.route_type = 1
GROUP BY        r.route_id

UNION

SELECT          'dc-wmata' as system,
                trim(lower(r.route_id)) as id,
                trim(COALESCE(r.route_long_name, r.route_short_name)) as name,
                'bus' as type,
                string_agg(DISTINCT initcap(trim(t.trip_headsign)), ', ') as directions
FROM            dc_wmata_routes as r
JOIN            dc_wmata_trips as t
                ON r.route_id = t.route_id
WHERE           r.route_type = 3
GROUP BY        r.route_id
ORDER BY        type,
                id,
                directions
