
import streamlit as st

from utils.database import fetch_dataframe, test_connection


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="EV Intelligence | India",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #00D4FF;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 16px;
        color: #AAB4C3;
        margin-top: 5px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 10px;
    }

    .info-card {
        background-color: #172334;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #26384D;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("⚡ EV Intelligence")

st.sidebar.markdown("---")

st.sidebar.markdown("### Project Navigation")
st.sidebar.info(
    "Use the pages in this sidebar to explore "
    "the EV market, charging infrastructure, "
    "state analysis and forecasts."
)

st.sidebar.markdown("---")
st.sidebar.caption("India EV Analytics Project")
st.sidebar.caption("Python | MySQL | Streamlit | Power BI")


# --------------------------------------------------
# HOME PAGE HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">⚡ EV Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'India Electric Vehicle Market & Charging '
    'Infrastructure Analytics'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("---")

st.markdown("""
Explore India's electric vehicle ecosystem through
registration trends, charging infrastructure,
state-level comparisons and predictive analytics.
""")


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

try:
    if test_connection():
        st.success("Connected to Aiven MySQL database")
    else:
        st.error("Database connection could not be verified.")

except Exception as error:
    st.error("Database connection failed.")
    st.exception(error)
    st.stop()


# --------------------------------------------------
# FETCH DATABASE METRICS
# --------------------------------------------------

try:
    annual_data = fetch_dataframe("""
        SELECT
            year,
            ev_registrations,
            year_status
        FROM vw_annual_ev_growth
        ORDER BY year DESC
        LIMIT 1
    """)

    infrastructure_data = fetch_dataframe("""
        SELECT
            COUNT(*) AS total_states,
            SUM(total_stations) AS total_stations,
            SUM(total_chargers) AS total_chargers
        FROM vw_state_ev_infrastructure
    """)

    if annual_data.empty or infrastructure_data.empty:
        st.warning("No dashboard data is currently available.")
        st.stop()

    latest_year = int(annual_data.iloc[0]["year"])
    latest_registrations = int(
        annual_data.iloc[0]["ev_registrations"]
    )
    year_status = str(annual_data.iloc[0]["year_status"])

    total_states = int(
        infrastructure_data.iloc[0]["total_states"]
    )
    total_stations = int(
        infrastructure_data.iloc[0]["total_stations"]
    )
    total_chargers = int(
        infrastructure_data.iloc[0]["total_chargers"]
    )

except Exception as error:
    st.error("Unable to load dashboard metrics.")
    st.exception(error)
    st.stop()


# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">India EV Market at a Glance</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label=f"EV Registrations ({latest_year})",
        value=f"{latest_registrations:,}"
    )
    st.caption(year_status)

with col2:
    st.metric(
        label="Charging Stations",
        value=f"{total_stations:,}"
    )

with col3:
    st.metric(
        label="Total Chargers",
        value=f"{total_chargers:,}"
    )

with col4:
    st.metric(
        label="States / UTs",
        value=f"{total_states:,}"
    )



# --------------------------------------------------
# PROJECT MODULES
# --------------------------------------------------

st.markdown("---")

st.markdown(
    '<div class="section-title">Explore Analytics Modules</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 EV Market Analysis")
    st.write(
        "Explore annual growth, monthly registration "
        "trends and changes in India's EV market."
    )

    if st.button("Open EV Market →", key="home_ev_market",
                 use_container_width=True):
        st.switch_page("pages/1_EV_Market.py")

    st.subheader("🗺️ State-Wise Analysis")
    st.write(
        "Compare EV registrations and charging "
        "infrastructure across Indian states."
    )

    if st.button("Open State Analysis →", key="home_state",
                 use_container_width=True):
        st.switch_page("pages/3_State_Analysis.py")

with col2:
    st.subheader("🔌 Charging Infrastructure")
    st.write(
        "Analyze charging station distribution, "
        "operators, ownership and power categories."
    )

    if st.button("Open Charging Infrastructure →",
                 key="home_charging",
                 use_container_width=True):
        st.switch_page("pages/2_Charging_Infrastructure.py")

    st.subheader("🔮 EV Registration Forecast")
    st.write(
        "Explore historical registration patterns "
        "and the experimental six-month forecast."
    )

    if st.button("Open EV Forecast →", key="home_forecast",
                 use_container_width=True):
        st.switch_page("pages/4_EV_Forecast.py")


# --------------------------------------------------
# DATA NOTES
# --------------------------------------------------

st.markdown("---")

st.markdown("### About This Project")

st.write("""
EV Intelligence is an end-to-end analytics project
designed to understand India's electric vehicle market
and charging infrastructure using data analytics,
database management, visualization and forecasting.
""")

st.info(
    "Data note: 2026 annual registrations are year-to-date "
    "partial figures, not full-year totals. Charging "
    "infrastructure data represents the available "
    "26 October 2025 snapshot, not live station data."
)

st.caption(
    "Developed using Python, MySQL, Power BI and Streamlit."
)
