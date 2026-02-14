import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import warnings

# 1. SYSTEM HYGIENE
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# ==========================================
# CONFIGURATION
# ==========================================
st.set_page_config(page_title="STC Leadership Dashboard 2025", layout="wide")
np.random.seed(42) 

COLOR_RED, COLOR_AMBER, COLOR_GREEN = "#FF4B4B", "#FFA500", "#09AB3B"
PROJECT_START = datetime(2025, 5, 1)
SNAPSHOT_DATE = datetime(2025, 7, 20) 

# ==========================================
# DATA ENGINE (FROZEN SCENARIO)
# ==========================================
@st.cache_data
def generate_frozen_data():
    # --- PAGE 1 DATA (LOCKED) ---
    weeks = pd.date_range(start=PROJECT_START, end=SNAPSHOT_DATE, freq='W')
    spi_values = [0.40, 0.45, 0.42, 0.50, 0.55, 0.48, 0.52, 0.65, 0.78, 0.82, 0.85]
    df_trend = pd.DataFrame({'Week': weeks[:len(spi_values)], 'SPI': spi_values})

    tasks = [
        {"ID": "2025-074", "Task": "Configure VAT Rules", "Workstream": "Finance", "Owner": "Antonio", "Planned": 10, "Actual": 22, "Group": "Ongoing / Delayed"},
        {"ID": "2025-081", "Task": "Student Master Migration", "Workstream": "Lifecycle", "Owner": "Mateo", "Planned": 12, "Actual": 14, "Group": "Ongoing / Delayed"},
        {"ID": "2025-085", "Task": "Fuel Tracker API", "Workstream": "Fleet", "Owner": "Francesco", "Planned": 8, "Actual": 9, "Group": "Ongoing / Delayed"},
        {"ID": "2025-088", "Task": "Regional Tax Calc", "Workstream": "Finance", "Owner": "Valentina", "Planned": 15, "Actual": 16, "Group": "Ongoing / Delayed"},
        {"ID": "2025-090", "Task": "Shift Planning Fixes", "Workstream": "Instructor", "Owner": "Enzo", "Planned": 5, "Actual": 5, "Group": "Completed This Week"},
        {"ID": "2025-092", "Task": "Enrollment Design", "Workstream": "Lifecycle", "Owner": "Camila", "Planned": 7, "Actual": 7, "Group": "Completed This Week"}
    ]
    df_tasks = pd.DataFrame(tasks)
    df_tasks['SPI'] = (df_tasks['Planned'] / df_tasks['Actual']).round(2)
    df_tasks['Days Taken'] = df_tasks['Actual']
    df_tasks['Variance (Days)'] = df_tasks['Actual'] - df_tasks['Planned']
    
    # --- PAGE 2 DATA (RESTORED 3-CHART LAYOUT) ---
    sizing_data = {'Size': ['S', 'M', 'L', 'XL'], 'Count': [45, 62, 28, 15]}
    df_sizes = pd.DataFrame(sizing_data)

    WORKSTREAMS = ['Student Lifecycle', 'Fleet Management', 'Instructor Scheduling', 'Exam Booking (App)', 'Finance & Regulatory']
    sprints = []
    for s_num in range(1, 9):
        for ws in WORKSTREAMS:
            if s_num <= 2: 
                vel = np.random.uniform(0.58, 0.65)
                lag = np.random.uniform(22, 26)
            elif s_num <= 4: 
                vel = np.random.uniform(0.78, 0.88)
                lag = np.random.uniform(12, 18)
            else: 
                vel = np.random.uniform(0.92, 1.0)
                lag = np.random.uniform(2, 5)
            sprints.append({'Sprint': f"Sprint {s_num}", 'Workstream': ws, 'Velocity': round(vel, 2), 'Lag': round(lag, 1)})
    df_sprints = pd.DataFrame(sprints)

    # --- PAGE 3 DATA (CORRECTED: SPREAD RIGHT, LESS RED) ---
    defects = []
    for i in range(1, 66):
        # 1. Spread bullets further right (0 to 85 days) to fill the chart
        days_offset = np.random.randint(0, 85)
        rep_date = PROJECT_START + timedelta(days=days_offset)
        
        # 2. Less Red (Only 15% Critical, mixed with High/Medium)
        sev = np.random.choice(['Critical', 'High', 'Medium'], p=[0.15, 0.35, 0.50])
        
        # Resolution Speed Logic (Maintained: Early=Slow, Late=Fast)
        if rep_date < datetime(2025, 6, 15):
            res_days = np.random.randint(10, 25) 
        else:
            res_days = np.random.randint(1, 5)   
            
        defects.append({
            'ID': f'DEF-{i:03d}', 
            'Date': rep_date, 
            'Severity': sev, 
            'Resolution_Days': res_days,
            'Workstream': np.random.choice(WORKSTREAMS)
        })
    df_defects = pd.DataFrame(defects)

    return df_trend, df_tasks, df_sizes, df_sprints, df_defects

