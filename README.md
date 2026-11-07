# ⚡ EV Intelligence – India's Electric Vehicle Market & Charging Infrastructure Analytics

<p align="center">
  <a href="https://ev-intelligence-india.streamlit.app/">
    <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Open Streamlit App">
  </a>
</p>

<p align="center">
  **An end-to-end data analytics and predictive intelligence project exploring India's electric vehicle market, registration trends, charging infrastructure and future EV registration patterns.**
</p>

---

## 🚀 Live Dashboard

**Streamlit Application:**  
👉 https://ev-intelligence-india.streamlit.app/

**GitHub Repository:**  
https://github.com/harshit1017kaushik-create/EV-Intelligence-India

---

## 📌 Project Overview

EV Intelligence is an end-to-end analytics project designed to understand the growth of India's electric vehicle ecosystem and evaluate the distribution of its charging infrastructure.

The project combines data collection, data cleaning, exploratory data analysis, SQL-based analysis, business intelligence dashboards and predictive modelling to transform raw datasets into meaningful insights.

### Key Business Questions

- How rapidly are EV registrations growing in India?
- Which states have the highest EV registrations?
- How is charging infrastructure distributed across states?
- Which charging operators have the largest infrastructure presence?
- Which states show higher preliminary infrastructure pressure?
- What could India's monthly EV registrations look like over the next six months?

## 🎯 Project Objectives

- Analyze historical EV registration trends across India.
- Evaluate state-wise EV registrations and charging infrastructure.
- Understand charging station ownership, operators and power categories.
- Identify states requiring further infrastructure assessment.
- Develop a six-month EV registration forecasting model.
- Build interactive Power BI and Streamlit dashboards.
- Deploy the application using cloud infrastructure.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Database | MySQL |
| Cloud Database | Aiven MySQL |
| Business Intelligence | Microsoft Power BI |
| Interactive Dashboard | Streamlit |
| Machine Learning | Scikit-learn |
| Forecasting | Linear Regression, Holt, Naive, Random Forest |
| Development | Google Colab, Python IDLE, MySQL Workbench |
| Version Control | Git and GitHub |
| Deployment | Streamlit Community Cloud |

## 📂 Project Structure

```text
EV-Intelligence-India/
│
├── App/
│   ├── Home.py
│   ├── utils/
│   │   ├── database.py
│   │   └── charts.py
│   │
│   ├── pages/
│   │   ├── 1_EV_Market.py
│   │   ├── 2_Charging_Infrastructure.py
│   │   ├── 3_State_Analysis.py
│   │   └── 4_EV_Forecast.py
│   │
│   └── .streamlit/
│
├── Data/
│   └── Forecast Data/
│
├── Models/
│
├── Notebooks/
│   ├── EV_Intelligence_Data_Cleaning.ipynb
│   ├── EV_Intelligence_Dataset_03.ipynb
│   └── EV_Intelligence_Predictive_Analytics.ipynb
│
├── Reports/
│   └── EV_Intelligence_Dashboard.pbix
│
├── SQL/
│   ├── 15_State_Wise_EV_Infrastructure_Analysis.sql
│   ├── 16_Create_State_Infrastructure_View.sql
│   ├── 17_Create_Annual_EV_Growth_View.sql
│   ├── 18_Create_Monthly_EV_Trends_View.sql
│   ├── 19_Create_Operator_Analysis_View.sql
│   ├── 20_Create_Charging_Power_Analysis_View.sql
│   └── 21_Create_State_Infrastructure_Gap_View.sql
│
├── .gitignore
├── requirements.txt
└── README.md
```

## 📊 Project Modules

### 1. EV Market Analysis

- Annual EV registration trends (2020–2026).
- Year-over-year growth analysis.
- Monthly registration trends.
- Month-over-month growth analysis.

### 2. Charging Infrastructure Analysis

- Charging station distribution.
- Operator-wise infrastructure analysis.
- Government vs private ownership.
- Charging power category distribution.
- State-wise charging infrastructure comparison.

### 3. State-Wise Analysis

- State-wise EV registrations.
- Charging stations and charger distribution.
- EVs-per-charger comparison.
- Registration vs charging infrastructure analysis.
- Preliminary infrastructure gap scoring.

### 4. EV Registration Forecast

- Historical vs forecast registration trends.
- Model performance comparison.
- Actual vs predicted test-period registrations.
- Six-month forecast visualization.
- Forecast details and methodology.

## 🧠 Predictive Analytics

Four forecasting approaches were evaluated:

- Linear Regression
- Holt's Exponential Smoothing
- Fixed-Origin Naive Forecast
- Random Forest Regression

### Model Performance Comparison

