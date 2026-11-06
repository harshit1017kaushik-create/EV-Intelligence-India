
import streamlit as st
import pandas as pd

from utils.database import fetch_dataframe
from utils.charts import (
    create_bar_chart,
    create_scatter_chart
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="State Analysis | EV Intelligence",
    page_icon="🗺️",
    layout="wide"
)


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🗺️ State-Wise EV Analysis")

st.markdown(
    "Explore electric vehicle registrations, charging "
    "infrastructure and infrastructure gap indicators "
    "across Indian states and union territories."
)

st.divider()


# --------------------------------------------------
# LOAD DATA FROM MYSQL VIEWS
# --------------------------------------------------

@st.cache_data(ttl=300, show_spinner=False)
def load_state_data():

    state_df = fetch_dataframe("""
        SELECT *
        FROM vw_state_ev_infrastructure
        ORDER BY ev_registrations DESC
    """)

    gap_df = fetch_dataframe("""
        SELECT *
        FROM vw_state_infrastructure_gap
        ORDER BY infrastructure_gap_score DESC
    """)

    return state_df, gap_df


try:
    state_df, gap_df = load_state_data()

    if state_df.empty or gap_df.empty:
        st.warning("State-wise data is not available.")
        st.stop()

except Exception as error:
    st.error("Unable to load state-wise analysis data.")
    st.exception(error)
    st.stop()


# --------------------------------------------------
# DATA PREPARATION
# --------------------------------------------------

numeric_columns = [
    "ev_registrations",
    "total_stations",
    "validated_stations",
    "suspect_stations",
    "total_chargers",
    "total_connectors",
    "evs_per_charger"
]

for column in numeric_columns:
    if column in state_df.columns:
        state_df[column] = pd.to_numeric(
            state_df[column],
            errors="coerce"
        )

gap_numeric_columns = [
    "ev_registrations",
    "total_chargers",
    "evs_per_charger",
    "demand_score",
    "pressure_score",
    "infrastructure_gap_score"
]

for column in gap_numeric_columns:
    if column in gap_df.columns:
        gap_df[column] = pd.to_numeric(
            gap_df[column],
            errors="coerce"
        )

st.success("State-wise data loaded successfully from Aiven MySQL.")

st.caption(
    f"States and UTs available: {state_df['state'].nunique()}"
)

st.divider()


# --------------------------------------------------
# STATE-WISE KPI OVERVIEW
# --------------------------------------------------

total_registrations = int(
    state_df["ev_registrations"].sum()
)

total_stations = int(
    state_df["total_stations"].sum()
)

total_chargers = int(
    state_df["total_chargers"].sum()
)

average_evs_per_charger = (
    total_registrations / total_chargers
    if total_chargers > 0
    else 0
)


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.subheader("India EV Infrastructure Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total EV Registrations",
        f"{total_registrations:,}"
    )

with col2:
    st.metric(
        "Total Charging Stations",
        f"{total_stations:,}"
    )

with col3:
    st.metric(
        "Total Chargers",
        f"{total_chargers:,}"
    )

with col4:
    st.metric(
        "Average EVs per Charger",
        f"{average_evs_per_charger:.2f}"
    )

st.caption(
    "Registrations cover 2020–2026 YTD. "
    "Infrastructure figures represent the available station dataset."
)

st.divider()


# --------------------------------------------------
# STATE-WISE EV REGISTRATION ANALYSIS
# --------------------------------------------------

st.subheader("1. State-Wise EV Registration Analysis")

st.write(
    "Compare EV registrations across Indian states "
    "and identify the leading EV markets."
)

available_states = sorted(
    state_df["state"].dropna().unique()
)

selected_states = st.multiselect(
    "Select States for Comparison",
    options=available_states,
    default=available_states,
    help="Select one or more states to compare EV registrations."
)

if not selected_states:

    st.warning("Please select at least one state.")

else:

    filtered_state_df = state_df[
        state_df["state"].isin(selected_states)
    ].copy()

    top_registration_states = filtered_state_df.nlargest(
        10, "ev_registrations"
    )

    registration_chart = create_bar_chart(
        top_registration_states,
        x="ev_registrations",
        y="state",
        title="Top 10 States by EV Registrations",
        orientation="h"
    )

    registration_chart.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Total EV Registrations",
        yaxis_title="State"
    )

    st.plotly_chart(
        registration_chart,
        use_container_width=True
    )

