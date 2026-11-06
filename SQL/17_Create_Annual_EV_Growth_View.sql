USE ev_intelligence;

CREATE OR REPLACE VIEW vw_annual_ev_growth AS

SELECT
    year,
    ev_registrations,
    year_status,
    yoy_growth_percent
FROM ev_registrations_annual
ORDER BY year;

SELECT *
FROM vw_annual_ev_growth;