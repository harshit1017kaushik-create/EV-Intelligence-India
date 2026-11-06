USE ev_intelligence;

CREATE OR REPLACE VIEW vw_state_ev_infrastructure AS

SELECT
    r.state,
    r.ev_registrations,
    COUNT(c.id) AS total_stations,

    SUM(CASE
        WHEN c.geo_validated = 1 THEN 1
        ELSE 0
    END) AS validated_stations,

    SUM(CASE
        WHEN c.geo_validated = 0 THEN 1
        ELSE 0
    END) AS suspect_stations,

    COALESCE(SUM(c.total_chargers), 0) AS total_chargers,
    COALESCE(SUM(c.total_connectors), 0) AS total_connectors,

    ROUND(
        r.ev_registrations /
        NULLIF(SUM(c.total_chargers), 0),
        2
    ) AS evs_per_charger

FROM ev_registrations_statewise r

LEFT JOIN ev_charging_stations c
    ON (
        LOWER(TRIM(r.state)) = LOWER(TRIM(c.state))
        OR (
            r.state = 'Andaman & Nicobar Island'
            AND c.state = 'Andaman and Nicobar Islands'
        )
        OR (
            r.state = 'UT of DNH and DD'
            AND c.state = 'Dadra and Nagar Haveli and Daman and Diu'
        )
    )

GROUP BY
    r.state,
    r.ev_registrations;
    
    SELECT *
FROM vw_state_ev_infrastructure
ORDER BY ev_registrations DESC;