st.divider()


# --------------------------------------------------
# STATE-WISE CHARGING INFRASTRUCTURE ANALYSIS
# --------------------------------------------------

st.subheader("2. State-Wise Charging Infrastructure")

st.write(
    "Compare charging station and charger distribution "
    "across Indian states."
)

if not selected_states:
    st.warning("Please select at least one state.")

else:

    infrastructure_df = state_df[
        state_df["state"].isin(selected_states)
    ].copy()

    # Top 10 states by stations
    top_station_states = infrastructure_df.nlargest(
        10, "total_stations"
    )

    station_chart = create_bar_chart(
        top_station_states,
        x="total_stations",
        y="state",
        title="Top 10 States by Charging Stations",
        orientation="h"
    )

    station_chart.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Number of Charging Stations",
        yaxis_title="State"
    )

    st.plotly_chart(
        station_chart,
        use_container_width=True
    )

    # Top 10 states by chargers
    top_charger_states = infrastructure_df.nlargest(
        10, "total_chargers"
    )

    charger_chart = create_bar_chart(
        top_charger_states,
        x="total_chargers",
        y="state",
        title="Top 10 States by Total Chargers",
        orientation="h"
    )

    charger_chart.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Number of Chargers",
        yaxis_title="State"
    )

    st.plotly_chart(
        charger_chart,
        use_container_width=True
    )

st.divider()


# --------------------------------------------------
# EVS PER CHARGER ANALYSIS
# --------------------------------------------------

st.subheader("3. EVs per Charger Analysis")

st.write(
    "Compare the number of EV registrations against "
    "available chargers across Indian states."
)

ev_charger_df = state_df.dropna(
    subset=["evs_per_charger"]
).copy()

ev_charger_df = ev_charger_df[
    ev_charger_df["total_chargers"] > 0
]

filtered_ev_charger_df = ev_charger_df[
    ev_charger_df["state"].isin(selected_states)
].copy()

if filtered_ev_charger_df.empty:

    st.warning("No valid EV-to-charger data available.")

else:

    top_pressure_states = filtered_ev_charger_df.nlargest(
        10, "evs_per_charger"
    )

    ev_charger_chart = create_bar_chart(
        top_pressure_states,
        x="evs_per_charger",
        y="state",
        title="Top 10 States by EVs per Charger",
        orientation="h"
    )

    ev_charger_chart.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="EV Registrations per Charger",
        yaxis_title="State"
    )

    st.plotly_chart(
        ev_charger_chart,
        use_container_width=True
    )


    # Relationship between registrations and chargers

    relationship_chart = create_scatter_chart(
        filtered_ev_charger_df,
        x="total_chargers",
        y="ev_registrations",
        title="EV Registrations vs Total Chargers",
        color="state"
    )

    relationship_chart.update_layout(
        xaxis_title="Total Chargers",
        yaxis_title="EV Registrations"
    )

    st.plotly_chart(
        relationship_chart,
        use_container_width=True
    )

st.divider()


# --------------------------------------------------
# INFRASTRUCTURE GAP ANALYSIS
# --------------------------------------------------

st.subheader("4. EV Charging Infrastructure Gap Analysis")

st.write(
    "Identify states with higher preliminary infrastructure "
    "gap scores using EV demand and charging infrastructure indicators."
)

# State filter
available_gap_states = sorted(
    gap_df["state"].dropna().unique()
)

selected_gap_states = st.multiselect(
    "Select States for Gap Analysis",
    options=available_gap_states,
    default=available_gap_states,
    key="gap_state_filter",
    help="Select states to compare infrastructure gap indicators."
)

if not selected_gap_states:

    st.warning("Please select at least one state.")

