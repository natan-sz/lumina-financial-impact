import streamlit as st

# --- Brand styling ---
st.markdown("""
    <style>
    /* Universal button style for Streamlit */
    button[kind="primary"], button[kind="secondary"], div.stButton > button {
        background-color: #03180c !important;
        color: #fff !important;
        border: 2px solid #03180c !important;
        border-radius: 8px !important;
        padding: 0.5em 1.5em !important;
        font-size: 1.1em !important;
        font-weight: 600 !important;
        box-shadow: none !important;
        background-image: none !important;
    }
    button[kind="primary"]:hover, button[kind="secondary"]:hover, div.stButton > button:hover {
        background-color: #175135 !important;
        color: #fff !important;
        border: 2px solid #175135 !important;
    }
    /* Remove extra black background in some themes */
    button:focus:not(:active) {
        outline: 2px solid #03180c !important;
        outline-offset: 2px !important;
        background-color: #03180c !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- State Management ---
if "show_costs" not in st.session_state:
    st.session_state["show_costs"] = False
if "savings_mode" not in st.session_state:
    st.session_state["savings_mode"] = None

# --- Intro Copy ---
st.image("lumina.webp",width=200)
st.title("Lumina Pilot Partner Financial Impact Calculator")
st.markdown("""
Exhaustion, loss of cognition and disengagement are silent drainers on productivity, but do you know just how much it could be costing your company?

Using our science-based research and knowledge, we have built this calculator to help you estimate the potential annual savings from using Lumina to reduce burnout-related costs in your company.
""")

st.markdown("---")
st.subheader("Step one: Please enter your organisation's information")

with st.form("inputs_form"):
    num_employees = st.number_input("Total number of employees", min_value=1, value=1500, key='num_employees')
    burnout_risk_pct = st.select_slider(
        "Est % risk of burnout",
        options=[5, 10, 15, 20, 25],
        value=10,
        key='burnout_risk_pct'
    )
    avg_salary = st.number_input("Avg employee salary (£)", min_value=10000, value=50000, step=1000 , key='avg_salary')
    avg_daily_absence_cost = st.number_input("Avg daily cost of absence (inc lost productivity)", min_value=50, value=150, key='avg_daily_absence_cost')
    next_step = st.form_submit_button("Calculate Burnout Costs (without Lumina)")

if next_step:
    st.session_state["show_costs"] = True
    st.session_state["savings_mode"] = None  # reset if coming back

if st.session_state["show_costs"]:
    # --- Costs Calculation ---
    employees_at_risk = num_employees * burnout_risk_pct / 100
    days_lost_per_burnout = 27.5
    burnout_leavers = 5
    cost_per_replacement = 50000

    absenteeism_cost = employees_at_risk * days_lost_per_burnout * avg_daily_absence_cost
    presenteeism_cost = 1.5 * absenteeism_cost
    turnover_cost = burnout_leavers * cost_per_replacement

    st.markdown("### Potential Costs (Annual, without Lumina)")
    st.write(f"**Absenteeism:** £{absenteeism_cost:,.0f}")
    st.write(f"**Presenteeism:** £{presenteeism_cost:,.0f}")
    st.write(f"**Burnout-related turnover:** £{turnover_cost:,.0f}")
    st.write(f"**Recruitment/Training costs avoided:** —")
    st.success("Now, let's estimate the potential savings with Lumina.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Conservative Savings (Lower Estimate)", key='cons_btn'):
            st.session_state["savings_mode"] = "conservative"
    with col2:
        if st.button("Aggressive Savings (Higher Estimate)", key='agg_btn'):
            st.session_state["savings_mode"] = "aggressive"

    # --- Savings Section ---
    if st.session_state["savings_mode"] in ("conservative", "aggressive"):
        conservative = st.session_state["savings_mode"] == "conservative"
        absenteeism_pct = 0.2 if conservative else 0.4
        presenteeism_pct = 0.1 if conservative else 0.2
        prevented_hires = 5 if conservative else 10
        recruitment_saving = 25000 if conservative else 50000
        lumina_cost_pppm = 4
        annual_lumina_cost = num_employees * lumina_cost_pppm * 12

        absenteeism_saved = absenteeism_cost * absenteeism_pct
        presenteeism_saved = presenteeism_cost * presenteeism_pct
        turnover_saved = prevented_hires * cost_per_replacement
        recruitment_saved = recruitment_saving
        total_savings = absenteeism_saved + presenteeism_saved + turnover_saved + recruitment_saved

        roi = (total_savings - annual_lumina_cost) / annual_lumina_cost if annual_lumina_cost else 0

        st.markdown("### Potential Lumina Savings")
        st.write(f"**Absenteeism (saved):** £{absenteeism_saved:,.0f}")
        st.write(f"**Presenteeism (saved):** £{presenteeism_saved:,.0f}")
        st.write(f"**Burnout-related turnover (saved):** £{turnover_saved:,.0f}")
        st.write(f"**Recruitment/Training costs avoided:** £{recruitment_saved:,.0f}")
        st.write(f"**Annual Lumina cost:** £{annual_lumina_cost:,.0f}")
        st.write(f"**Total Estimated Savings:** £{total_savings:,.0f}")
        st.write(f"**Lumina ROI:** {roi:.2f}")

        st.success("This is your estimated annual financial impact from tackling burnout with Lumina.")

