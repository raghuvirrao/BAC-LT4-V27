import streamlit as st
import pandas as pd
import numpy as np
from logic import (
    predict_duration,
    calculate_costs,
    stakeholder_insights,
    plot_cost_breakdown,
    plot_residual_value_decay,
    plot_regional_comparison,
)

st.set_page_config(page_title=✈️ MRO Dashboard", layout="wide")

st.title("✈️ MRO Duration & Economic Impact Dashboard")

st.markdown("---")

# --- SIDEBAR INPUTS ---
st.sidebar.header("📌 Aircraft & Maintenance Inputs")

aircraft_age = st.sidebar.slider("Aircraft Age (Years)", 0, 30, 10)
cumulative_fc = st.sidebar.number_input("Cumulative Flight Cycles", value=12000)
avg_daily_util = st.sidebar.slider("Average Daily Utilisation (hrs)", 1.0, 16.0, 12.0)
predicted_duration = st.sidebar.slider("Predicted MRO Duration (Days)", 7, 60, 18)
aircraft_bin = st.sidebar.selectbox("Aircraft Vintage Bin", ["New (0–5 yrs)", "Mid-life (6–15 yrs)", "Old (15+ yrs)"])
mro_region = st.sidebar.selectbox("MRO Region", ["Middle East", "East Asia", "SE Asia", "USA"])

st.markdown("### Stakeholder-Specific Views")
stakeholder = st.selectbox("Choose Stakeholder Perspective", ["Airline", "Lessor", "Financier", "MRO Provider"])

# --- ADVANCED FINANCIAL INPUTS ---
with st.expander("💰 Financial Parameters", expanded=False):
    lease_rate = st.number_input("Monthly Lease Rate (USD)", value=35000)
    lost_rev_per_hour = st.number_input("Lost Revenue per Flight Hour (USD)", value=21180.77)
    labor_rate_region = {
        "Middle East": 95,
        "East Asia": 105,
        "SE Asia": 75,
        "USA": 130
    }
    labor_rate = labor_rate_region.get(mro_region, 100)

# --- DURATION SECTION ---
st.subheader("🛠️ Predicted MRO Duration")
st.success(f"✈️ Estimated MRO Duration: **{predicted_duration} days**")
st.markdown(f"""
- Based on: `{aircraft_age}` years | `{avg_daily_util}` hrs/day | `{mro_region}` MRO
- Predicted using interaction effects and stakeholder-adjusted decay logic
""")

# --- ECONOMIC IMPACT ---
st.subheader("💸 Cost-Benefit Analysis (CBA)")
costs = calculate_costs(
    duration=predicted_duration,
    lease_rate=lease_rate,
    lost_revenue_per_hour=lost_rev_per_hour,
    avg_daily_util=avg_daily_util,
    labor_rate=labor_rate,
    aircraft_bin=aircraft_bin
)

st.markdown(f"""
**Estimated Lost Revenue:** ${costs['lost_revenue']:,.0f}  
**Lease Cost (Downtime):** ${costs['lease_cost']:,.0f}  
**Maintenance Labor Cost:** ${costs['labor_cost']:,.0f}  
**Material Cost (30% of labor):** ${costs['material_cost']:,.0f}  
**Residual Value Loss:** ${costs['residual_loss']:,.0f}  

### ✅ Net Economic Impact: ${costs['net_impact']:,.0f}
""")

# --- CHARTS & VISUAL INSIGHTS ---
st.subheader("📊 Visual Insights")

st.plotly_chart(plot_cost_breakdown(costs), use_container_width=True)
st.markdown("**Figure:** Breakdown of key cost contributors.")

st.plotly_chart(plot_residual_value_decay(aircraft_bin), use_container_width=True)
st.markdown("**Figure:** Residual value loss increases exponentially with prolonged downtime.")

st.plotly_chart(plot_regional_comparison(), use_container_width=True)
st.markdown("**Figure:** Benchmark MRO turnaround durations by region (industry average).")

# --- STAKEHOLDER INSIGHT BULLETS ---
st.subheader(f"🧠 Insights for {stakeholder}")
bullets = stakeholder_insights(stakeholder, costs, predicted_duration)
for bullet in bullets:
    st.markdown(f"- {bullet}")
