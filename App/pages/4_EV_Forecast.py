
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="EV Registration Forecast",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stMetric"] {
        background: rgba(30, 80, 90, 0.30);
        padding: 16px;
        border-radius: 10px;
        border: 1px solid rgba(100, 200, 180, 0.25);
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# FILE PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FOLDER = PROJECT_ROOT / "Data" / "Forecast Data"

HISTORICAL_FILE = (
    DATA_FOLDER / "EV_Registrations_Monthly_Historical_Processed.csv"
)

FORECAST_FILE = (
    DATA_FOLDER / "EV_Registration_6_Month_Forecast.csv"
)

TEST_FILE = (
    DATA_FOLDER / "EV_Model_Test_Predictions.csv"
)


# =========================================================
# DATA LOADING
# =========================================================

@st.cache_data(ttl=300)
def load_forecast_data():

    historical = pd.read_csv(HISTORICAL_FILE)
    forecast = pd.read_csv(FORECAST_FILE)
    test = pd.read_csv(TEST_FILE)

    historical["Month"] = pd.to_datetime(
        historical["Month"]
    )

    forecast["Month"] = pd.to_datetime(
        forecast["Month"]
    )

    test["Month"] = pd.to_datetime(
        test["Month"]
    )

    numeric_columns = {
        "historical": ["EV_Registrations"],
        "forecast": ["Predicted_EV_Registrations"],
        "test": [
            "Actual_EV_Registrations",
            "Linear_Regression",
            "Holt",
            "Fixed_Origin_Naive",
            "Random_Forest"
        ]
    }

    for column in numeric_columns["historical"]:
        historical[column] = pd.to_numeric(
            historical[column], errors="coerce"
        )

    for column in numeric_columns["forecast"]:
        forecast[column] = pd.to_numeric(
            forecast[column], errors="coerce"
        )

    for column in numeric_columns["test"]:
        test[column] = pd.to_numeric(
            test[column], errors="coerce"
        )

    historical = historical.dropna().sort_values("Month")
    forecast = forecast.dropna().sort_values("Month")
    test = test.dropna().sort_values("Month")

    return historical, forecast, test


# =========================================================
# LOAD AND VALIDATE
# =========================================================

st.title("📈 EV Registration Forecast Dashboard")

st.caption(
    "India Electric Vehicle Market | Historical Analysis "
    "and Predictive Forecasting"
)

required_files = [
    HISTORICAL_FILE,
    FORECAST_FILE,
    TEST_FILE
]

missing_files = [
    str(file) for file in required_files
    if not file.exists()
]

if missing_files:
    st.error("Required forecast files are missing:")
    for file in missing_files:
        st.write(file)
    st.stop()

try:
    historical, forecast, test = load_forecast_data()

except Exception as error:
    st.error(f"Error loading forecast data: {error}")
    st.stop()


if historical.empty or forecast.empty or test.empty:
    st.error("One or more forecast datasets contain no usable records.")
    st.stop()


# =========================================================
# DATA VALIDATION
# =========================================================

required_historical = {
    "Month", "EV_Registrations"
}

required_forecast = {
    "Month", "Predicted_EV_Registrations"
}

required_test = {
    "Month",
    "Actual_EV_Registrations",
    "Linear_Regression",
    "Holt",
    "Fixed_Origin_Naive",
    "Random_Forest"
}

if not required_historical.issubset(historical.columns):
    st.error("Historical CSV columns do not match the expected format.")
    st.stop()

if not required_forecast.issubset(forecast.columns):
    st.error("Forecast CSV columns do not match the expected format.")
    st.stop()

if not required_test.issubset(test.columns):
    st.error("Test prediction CSV columns do not match the expected format.")
    st.stop()


# =========================================================
# MODEL PERFORMANCE DATA
# =========================================================

model_performance = pd.DataFrame({
    "Model": [
        "Linear Regression",
        "Holt",
        "Naive",
        "Random Forest"
    ],
    "MAPE": [
        7.24,
        13.18,
        13.68,
        20.62
    ]
})


# =========================================================
# KPI CALCULATIONS
# =========================================================

latest_actual = int(
    historical.iloc[-1]["EV_Registrations"]
)

latest_actual_month = historical.iloc[-1]["Month"].strftime(
    "%b %Y"
)

final_forecast = int(
    forecast.iloc[-1]["Predicted_EV_Registrations"]
)

forecast_month = forecast.iloc[-1]["Month"].strftime(
    "%b %Y"
)

forecast_growth = (
    (final_forecast / latest_actual) - 1
) * 100

best_mape = model_performance["MAPE"].min()


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("Forecast Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Latest Actual Registrations",
        f"{latest_actual:,}",
        latest_actual_month
    )

with col2:
    st.metric(
        f"{forecast_month} Forecast",
        f"{final_forecast:,}"
    )

with col3:
    st.metric(
        "Forecast Growth",
        f"{forecast_growth:.2f}%",
        "vs latest actual"
    )

with col4:
    st.metric(
        "Best Model MAPE",
        f"{best_mape:.2f}%"
    )


st.divider()


# =========================================================
# HISTORICAL VS FORECAST
# =========================================================

st.subheader("India EV Registrations – Historical vs Forecast")

fig_combined = go.Figure()

fig_combined.add_trace(
    go.Scatter(
        x=historical["Month"],
        y=historical["EV_Registrations"],
        mode="lines+markers",
        name="Historical Registrations",
        line=dict(width=3)
    )
)

