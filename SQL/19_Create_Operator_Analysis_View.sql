USE ev_intelligence;

CREATE OR REPLACE VIEW vw_operator_analysis AS
SELECT
    operator,
    COUNT(*) AS total_stations,
    SUM(total_chargers) AS total_chargers,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM ev_charging_stations),
        2
    ) AS station_market_share_percent
FROM ev_charging_stations
GROUP BY operator;

SELECT *
FROM vw_operator_analysis
ORDER BY total_stations DESC;