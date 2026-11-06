USE ev_intelligence;

CREATE OR REPLACE VIEW vw_charging_power_analysis AS
SELECT
    Power_Category,
    COUNT(*) AS total_stations,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM ev_charging_stations),
        2
    ) AS station_share_percent,
    ROUND(AVG(max_power_kw), 2) AS average_power_kw,
    MAX(max_power_kw) AS maximum_power_kw
FROM ev_charging_stations
GROUP BY Power_Category;

SELECT *
FROM vw_charging_power_analysis
ORDER BY average_power_kw;