# Connect forecast line to the last historical observation
forecast_dates = pd.concat([
    historical[["Month"]].tail(1),
    forecast[["Month"]]
], ignore_index=True)

forecast_values = pd.concat([
    historical[["EV_Registrations"]].tail(1).rename(
        columns={"EV_Registrations": "Predicted_EV_Registrations"}
    ),
    forecast[["Predicted_EV_Registrations"]]
], ignore_index=True)

fig_combined.add_trace(
    go.Scatter(
        x=forecast_dates["Month"],
        y=forecast_values["Predicted_EV_Registrations"],
        mode="lines+markers",
        name="Forecast Registrations",
        line=dict(width=3, dash="dash")
    )
)

fig_combined.update_layout(
    template="plotly_dark",
    height=430,
    hovermode="x unified",
    yaxis_title="EV Registrations",
    xaxis_title="Month",
    legend=dict(orientation="h", y=1.12),
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(
    fig_combined,
    use_container_width=True
)


# =========================================================
# SIX MONTH FORECAST CHART
# =========================================================

st.subheader("Six-Month EV Registration Forecast")

fig_forecast = px.bar(
    forecast,
    x="Month",
    y="Predicted_EV_Registrations",
    text="Predicted_EV_Registrations",
    title="Monthly Predicted EV Registrations",
)

fig_forecast.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig_forecast.update_layout(
    template="plotly_dark",
    height=380,
    xaxis_title="Forecast Month",
    yaxis_title="Predicted Registrations",
    showlegend=False,
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(
    fig_forecast,
    use_container_width=True
)


# =========================================================
# MODEL PERFORMANCE COMPARISON
# =========================================================

st.subheader("Predictive Model Performance Comparison")

fig_models = px.bar(
    model_performance.sort_values(
        "MAPE", ascending=True
    ),
    x="MAPE",
    y="Model",
    orientation="h",
    text="MAPE",
    title="Test MAPE – Lower is Better"
)

fig_models.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_models.update_layout(
    template="plotly_dark",
    height=350,
    xaxis_title="MAPE (%)",
    yaxis_title="Model",
    showlegend=False,
    margin=dict(l=20, r=60, t=50, b=20)
)
fig_models.update_yaxes(
    categoryorder="array",
    categoryarray=[
        "Random Forest",
        "Naive",
        "Holt",
        "Linear Regression"
    ]
)

st.plotly_chart(
    fig_models,
    use_container_width=True
)


# =========================================================
# ACTUAL VS PREDICTED TEST PERIOD
# =========================================================

st.subheader("Actual vs Predicted – Test Period")

fig_test = go.Figure()

fig_test.add_trace(
    go.Scatter(
        x=test["Month"],
        y=test["Actual_EV_Registrations"],
        mode="lines+markers",
        name="Actual Registrations",
        line=dict(width=3)
    )
)

fig_test.add_trace(
    go.Scatter(
        x=test["Month"],
        y=test["Linear_Regression"],
        mode="lines+markers",
        name="Linear Regression",
        line=dict(width=3, dash="dash")
    )
)

fig_test.update_layout(
    template="plotly_dark",
    height=380,
    xaxis_title="Test Month",
    yaxis_title="EV Registrations",
    hovermode="x unified",
    margin=dict(l=20, r=20, t=30, b=20)
)

st.plotly_chart(
    fig_test,
    use_container_width=True
)


# =========================================================
# FORECAST TABLE
# =========================================================

st.subheader("Monthly Forecast Details")

display_forecast = forecast.copy()

display_forecast["Month"] = (
    display_forecast["Month"].dt.strftime("%B %Y")
)

display_forecast["Predicted_EV_Registrations"] = (
    display_forecast["Predicted_EV_Registrations"]
    .round()
    .astype(int)
)

display_forecast = display_forecast.rename(
    columns={
        "Month": "Forecast Month",
        "Predicted_EV_Registrations": "Predicted EV Registrations"
    }
)

st.dataframe(
    display_forecast.style.format({
        "Predicted EV Registrations": "{:,.0f}"
    }),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# DOWNLOAD FORECAST
# =========================================================

csv_data = forecast.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Forecast CSV",
    data=csv_data,
    file_name="EV_Registration_6_Month_Forecast.csv",
    mime="text/csv"
)


# =========================================================
# TEST PREDICTION DETAILS
# =========================================================

with st.expander("View Model Test Predictions"):

    test_display = test.copy()

    test_display["Month"] = (
        test_display["Month"].dt.strftime("%B %Y")
    )

    st.dataframe(
        test_display,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# METHODOLOGY AND LIMITATIONS
# =========================================================

with st.expander("Forecast Methodology & Limitations"):

    st.markdown("""
    **Selected Model:** Linear Regression

    **Model Evaluation:**
    - MAE: 23,079.80
    - RMSE: 24,767.54
    - MAPE: 7.24%

    **Training Period:** April 2025 – May 2026

    **Testing Period:** June 2026 – September 2026

    **Forecast Period:** October 2026 – March 2027

    **Important Limitations:**
    - The model is based on a limited historical dataset.
    - Test evaluation covers only four months.
    - Forecasts are experimental estimates, not guaranteed outcomes.
    - Forecast uncertainty can increase over the prediction horizon.
    - October 2026 historical registrations were excluded because
      source data completeness was uncertain.
    """)


# =========================================================
# DATA SOURCE
# =========================================================

st.caption(
    "EV Intelligence | Data source: Processed VAHAN monthly "
    "registration dataset and project forecasting outputs."
)
