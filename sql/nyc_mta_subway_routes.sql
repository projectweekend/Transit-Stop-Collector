SELECT          'nyc-mta-subway' as system,
                trim(lower(r.route_id)) as id,
                trim(r.route_short_name) as name,
                'train' as type,
                '' as directions
FROM            nyc_mta_subway_routes as r
GROUP BY        r.route_id
ORDER BY        type,
                id,
                directions
