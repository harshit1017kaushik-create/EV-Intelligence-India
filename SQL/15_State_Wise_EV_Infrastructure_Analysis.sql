CREATE DATABASE IF NOT EXISTS ev_intelligence;

USE ev_intelligence;

SELECT DATABASE();

SHOW TABLES;

USE ev_intelligence;

-- 1. Annual registrations
CREATE TABLE ev_registrations_annual (
    year INT PRIMARY KEY,
    ev_registrations BIGINT NOT NULL,
    year_status VARCHAR(30),
    yoy_growth_percent DECIMAL(10,2)
);

-- 2. Statewise registrations
CREATE TABLE ev_registrations_statewise (
    state VARCHAR(100) PRIMARY KEY,
    ev_registrations BIGINT NOT NULL,
    registration_share_percent DECIMAL(10,6),
    registration_rank INT
);

-- 3. Monthly registrations
CREATE TABLE ev_registrations_monthly (
    month DATE PRIMARY KEY,
    ev_registrations BIGINT NOT NULL,
    year INT,
    mom_growth_percent DECIMAL(10,2)
);


USE ev_intelligence;

CREATE TABLE ev_charging_stations (
    id VARCHAR(50) PRIMARY KEY,
    operator VARCHAR(150),
    ownership VARCHAR(100),
    state VARCHAR(100),
    state_code VARCHAR(20),
    district VARCHAR(150),
    city VARCHAR(150),
    address TEXT,
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    location_quality VARCHAR(30),
    mixed_admin BOOLEAN,
    total_chargers INT,
    total_connectors INT,
    max_power_kw DECIMAL(10,2),
    Power_Category VARCHAR(30),
    geo_validated BOOLEAN,
    geo_validation_reason VARCHAR(255)
);

SHOW TABLES;

USE ev_intelligence;

SELECT
    DATABASE() AS database_name,
    @@hostname AS hostname,
    @@port AS port,
    CURRENT_USER() AS mysql_user;

SELECT COUNT(*) AS existing_records
FROM ev_charging_stations;

SELECT *
FROM ev_charging_stations
LIMIT 5;

USE ev_intelligence;

SELECT 'ev_charging_stations' AS table_name, COUNT(*) AS total_records
FROM ev_charging_stations

UNION ALL

SELECT 'ev_registrations_annual', COUNT(*)
FROM ev_registrations_annual

UNION ALL

SELECT 'ev_registrations_statewise', COUNT(*)
FROM ev_registrations_statewise

UNION ALL

SELECT 'ev_registrations_monthly', COUNT(*)
FROM ev_registrations_monthly;

SELECT *
FROM ev_registrations_annual
ORDER BY year;

SELECT *
FROM ev_registrations_monthly
ORDER BY month;

USE ev_intelligence;

INSERT INTO ev_registrations_annual
(year, ev_registrations, year_status, yoy_growth_percent)
VALUES
(2020, 125977, 'Completed Year', NULL),
(2026, 2857815, 'YTD - Partial Year', NULL);

INSERT INTO ev_registrations_monthly
(month, ev_registrations, year, mom_growth_percent)
VALUES
('2025-01-01', 177181, 2025, NULL);

SELECT COUNT(*) FROM ev_registrations_annual;
SELECT COUNT(*) FROM ev_registrations_monthly;

USE ev_intelligence;

SELECT
    year,
    ev_registrations,
    year_status,
    yoy_growth_percent
FROM ev_registrations_annual
ORDER BY year;

SELECT
    year,
    ev_registrations,
    LAG(ev_registrations) OVER (ORDER BY year) AS previous_year_registrations,
    ev_registrations -
        LAG(ev_registrations) OVER (ORDER BY year) AS additional_registrations
FROM ev_registrations_annual
WHERE year_status = 'Completed Year'
ORDER BY year;

SELECT
    YEAR(month) AS registration_year,
    MONTHNAME(month) AS registration_month,
    ev_registrations,
    mom_growth_percent
FROM ev_registrations_monthly
ORDER BY month;

SELECT
    MONTHNAME(m2025.month) AS month_name,
    m2025.ev_registrations AS registrations_2025,
    m2026.ev_registrations AS registrations_2026,
    m2026.ev_registrations - m2025.ev_registrations
        AS additional_registrations,
    ROUND(
        (m2026.ev_registrations - m2025.ev_registrations)
        * 100.0 / m2025.ev_registrations,
        2
    ) AS yoy_change_percent
FROM ev_registrations_monthly m2025
JOIN ev_registrations_monthly m2026
    ON MONTH(m2025.month) = MONTH(m2026.month)
WHERE YEAR(m2025.month) = 2025
  AND YEAR(m2026.month) = 2026
ORDER BY MONTH(m2025.month);

SELECT
    state,
    ev_registrations,
    registration_share_percent,
    registration_rank
FROM ev_registrations_statewise
ORDER BY ev_registrations DESC
LIMIT 10;

SELECT
    CASE
        WHEN registration_rank <= 3 THEN 'Top 3 States'
        WHEN registration_rank <= 10 THEN 'Top 10 States'
    END AS state_group,
    SUM(ev_registrations) AS total_registrations,
    ROUND(SUM(registration_share_percent), 2) AS total_market_share
FROM ev_registrations_statewise
WHERE registration_rank <= 10
GROUP BY
    CASE
        WHEN registration_rank <= 3 THEN 'Top 3 States'
        WHEN registration_rank <= 10 THEN 'Top 10 States'
    END
ORDER BY total_registrations DESC;

