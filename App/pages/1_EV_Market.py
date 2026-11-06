
import streamlit as st
import pandas as pd

from utils.database import fetch_dataframe
from utils.charts import (
    create_bar_chart,
    create_line_chart
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="EV Market Analysis | EV Intelligence",
    page_icon="📈",
    layout="wide"
)


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("📈 EV Market Analysis")

st.markdown(
    "Analyze India's electric vehicle registration "
    "growth through annual and monthly trends."
)

st.divider()


# --------------------------------------------------
# LOAD DATA FROM MYSQL VIEWS
# --------------------------------------------------

@st.cache_data(ttl=300, show_spinner=False)
def load_market_data():

    annual_df = fetch_dataframe("""
        SELECT
            year,
            ev_registrations,
            year_status,
            yoy_growth_percent
        FROM vw_annual_ev_growth
        ORDER BY year
    """)

    monthly_df = fetch_dataframe("""
        SELECT
            month,
            registration_year,
            registration_month,
            ev_registrations,
            mom_growth_percent
        FROM vw_monthly_ev_trends
        ORDER BY registration_year, registration_month
    """)

    return annual_df, monthly_df


try:
    annual_df, monthly_df = load_market_data()

    if annual_df.empty or monthly_df.empty:
        st.warning("Registration data is not available.")
        st.stop()

except Exception as error:
    st.error("Unable to load EV registration data.")
    st.exception(error)
    st.stop()


# --------------------------------------------------
# DATA PREPARATION
# --------------------------------------------------

annual_df["year"] = pd.to_numeric(
    annual_df["year"]
)

annual_df["ev_registrations"] = pd.to_numeric(
    annual_df["ev_registrations"]
)

annual_df["yoy_growth_percent"] = pd.to_numeric(
    annual_df["yoy_growth_percent"],
    errors="coerce"
)

monthly_df["ev_registrations"] = pd.to_numeric(
    monthly_df["ev_registrations"]
)

monthly_df["mom_growth_percent"] = pd.to_numeric(
    monthly_df["mom_growth_percent"],
    errors="coerce"
)

monthly_df["month"] = pd.to_datetime(
    monthly_df["month"]
)
monthly_df = monthly_df.sort_values(
    by="month",
    ascending=True
).reset_index(drop=True)

latest_annual = annual_df.iloc[-1]
latest_monthly = monthly_df.iloc[-1]


# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

st.subheader("India EV Market Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Latest Annual Registrations",
        f"{int(latest_annual['ev_registrations']):,}"
    )
    st.caption(
        f"Year: {int(latest_annual['year'])}"
    )

with col2:
    st.metric(
        "Latest Monthly Registrations",
        f"{int(latest_monthly['ev_registrations']):,}"
    )
    st.caption(
        latest_monthly["month"].strftime("%B %Y")
    )

completed_years = annual_df[
    annual_df["year_status"] == "Completed Year"
].dropna(subset=["yoy_growth_percent"])

with col3:
    if not completed_years.empty:
        latest_completed = completed_years.iloc[-1]

        st.metric(
            "Latest Completed-Year YoY Growth",
            f"{latest_completed['yoy_growth_percent']:.2f}%"
        )

        st.caption(f"Year: {int(latest_completed['year'])}")
    else:
        st.metric("Latest Completed-Year YoY Growth", "N/A")
with col4:
    st.metric(
        "Latest MoM Growth",
        (
            f"{latest_monthly['mom_growth_percent']:.2f}%"
            if pd.notna(latest_monthly["mom_growth_percent"])
            else "N/A"
        )
    )

st.caption(
    "Annual 2026 registrations are year-to-date partial figures."
)

st.divider()



# --------------------------------------------------
# YEAR FILTER
# --------------------------------------------------

st.subheader("Filter Annual Registration Data")

available_years = sorted(
    annual_df["year"].astype(int).tolist()
)

selected_years = st.multiselect(
    "Select Year(s)",
    options=available_years,
    default=available_years,
    help="Select one or more years to filter annual analysis."
)

if not selected_years:
    st.warning("Please select at least one year.")
    st.stop()

filtered_annual_df = annual_df[
    annual_df["year"].isin(selected_years)
].copy()

