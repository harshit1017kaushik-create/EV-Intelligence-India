
import streamlit as st
import pandas as pd

from utils.database import fetch_dataframe
from utils.charts import (
    create_bar_chart,
    create_donut_chart
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Charging Infrastructure | EV Intelligence",
    page_icon="🔌",
    layout="wide"
)


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🔌 Charging Infrastructure Analysis")

st.markdown(
    "Explore India's EV charging ecosystem through "
    "station distribution, operators, ownership "
    "and charging power categories."
)

st.divider()


# --------------------------------------------------
# LOAD DATA FROM MYSQL VIEWS
# --------------------------------------------------

@st.cache_data(ttl=300, show_spinner=False)
def load_infrastructure_data():

    state_df = fetch_dataframe("""
        SELECT *
        FROM vw_state_ev_infrastructure
        ORDER BY total_stations DESC
    """)

    operator_df = fetch_dataframe("""
        SELECT *
        FROM vw_operator_analysis
        ORDER BY total_stations DESC
    """)

    ownership_df = fetch_dataframe("""
        SELECT *
        FROM vw_ownership_analysis
        ORDER BY total_stations DESC
    """)

    power_df = fetch_dataframe("""
        SELECT *
        FROM vw_charging_power_analysis
        ORDER BY total_stations DESC
    """)

    return state_df, operator_df, ownership_df, power_df


try:
    (
        state_df,
        operator_df,
        ownership_df,
        power_df
    ) = load_infrastructure_data()

    if any(
        df.empty for df in [
            state_df,
            operator_df,
            ownership_df,
            power_df
        ]
    ):
        st.warning("Some infrastructure data is unavailable.")
        st.stop()

except Exception as error:
    st.error("Unable to load charging infrastructure data.")
    st.exception(error)
    st.stop()

# --------------------------------------------------
# DATA PREPARATION
# --------------------------------------------------

total_stations = int(state_df["total_stations"].sum())
total_chargers = int(state_df["total_chargers"].sum())
total_connectors = int(state_df["total_connectors"].sum())

total_operators = operator_df["operator"].nunique()


# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

st.subheader("Charging Infrastructure Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Charging Stations",
        f"{total_stations:,}"
    )

with col2:
    st.metric(
        "Total Chargers",
        f"{total_chargers:,}"
    )

with col3:
    st.metric(
        "Total Connectors",
        f"{total_connectors:,}"
    )

with col4:
    st.metric(
        "Charging Operators",
        f"{total_operators:,}"
    )

st.caption(
    "Source: EV Intelligence charging infrastructure dataset"
)

st.divider()


# --------------------------------------------------
# STATE-WISE CHARGING STATION ANALYSIS
# --------------------------------------------------

st.subheader("1. State-Wise Charging Station Distribution")

st.write(
    "Compare charging station availability across "
    "Indian states and identify leading regions."
)

# State filter
available_states = sorted(state_df["state"].dropna().unique())

selected_states = st.multiselect(
    "Select States",
    options=available_states,
    default=available_states,
    help="Select states to compare charging infrastructure."
)

if not selected_states:
    st.warning("Please select at least one state.")
else:

    filtered_state_df = state_df[
        state_df["state"].isin(selected_states)
    ].copy()

    top_states_df = filtered_state_df.nlargest(
        10, "total_stations"
    )

    state_chart = create_bar_chart(
        top_states_df,
        x="total_stations",
        y="state",
        title="Top 10 States by EV Charging Stations",
        orientation="h"
    )

    state_chart.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Number of Charging Stations",
        yaxis_title="State"
    )

    st.plotly_chart(
        state_chart,
        use_container_width=True
    )

st.divider()


# --------------------------------------------------
# OPERATOR-WISE ANALYSIS
# --------------------------------------------------

st.subheader("2. Operator-Wise Charging Station Analysis")

st.write(
    "Identify the leading EV charging operators "
    "based on their station network across India."
)

available_operators = sorted(
    operator_df["operator"].dropna().unique()
)

selected_operators = st.multiselect(
    "Select Charging Operators",
    options=available_operators,
    default=available_operators,
    help="Select operators to compare their station networks."
)

if not selected_operators:
    st.warning("Please select at least one operator.")

else:

    filtered_operator_df = operator_df[
        operator_df["operator"].isin(selected_operators)
    ].copy()

    top_operators_df = filtered_operator_df.nlargest(
        10, "total_stations"
    )

    operator_chart = create_bar_chart(
        top_operators_df,
        x="total_stations",
        y="operator",
        title="Top 10 EV Charging Operators in India",
        orientation="h"
    )

    operator_chart.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Number of Charging Stations",
        yaxis_title="Charging Operator"
    )

    st.plotly_chart(
        operator_chart,
        use_container_width=True
    )

st.divider()


# --------------------------------------------------
# OWNERSHIP ANALYSIS
# --------------------------------------------------

st.subheader("3. Charging Station Ownership Analysis")

st.write(
    "Understand the distribution of EV charging "
    "stations across different ownership categories."
)

ownership_chart = create_donut_chart(
    ownership_df,
    names="ownership",
    values="total_stations",
    title="EV Charging Stations by Ownership"
)

st.plotly_chart(
    ownership_chart,
    use_container_width=True
)

# Ownership summary table

st.markdown("#### Ownership Breakdown")

ownership_display = ownership_df[
    [
        "ownership",
        "total_stations",
        "total_chargers",
        "station_share_percent"
    ]
].copy()

ownership_display = ownership_display.rename(
    columns={
        "ownership": "Ownership Type",
        "total_stations": "Total Stations",
        "total_chargers": "Total Chargers",
        "station_share_percent": "Station Share (%)"
    }
)

st.dataframe(
    ownership_display,
    use_container_width=True,
    hide_index=True
)

st.divider()


# --------------------------------------------------
# CHARGING POWER CATEGORY ANALYSIS
# --------------------------------------------------

st.subheader("4. Charging Power Category Analysis")

st.write(
    "Analyze the distribution of EV charging stations "
    "based on their maximum charging power."
)

# Power category bar chart
power_chart = create_bar_chart(
    power_df,
    x="Power_Category",
    y="total_stations",
    title="Charging Stations by Power Category"
)

power_chart.update_layout(
    xaxis_title="Charging Power Category",
    yaxis_title="Number of Charging Stations"
)

st.plotly_chart(
    power_chart,
    use_container_width=True
)


# Power category donut chart
power_donut = create_donut_chart(
    power_df,
    names="Power_Category",
    values="total_stations",
    title="Charging Station Market Share by Power Category"
)

st.plotly_chart(
    power_donut,
    use_container_width=True
)


# Power category comparison table
st.markdown("#### Charging Power Comparison")

power_display = power_df[
    [
        "Power_Category",
        "total_stations",
        "station_share_percent",
        "average_power_kw",
        "maximum_power_kw"
    ]
].copy()

power_display = power_display.rename(
    columns={
        "Power_Category": "Power Category",
        "total_stations": "Total Stations",
        "station_share_percent": "Station Share (%)",
        "average_power_kw": "Average Power (kW)",
        "maximum_power_kw": "Maximum Power (kW)"
    }
)

st.dataframe(
    power_display,
    use_container_width=True,
    hide_index=True
)

st.divider()


# --------------------------------------------------
# DATA NOTES
# --------------------------------------------------

st.info(
    "Power categories use project-defined thresholds: "
    "Low (≤7.4 kW), Medium (>7.4–22 kW), "
    "High (>22 kW). Missing power information should "
    "not be interpreted as zero."
)

st.caption(
    "Source: EV Intelligence MySQL database | "
    "View: vw_charging_power_analysis"
)