| Model | Test MAPE |
|---|---:|
| Linear Regression | **7.24%** |
| Holt | 13.18% |
| Naive | 13.68% |
| Random Forest | 20.62% |

**Selected Model: Linear Regression**

| Evaluation Metric | Result |
|---|---:|
| MAPE | 7.24% |
| RMSE | 24,767.54 |
| MAE | 23,079.80 |
| Test Months | 4 |

### Six-Month EV Registration Forecast

| Forecast Month | Predicted Registrations |
|---|---:|
| October 2026 | 358,615 |
| November 2026 | 361,620 |
| December 2026 | 383,958 |
| January 2027 | 402,900 |
| February 2027 | 414,146 |
| March 2027 | 431,248 |

The forecast is experimental and uses recursive predictions. Forecast uncertainty may increase over the prediction horizon. Model performance is based on a limited four-month test period.

## 🗄️ SQL Database & Analysis

**Database:** `ev_intelligence`

### Database Tables

- `ev_charging_stations`
- `ev_registrations_annual`
- `ev_registrations_statewise`
- `ev_registrations_monthly`

### Analytical SQL Views

- `vw_state_ev_infrastructure`
- `vw_annual_ev_growth`
- `vw_monthly_ev_trends`
- `vw_operator_analysis`
- `vw_charging_power_analysis`
- `vw_state_infrastructure_gap`
- `vw_ev_station_map`
- `vw_ownership_analysis`

### SQL Scripts Included

| SQL File | Purpose |
|---|---|
| `15_State_Wise_EV_Infrastructure_Analysis.sql` | State-wise infrastructure analysis |
| `16_Create_State_Infrastructure_View.sql` | Creates state infrastructure view |
| `17_Create_Annual_EV_Growth_View.sql` | Creates annual EV growth view |
| `18_Create_Monthly_EV_Trends_View.sql` | Creates monthly EV trends view |
| `19_Create_Operator_Analysis_View.sql` | Creates operator analysis view |
| `20_Create_Charging_Power_Analysis_View.sql` | Creates charging power analysis view |
| `21_Create_State_Infrastructure_Gap_View.sql` | Creates infrastructure gap view |

## 📈 Power BI Dashboard

The Power BI report is available in:

`Reports/EV_Intelligence_Dashboard.pbix`

It contains six analytical pages:

1. EV Market Overview
2. State-Wise Analysis
3. Charging Infrastructure
4. Infrastructure Gap Analysis
5. EV Registration Forecast
6. EV Forecast Performance

The report includes KPI cards, trend analysis, comparisons, interactive filters, maps and predictive performance visualizations.

## 📓 Jupyter Notebooks

The `Notebooks` folder contains three notebooks:

| Notebook | Purpose |
|---|---|
| `EV_Intelligence_Data_Cleaning.ipynb` | Data preparation and cleaning |
| `EV_Intelligence_Dataset_03.ipynb` | EV dataset analysis and exploration |
| `EV_Intelligence_Predictive_Analytics.ipynb` | Predictive modelling and forecasting |

## 📚 Data Sources

- **EV Registration Data:** VAHAN-based registration data covering 2020–October 2026.
- **Charging Infrastructure Data:** EV Charging Stations API dataset, representing a third-party snapshot dated 26 October 2025.

The 2026 registration figures are year-to-date and should not be interpreted as full-year totals.

## ⚠️ Data & Methodology Limitations

- Charging infrastructure data represents a historical snapshot, not a live government feed.
- Suspect geographic records are flagged and excluded from the validated station map.
- EVs-per-charger is a comparative screening indicator, not definitive evidence of infrastructure shortage.
- Infrastructure gap scores are preliminary screening rankings.
- Charging power categories use project-defined thresholds.
- Forecast results are experimental and should not be treated as guaranteed future registrations.
- Correlations and observed relationships do not establish causation.

## ☁️ Deployment

The interactive Streamlit application is deployed using Streamlit Community Cloud.

Cloud database connectivity is provided through Aiven MySQL.

Database credentials are configured using Streamlit Secrets and are not stored in this repository.

## 👨‍💻 Author

**Harshit Kaushik**

B.Tech – Computer Science and Engineering

Interested in Data Analytics, Python, SQL, Business Intelligence and Predictive Analytics.

**GitHub:** https://github.com/harshit1017kaushik-create

---

## ⭐ Project Highlights

- End-to-end data analytics workflow.
- Python-based data cleaning and exploratory analysis.
- MySQL database design and analytical views.
- Interactive Power BI dashboards.
- Machine learning-based forecasting.
- Cloud-hosted Streamlit application.
- Aiven cloud database integration.

**Explore the live dashboard and the complete project repository!**