df_trend, df_tasks, df_sizes, df_sprints, df_defects = generate_frozen_data()

# ==========================================
# LAYOUT
# ==========================================
st.title("🚀 STC Leadership Dashboard | Autoscuola ERP 2025")
st.subheader("Status Report: Week 29 (July 14 – July 20, 2025)")

# TOP METRICS
m1, m2, m3, m4 = st.columns(4)
m1.metric("SPI (Performance)", "0.85", "-0.15 vs Target")
with m2:
    st.markdown("**Defect Health (UAT)**")
    st.markdown("🔴 2 | 🟡 5 | 🟢 12")
m3.metric("Handover Lag", "4.1 Hrs", "Target < 4.0")
m4.metric("Sprint Velocity", "79%", "Capacity Risk")

tab1, tab2, tab3 = st.tabs(["📉 Timeline & SPI", "🌍 Regional Agile", "🐛 Quality Assurance"])

# --- TAB 1 (LOCKED) ---
with tab1:
    st.subheader("📈 SPI Recovery Trend")
    st.plotly_chart(px.line(df_trend, x='Week', y='SPI', markers=True), width='stretch')
    
    st.markdown("---")
    st.markdown("#### 📋 Week 29 Task Audit Console")
    def color_spi(val):
        color = 'red' if val < 0.85 else ('orange' if val < 0.95 else 'green')
        return f'background-color: {color}; color: white; font-weight: bold'
    for group in ["Completed This Week", "Ongoing / Delayed"]:
        st.write(f"**{group}**")
        subset = df_tasks[df_tasks['Group'] == group][['ID', 'Task', 'Workstream', 'Owner', 'SPI', 'Days Taken', 'Variance (Days)']]
        st.dataframe(subset.style.applymap(color_spi, subset=['SPI']).format({'SPI': "{:.2f}"}), width='stretch', hide_index=True)

# --- TAB 2 (RESTORED 3-CHART LAYOUT) ---
with tab2:
    st.subheader("🌍 Regional Efficiency & Collaboration")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**1. Technical Intake (Pie)**")
        st.plotly_chart(px.pie(df_sizes, values='Count', names='Size', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu), width='stretch')
    with col2:
        st.markdown("**2. Handover Lag Trend (Line)**")
        lag_trend = df_sprints.groupby('Sprint')['Lag'].mean().reset_index()
        fig_line = px.line(lag_trend, x='Sprint', y='Lag', markers=True)
        fig_line.add_hline(y=4.0, line_dash="dot", line_color="red", annotation_text="Target (4h)")
        st.plotly_chart(fig_line, width='stretch')

    st.markdown("---")
    st.markdown("#### 📊 3. Sprint Velocity Heatmap")
    pivot_vel = df_sprints.pivot(index="Workstream", columns="Sprint", values="Velocity")
    st.plotly_chart(px.imshow(pivot_vel, text_auto=".0%", color_continuous_scale="RdYlGn", aspect="auto"), width='stretch')

# --- TAB 3 (UPDATED LOGIC) ---
with tab3:
    st.subheader("🧪 UAT & Data Integrity Verification")
    
    st.info("✅ **UAT Achievement:** 60+ Scenarios Executed | 52 Critical Defects Resolved | 100% Data Integrity Verified")
    
    st.markdown("#### 📉 Defect Resolution Speed (MTTR)")
    fig_defects = px.scatter(
        df_defects, 
        x='Date', 
        y='Resolution_Days', 
        size='Resolution_Days', 
        color='Severity', 
        color_discrete_map={'Critical': COLOR_RED, 'High': COLOR_AMBER, 'Medium': COLOR_GREEN},
        title="Impact of Process Improvements on Bug Fixing Speed"
    )
    st.plotly_chart(fig_defects, width='stretch')

    st.markdown("#### 📋 Critical Defect Resolution Log (Top 10)")
    # Filter only Critical to match the table title
    critical_bugs = df_defects[df_defects['Severity'] == 'Critical'].sort_values('Resolution_Days', ascending=False).head(10)
    st.dataframe(critical_bugs[['ID', 'Date', 'Workstream', 'Resolution_Days', 'Severity']], width='stretch', hide_index=True)
