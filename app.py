import streamlit as st

st.title("Burnout ROI & Savings Calculator")

st.header("Input Metrics")
num_employees = st.number_input("Total number of employees", min_value=1, value=1500)
burnout_risk_pct = st.slider("Estimated % at risk of burnout", min_value=0, max_value=100, value=10)
avg_salary = st.number_input("Average employee salary (£)", min_value=0, value=50000)
avg_daily_absence_cost = st.number_input("Average daily cost of absence (£)", min_value=0, value=200)
burnout_leavers = st.number_input("Burnout-related leavers per year", min_value=0, value=5)
days_lost_per_burnout = st.number_input("Days lost per burnout-affected employee per year", min_value=0.0, value=27.5)
cost_per_replacement = st.number_input("Cost per replacement (£)", min_value=0, value=50000)
prevented_hires_low = st.number_input("Prevented hires (low)", min_value=0, value=5)
prevented_hires_high = st.number_input("Prevented hires (high)", min_value=0, value=10)
annual_lumina_cost = st.number_input("Annual Lumina Cost (£)", min_value=0, value=1500*6*12//12)  # £6/employee/month

st.header("Calculated Outputs")

# Calculations
employees_at_risk = num_employees * burnout_risk_pct / 100
absenteeism_cost = employees_at_risk * days_lost_per_burnout * avg_daily_absence_cost
presenteeism_cost = 1.5 * absenteeism_cost
turnover_cost = burnout_leavers * cost_per_replacement

recruitment_training_savings_low = 25000
recruitment_training_savings_high = 50000

# Conservative (low) savings
conservative_savings = (
    0.2 * absenteeism_cost +
    0.1 * presenteeism_cost +
    prevented_hires_low * cost_per_replacement +
    recruitment_training_savings_low
)

# Aggressive (high) savings
aggressive_savings = (
    0.4 * absenteeism_cost +
    0.2 * presenteeism_cost +
    prevented_hires_high * cost_per_replacement +
    recruitment_training_savings_high
)

# Annual cost = £6 per employee per month × 12 months
annual_lumina_cost = num_employees * 6 * 12

roi_conservative = conservative_savings / annual_lumina_cost if annual_lumina_cost else 0
roi_aggressive = aggressive_savings / annual_lumina_cost if annual_lumina_cost else 0

def fmt(x):
    return f"£{x:,.0f}" if isinstance(x, (int, float)) else x

# Show the output table
st.write("### Metrics")
st.table([
    ["Employees at risk", f"{employees_at_risk:,.0f}"],
    ["Absenteeism Cost", fmt(absenteeism_cost)],
    ["Presenteeism Cost", fmt(presenteeism_cost)],
    ["Turnover Cost", fmt(turnover_cost)],
    ["Recruitment/Training Savings (low)", fmt(recruitment_training_savings_low)],
    ["Recruitment/Training Savings (high)", fmt(recruitment_training_savings_high)],
    ["Conservative Savings", fmt(conservative_savings)],
    ["Aggressive Savings", fmt(aggressive_savings)],
    ["Annual Lumina Cost", fmt(annual_lumina_cost)],
    ["ROI (Conservative)", f"{roi_conservative:.2f}"],
    ["ROI (Aggressive)", f"{roi_aggressive:.2f}"],
])

st.caption("All calculations based on your input values above.")