# --------------------------------------------------
# ANNUAL REGISTRATION ANALYSIS
# --------------------------------------------------

st.subheader("1. Annual EV Registration Trend")

st.write(
    "Track the growth of electric vehicle registrations "
    "across India from 2020 to 2026."
)

annual_chart = create_bar_chart(
    filtered_annual_df,
    x="year",
    y="ev_registrations",
    title="Annual EV Registrations in India",
)

st.plotly_chart(
    annual_chart,
    use_container_width=True
)


# --------------------------------------------------
# YEAR-OVER-YEAR GROWTH
# --------------------------------------------------

st.subheader("2. Year-over-Year Growth")

st.write(
    "Understand the percentage change in EV registrations "
    "compared with the previous year."
)

yoy_df = filtered_annual_df.dropna(
    subset=["yoy_growth_percent"]
).copy()

if not yoy_df.empty:

    yoy_chart = create_line_chart(
        yoy_df,
        x="year",
        y="yoy_growth_percent",
        title="Year-over-Year EV Registration Growth (%)"
    )

    st.plotly_chart(
        yoy_chart,
        use_container_width=True
    )

else:
    st.info("YoY growth data is not available.")


st.divider()




# --------------------------------------------------
# MONTHLY DATE FILTER
# --------------------------------------------------

st.subheader("Filter Monthly Registration Data")

min_month = monthly_df["month"].min().date()
max_month = monthly_df["month"].max().date()

date_col1, date_col2 = st.columns(2)

with date_col1:
    start_date = st.date_input(
        "Start Date",
        value=min_month,
        min_value=min_month,
        max_value=max_month,
        format="DD/MM/YYYY"
    )

with date_col2:
    end_date = st.date_input(
        "End Date",
        value=max_month,
        min_value=min_month,
        max_value=max_month,
        format="DD/MM/YYYY"
    )

if start_date > end_date:
    st.warning("Start Date cannot be after End Date.")
    filtered_monthly_df = pd.DataFrame(
        columns=monthly_df.columns
    )
else:
    filtered_monthly_df = monthly_df[
        (monthly_df["month"] >= pd.Timestamp(start_date)) &
        (monthly_df["month"] <= pd.Timestamp(end_date))
    ].copy()

# --------------------------------------------------
# MONTHLY REGISTRATION ANALYSIS
# --------------------------------------------------

st.subheader("3. Monthly EV Registration Trend")

st.write(
    "Explore monthly changes in EV registrations "
    "from January 2025 onward."
)

monthly_chart = create_line_chart(
    filtered_monthly_df,
    x="month",
    y="ev_registrations",
    title="Monthly EV Registrations in India"
)

st.plotly_chart(
    monthly_chart,
    use_container_width=True
)


# --------------------------------------------------
# MONTH-OVER-MONTH GROWTH
# --------------------------------------------------

st.subheader("4. Month-over-Month Growth")

st.write(
    "Analyze the percentage increase or decrease "
    "in registrations compared with the previous month."
)

mom_df = filtered_monthly_df.dropna(
    subset=["mom_growth_percent"]
).copy()

if not mom_df.empty:

    mom_chart = create_line_chart(
        mom_df,
        x="month",
        y="mom_growth_percent",
        title="Month-over-Month EV Registration Growth (%)"
    )

    st.plotly_chart(
        mom_chart,
        use_container_width=True
    )

else:
    st.info("MoM growth data is not available.")


st.divider()


# --------------------------------------------------
# REGISTRATION DATA TABLES
# --------------------------------------------------

with st.expander("View Annual Registration Data"):

    st.dataframe(
        annual_df,
        use_container_width=True,
        hide_index=True
    )


with st.expander("View Monthly Registration Data"):

    st.dataframe(
        monthly_df,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# DATA NOTES
# --------------------------------------------------

st.info(
    "Data interpretation: 2026 annual registrations are "
    "YTD partial figures. Monthly data covers January 2025 "
    "onward; October 2026 may also be partial."
)

st.caption(
    "Source: EV Intelligence MySQL database | "
    "Views: vw_annual_ev_growth and vw_monthly_ev_trends"
)