else:

    filtered_gap_df = gap_df[
        gap_df["state"].isin(selected_gap_states)
    ].copy()

    # Top 10 states by infrastructure gap score
    top_gap_states = filtered_gap_df.nlargest(
        10, "infrastructure_gap_score"
    )

    gap_chart = create_bar_chart(
        top_gap_states,
        x="infrastructure_gap_score",
        y="state",
        title="Top 10 States by Infrastructure Gap Score",
        orientation="h"
    )

    gap_chart.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Infrastructure Gap Score",
        yaxis_title="State"
    )

    st.plotly_chart(
        gap_chart,
        use_container_width=True
    )


    # Demand score vs pressure score
    score_chart = create_scatter_chart(
        filtered_gap_df,
        x="demand_score",
        y="pressure_score",
        title="Demand Score vs Infrastructure Pressure Score",
        color="state"
    )

    score_chart.update_layout(
        xaxis_title="EV Demand Score",
        yaxis_title="Infrastructure Pressure Score"
    )

    st.plotly_chart(
        score_chart,
        use_container_width=True
    )

    # Infrastructure gap data table
    st.markdown("#### Infrastructure Gap Details")

    gap_display = filtered_gap_df[
        [
            "state",
            "ev_registrations",
            "total_chargers",
            "evs_per_charger",
            "demand_score",
            "pressure_score",
            "infrastructure_gap_score"
        ]
    ].sort_values(
        "infrastructure_gap_score",
        ascending=False
    ).copy()

    gap_display = gap_display.rename(
        columns={
            "state": "State",
            "ev_registrations": "EV Registrations",
            "total_chargers": "Total Chargers",
            "evs_per_charger": "EVs per Charger",
            "demand_score": "Demand Score",
            "pressure_score": "Pressure Score",
            "infrastructure_gap_score": "Infrastructure Gap Score"
        }
    )

    st.dataframe(
        gap_display,
        use_container_width=True,
        hide_index=True
    )

st.divider()


# --------------------------------------------------
# CONSOLIDATED STATE-WISE ANALYSIS TABLE
# --------------------------------------------------

st.subheader("5. Consolidated State-Wise Data")

st.write(
    "Explore EV registrations and charging infrastructure "
    "indicators for the selected states."
)

consolidated_df = state_df.merge(
    gap_df[
        [
            "state",
            "demand_score",
            "pressure_score",
            "infrastructure_gap_score"
        ]
    ],
    on="state",
    how="left"
)

consolidated_df = consolidated_df[
    consolidated_df["state"].isin(selected_states)
].copy()

display_columns = [
    "state",
    "ev_registrations",
    "total_stations",
    "total_chargers",
    "evs_per_charger",
    "infrastructure_gap_score"
]

consolidated_display = consolidated_df[
    display_columns
].sort_values(
    "infrastructure_gap_score",
    ascending=False
).rename(
    columns={
        "state": "State",
        "ev_registrations": "EV Registrations",
        "total_stations": "Charging Stations",
        "total_chargers": "Total Chargers",
        "evs_per_charger": "EVs per Charger",
        "infrastructure_gap_score": "Infrastructure Gap Score"
    }
)

st.dataframe(
    consolidated_display,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    label="Download State Analysis CSV",
    data=consolidated_display.to_csv(index=False).encode("utf-8"),
    file_name="EV_State_Analysis.csv",
    mime="text/csv"
)

st.divider()


# --------------------------------------------------
# DATA QUALITY AND METHODOLOGY NOTES
# --------------------------------------------------

st.subheader("Data Quality & Methodology Notes")

with st.expander("View Data Notes and Limitations"):

    st.markdown("""
    **1. EV Registration Data**
    - Registration figures cover 2020 to October 2026.
    - 2026 represents year-to-date partial registrations.

    **2. Charging Infrastructure Data**
    - Charging station data contains 29,184 records.
    - The infrastructure dataset represents a snapshot dated
      26 October 2025, not live station availability.
    - Station, charger and connector counts are different measures.

    **3. Geographic Validation**
    - 29,069 station records passed geographic screening.
    - 115 records were flagged for further review.
    - Suspect and mixed administrative records are excluded
      from the validated station map.

    **4. Infrastructure Gap Score**
    - The score combines normalized demand and infrastructure
      pressure indicators.
    - It is a preliminary screening indicator, not proof of
      an actual charging shortage.

    **5. Analytical Limitations**
    - EVs per charger is a comparative pressure indicator.
    - Correlations do not establish causation.
    - State-level comparisons should be interpreted in the
      context of the available data coverage.
    """)

st.caption(
    "EV Intelligence | India EV Market & Charging Infrastructure Analytics"
)
