USE ev_intelligence;

CREATE OR REPLACE VIEW vw_state_infrastructure_gap AS
SELECT
    state,
    ev_registrations,
    total_chargers,
    evs_per_charger,

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
            (
                (ev_registrations - min_demand) /
                NULLIF(max_demand - min_demand, 0) * 100
            ) * 0.5
            +
            (
                (evs_per_charger - min_pressure) /
                NULLIF(max_pressure - min_pressure, 0) * 100
            ) * 0.5
        ),
        2
    ) AS infrastructure_gap_score

FROM (
    SELECT
        *,
        MIN(ev_registrations) OVER () AS min_demand,
        MAX(ev_registrations) OVER () AS max_demand,
        MIN(evs_per_charger) OVER () AS min_pressure,
        MAX(evs_per_charger) OVER () AS max_pressure
    FROM vw_state_ev_infrastructure
) AS metrics;

SELECT *
FROM vw_state_infrastructure_gap
ORDER BY infrastructure_gap_score DESC;