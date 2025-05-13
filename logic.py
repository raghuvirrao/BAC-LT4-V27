import numpy as np
import plotly.graph_objects as go

def predict_duration(age, fc, util, mro_region, aircraft_type):
    return 18  # Static placeholder (already user-controlled)

def calculate_costs(duration, lease_rate, lost_revenue_per_hour, avg_daily_util, labor_rate, aircraft_bin):
    lost_revenue = lost_revenue_per_hour * avg_daily_util * duration
    lease_cost = (lease_rate / 30) * duration
    labor_hours = duration * 10  # assume 10 labor hours per day of MRO
    labor_cost = labor_hours * labor_rate
    material_cost = 0.3 * labor_cost

    # --- Residual Value Loss based on vintage bin ---
    aircraft_value = 60_000_000  # USD (half-life)
    k_lookup = {
        "New (0–5 yrs)": 0.05,
        "Mid-life (6–15 yrs)": 0.08,
        "Old (15+ yrs)": 0.12
    }
    max_loss_lookup = {
        "New (0–5 yrs)": 0.04,
        "Mid-life (6–15 yrs)": 0.03,
        "Old (15+ yrs)": 0.02
    }
    k = k_lookup[aircraft_bin]
    max_loss = max_loss_lookup[aircraft_bin]
    residual_loss = aircraft_value * max_loss * (1 - np.exp(-k * duration))

    net_impact = lost_revenue + lease_cost + labor_cost + material_cost + residual_loss

    return {
        "lost_revenue": lost_revenue,
        "lease_cost": lease_cost,
        "labor_cost": labor_cost,
        "material_cost": material_cost,
        "residual_loss": residual_loss,
        "net_impact": net_impact
    }

def plot_cost_breakdown(costs):
    fig = go.Figure(data=[go.Pie(
        labels=["Lost Revenue", "Lease Cost", "Labor", "Materials", "Residual Value Loss"],
        values=[
            costs['lost_revenue'],
            costs['lease_cost'],
            costs['labor_cost'],
            costs['material_cost'],
            costs['residual_loss']
        ],
        hole=0.4
    )])
    fig.update_traces(textinfo='label+percent', pull=[0.1, 0.1, 0.05, 0.05, 0.05])
    return fig

def plot_residual_value_decay(aircraft_bin):
    k_lookup = {
        "New (0–5 yrs)": 0.05,
        "Mid-life (6–15 yrs)": 0.08,
        "Old (15+ yrs)": 0.12
    }
    max_loss_lookup = {
        "New (0–5 yrs)": 0.04,
        "Mid-life (6–15 yrs)": 0.03,
        "Old (15+ yrs)": 0.02
    }
    aircraft_value = 60_000_000
    k = k_lookup[aircraft_bin]
    max_loss = max_loss_lookup[aircraft_bin]

    x = np.arange(0, 60)
    y = aircraft_value * max_loss * (1 - np.exp(-k * x))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name="Residual Loss Curve"))
    fig.update_layout(title="Residual Value Loss vs MRO Downtime", xaxis_title="Downtime (Days)", yaxis_title="Residual Value Loss (USD)")
    return fig

def plot_regional_comparison():
    regions = ["Middle East", "East Asia", "SE Asia", "USA"]
    durations = [14, 18, 22, 19]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=regions, y=durations, text=durations, textposition='auto'))
    fig.update_layout(title="Benchmark MRO Duration by Region", xaxis_title="Region", yaxis_title="Avg MRO TAT (days)")
    return fig

def stakeholder_insights(stakeholder, costs, duration):
    insights = []

    if stakeholder == "Airline":
        if costs['lost_revenue'] > costs['lease_cost']:
            insights.append("Revenue losses due to downtime exceed lease losses—focus on uptime.")
        if duration < 15:
            insights.append("Predicted downtime is significantly lower than regional average.")
        insights.append("Prioritise MROs with faster TAT to preserve seat revenue.")

    elif stakeholder == "Lessor":
        insights.append(f"Residual value risk is ${costs['residual_loss']:,.0f} due to {duration} day grounding.")
        if costs['lease_cost'] > 20000:
            insights.append("Significant lease cost loss due to idle aircraft.")
        insights.append("Quick turnaround enhances long-term asset value.")

    elif stakeholder == "Financier":
        roi = (costs['lost_revenue'] + costs['lease_cost']) / costs['net_impact']
        insights.append(f"Operational ROI based on downtime is approximately {roi:.2%}.")
        insights.append("Residual value loss is amortizable across remaining lease horizon.")
        if costs['net_impact'] > 1000000:
            insights.append("Consider risk hedging on high-value asset exposure.")

    elif stakeholder == "MRO Provider":
        insights.append("Predicted TAT is lower than regional peers—competitive edge.")
        insights.append(f"Average labor cost per day: ${costs['labor_cost']/duration:,.0f}")
        insights.append("Scope to reduce material markup by efficient procurement.")

    return insights