SELECT
    'Top 3 States' AS state_group,
    SUM(ev_registrations) AS total_registrations,
    ROUND(SUM(registration_share_percent), 2) AS market_share
FROM ev_registrations_statewise
WHERE registration_rank <= 3

UNION ALL

SELECT
    'Top 10 States',
    SUM(ev_registrations),
    ROUND(SUM(registration_share_percent), 2)
FROM ev_registrations_statewise
WHERE registration_rank <= 10;

SELECT
    r.state,
    r.ev_registrations,
    COUNT(c.id) AS total_stations,
    SUM(c.total_chargers) AS total_chargers,
    SUM(c.total_connectors) AS total_connectors,

    ROUND(
        r.ev_registrations / NULLIF(SUM(c.total_chargers), 0),
        2
    ) AS evs_per_charger

FROM ev_registrations_statewise r

LEFT JOIN ev_charging_stations c
    ON LOWER(TRIM(r.state)) = LOWER(TRIM(c.state))

GROUP BY
    r.state,
    r.ev_registrations

ORDER BY evs_per_charger DESC;

SELECT
    r.state,
    r.ev_registrations,
    COUNT(c.id) AS total_stations,
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
    r.ev_registrations

ORDER BY evs_per_charger DESC;


USE ev_intelligence;

DROP TEMPORARY TABLE IF EXISTS state_gap_analysis;

CREATE TEMPORARY TABLE state_gap_analysis AS
SELECT
    r.state,
    r.ev_registrations,
    COALESCE(SUM(c.total_chargers), 0) AS total_chargers,

    r.ev_registrations /
        NULLIF(SUM(c.total_chargers), 0) AS evs_per_charger

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
    
    SELECT
    state,
    ev_registrations,
    total_chargers,
    ROUND(evs_per_charger, 2) AS evs_per_charger,

    ROUND(
        (ev_registrations - min_demand) /
        NULLIF(max_demand - min_demand, 0) * 100,
        2
    ) AS demand_score,

    ROUND(
        (evs_per_charger - min_pressure) /
        NULLIF(max_pressure - min_pressure, 0) * 100,
        2
    ) AS pressure_score,

    ROUND(
        (
            (ev_registrations - min_demand) /
            NULLIF(max_demand - min_demand, 0) * 0.5
            +
            (evs_per_charger - min_pressure) /
            NULLIF(max_pressure - min_pressure, 0) * 0.5
        ) * 100,
        2
    ) AS infrastructure_gap_score

FROM (
    SELECT *,
        MIN(ev_registrations) OVER () AS min_demand,
        MAX(ev_registrations) OVER () AS max_demand,
        MIN(evs_per_charger) OVER () AS min_pressure,
        MAX(evs_per_charger) OVER () AS max_pressure
    FROM state_gap_analysis
) AS metrics

ORDER BY infrastructure_gap_score DESC
LIMIT 10;

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

GROUP BY operator

ORDER BY total_stations DESC
LIMIT 10;

SELECT
    operator,
    COUNT(*) AS total_stations,
    SUM(total_chargers) AS total_chargers,

    ROUND(
        SUM(total_chargers) /
        NULLIF(COUNT(*), 0),
        2
    ) AS chargers_per_station

FROM ev_charging_stations

GROUP BY operator

ORDER BY chargers_per_station DESC
LIMIT 10;

SELECT
    Power_Category,
    COUNT(*) AS total_stations,

    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM ev_charging_stations),
        2
    ) AS percentage_share,

    ROUND(AVG(max_power_kw), 2) AS average_power_kw,
    MAX(max_power_kw) AS highest_power_kw

FROM ev_charging_stations

GROUP BY Power_Category

ORDER BY average_power_kw;

DESCRIBE ev_charging_stations;

SELECT
    location_quality,
    geo_validated,
    COUNT(*) AS total_stations,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM ev_charging_stations),
        2
    ) AS percentage_share
FROM ev_charging_stations
GROUP BY
    location_quality,
    geo_validated
ORDER BY total_stations DESC;

SELECT
    ownership,
    COUNT(*) AS total_stations,
    SUM(total_chargers) AS total_chargers,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM ev_charging_stations),
        2
    ) AS station_share_percent
FROM ev_charging_stations
GROUP BY ownership
ORDER BY total_stations DESC;

SELECT
    r.state,
    r.ev_registrations,
    COUNT(c.id) AS total_stations,

    SUM(
        CASE WHEN c.geo_validated = 1
        THEN 1 ELSE 0 END
    ) AS validated_stations,

    SUM(
        CASE WHEN c.geo_validated = 0
        THEN 1 ELSE 0 END
    ) AS suspect_stations,

    COALESCE(SUM(c.total_chargers), 0) AS total_chargers,

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
    r.ev_registrations

ORDER BY r.ev_registrations DESC;

CREATE OR REPLACE VIEW vw_ev_station_map AS
SELECT
    state,
    latitude,
    longitude,
    COUNT(*) AS total_stations
FROM ev_charging_stations
WHERE geo_validated = 1
  AND mixed_admin = 0
  AND latitude IS NOT NULL
  AND longitude IS NOT NULL
GROUP BY
    state,
    latitude,
    longitude;
    
CREATE OR REPLACE VIEW vw_ownership_analysis AS
SELECT
    ownership,
    COUNT(*) AS total_stations,
    SUM(total_chargers) AS total_chargers,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM ev_charging_stations),
        2
    ) AS station_share_percent
FROM ev_charging_stations
GROUP BY ownership;