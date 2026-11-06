USE ev_intelligence;

CREATE OR REPLACE VIEW vw_monthly_ev_trends AS
SELECT
    month,
    YEAR(month) AS registration_year,
    MONTHNAME(month) AS registration_month,
    ev_registrations,
    mom_growth_percent
FROM ev_registrations_monthly
ORDER BY month;

SELECT *
FROM vw_monthly_ev_trends;