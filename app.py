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
# DATA ENGINE
# ==========================================
@st.cache_data
def generate_frozen_data():
    # Pool di problemi tecnici unici (Senza random per il Log dei Critici)
    unique_critical_issues = [
        "SQL Injection vulnerability in login module",
        "Unauthenticated API access to Personal Identifiable Information",
        "Database deadlock during high-concurrency invoice generation",
        "Total data loss in sync between mobile app and core database",
        "Bypass of Multi-Factor Authentication (MFA) on admin portal",
        "Insecure Direct Object Reference (IDOR) on student records",
        "Hardcoded encryption keys found in public source code",
        "Race condition in booking logic causing double exam assignments",
        "Complete failure of the payment gateway integration",
        "Unauthorized privilege escalation in the user management module"
    ]
    
    other_issues = [
        {"desc": "Memory leak in PDF generation engine causing server crashes", "sev": "High"},
        {"desc": "Broken TLS handshake for specific European ISP ranges", "sev": "High"},
        {"desc": "Validation error in VAT calculation for cross-border transactions", "sev": "High"},
        {"desc": "Slow response times (>5s) on fleet tracking dashboard", "sev": "Medium"},
        {"desc": "CSS layout shift in Safari mobile for instructor scheduling", "sev": "Medium"}
    ]

    # Row 1 Data
    weeks = pd.date_range(start=PROJECT_START, end=SNAPSHOT_DATE, freq='W')
    spi_values = [0.40, 0.45, 0.42, 0.50, 0.55, 0.48, 0.52, 0.65, 0.78, 0.82, 0.85]
    df_trend = pd.DataFrame({'Week': weeks[:len(spi_values)], 'SPI': spi_values})

    tasks = [
        {"ID": "2025-074", "Task": "Configure VAT Rules", "Workstream": "Finance", "Owner": "Antonio", "Planned": 10, "Actual": 22, "Group": "Ongoing"},
        {"ID": "2025-081", "Task": "Student Master Migration", "Workstream": "Lifecycle", "Owner": "Mateo", "Planned": 12, "Actual": 14, "Group": "Ongoing"},
        {"ID": "2025-085", "Task": "Fuel Tracker API", "Workstream": "Fleet", "Owner": "Francesco", "Planned": 8, "Actual": 9, "Group": "Ongoing"},
        {"ID": "2025-088", "Task": "Regional Tax Calc", "Workstream": "Finance", "Owner": "Valentina", "Planned": 15, "Actual": 16, "Group": "Ongoing"},
        {"ID": "2025-090", "Task": "Shift Planning Fixes", "Workstream": "Instructor", "Owner": "Enzo", "Planned": 5, "Actual": 5, "Group": "Completed This Week"},
        {"ID": "2025-092", "Task": "Enrollment Design", "Workstream": "Lifecycle", "Owner": "Camila", "Planned": 7, "Actual": 7, "Group": "Completed This Week"}
    ]
    df_tasks = pd.DataFrame(tasks)
    df_tasks['SPI'] = (df_tasks['Planned'] / df_tasks['Actual']).round(2)
    df_tasks['Days Taken'] = df_tasks['Actual']
    df_tasks['Variance (Days)'] = df_tasks['Actual'] - df_tasks['Planned']
    
    # Row 2 Data
    sizing_data = {'Size': ['S', 'M', 'L', 'XL'], 'Count': [45, 62, 28, 15]}
    df_sizes = pd.DataFrame(sizing_data)
    WORKSTREAMS = ['Student Lifecycle', 'Fleet Management', 'Instructor Scheduling', 'Exam Booking (App)', 'Finance & Regulatory']
    
    sprints = []
    for s_num in range(1, 9):
        for ws in WORKSTREAMS:
            vel = np.random.uniform(0.92, 1.0) if s_num > 4 else np.random.uniform(0.58, 0.88)
            lag = np.random.uniform(2, 5) if s_num > 4 else np.random.uniform(12, 26)
            sprints.append({'Sprint': f"Sprint {s_num}", 'Workstream': ws, 'Velocity': round(vel, 2), 'Lag': round(lag, 1)})
    df_sprints = pd.DataFrame(sprints)

    # Row 3 Data
    defects = []
    trans_start, trans_end = datetime(2025, 6, 1), datetime(2025, 6, 15)
    
    for i in range(65):
        days_offset = np.random.randint(0, 85)
        rep_date = PROJECT_START + timedelta(days=days_offset)
        
        # Assegnazione deterministica per i primi 10 critici
        if i < 10:
            desc = unique_critical_issues[i]
            sev = "Critical"
            res_days = np.random.randint(15, 26) # Renderli i più lenti per farli apparire in cima
        else:
            issue = np.random.choice(other_issues)
            desc = issue['desc']
            sev = issue['sev']
            # Logica transizione normale
            if rep_date < trans_start: res_days = np.random.randint(10, 20)
            elif rep_date > trans_end: res_days = np.random.randint(1, 6)
            else: res_days = np.random.randint(5, 12)
            
        defects.append({
            'ID': f'DEF-{i+1:03d}', 
            'Date': rep_date, 
            'Description': desc,
            'Severity': sev, 
            'Resolution_Days': res_days, 
            'Workstream': WORKSTREAMS[i % len(WORKSTREAMS)]
        })
    df_defects = pd.DataFrame(defects)

    return df_trend, df_tasks, df_sizes, df_sprints, df_defects

df_trend, df_tasks, df_sizes, df_sprints, df_defects = generate_frozen_data()

# ==========================================
# HEADER
# ==========================================
st.title("🚀 STC Leadership Dashboard | Autoscuola ERP 2025")
st.subheader("Unified Status Report: Week 29 (July 14 – July 20, 2025)")

m1, m2, m3, m4 = st.columns(4)
m1.metric("SPI (Performance)", "0.85", "-0.15 vs Target")
with m2:
    st.markdown("**Defect Health (UAT)**")
    st.markdown("🔴 2 | 🟡 5 | 🟢 12")
m3.metric("Handover Lag", "4.1 Hrs", "Target < 4.0")
m4.metric("Sprint Velocity", "79%", "Capacity Risk")

st.markdown("---")

# ==========================================
# ROW 1
# ==========================================
st.subheader("📊Performance & Task Audit")
r1_c1, r1_c2 = st.columns([1, 1])
with r1_c1:
    st.markdown("#### 📈 SPI Recovery Trend")
    st.plotly_chart(px.line(df_trend, x='Week', y='SPI', markers=True), width='stretch')
with r1_c2:
    st.markdown("#### 📋 Task Audit")
    def color_spi(val):
        color = 'red' if val < 0.85 else ('orange' if val < 0.95 else 'green')
        return f'background-color: {color}; color: white; font-weight: bold'
    for group in ["Completed This Week", "Ongoing"]:
        st.write(f"**{group}**")
        subset = df_tasks[df_tasks['Group'] == group][['ID', 'Task', 'Workstream', 'Owner', 'SPI', 'Days Taken', 'Variance (Days)']]
        st.dataframe(subset.style.applymap(color_spi, subset=['SPI']).format({'SPI': "{:.2f}"}), width='stretch', hide_index=True)

st.markdown("---")

# ==========================================
# ROW 2
# ==========================================
st.subheader("🌍Regional Efficiency & Sprint Metrics")
r2_c1, r2_c2, r2_c3 = st.columns(3)
with r2_c1:
    st.markdown("#### 📉 Technical Intake")
    st.plotly_chart(px.pie(df_sizes, values='Count', names='Size', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu), width='stretch')
with r2_c2:
    st.markdown("#### 📉 Handover Lag")
    lag_trend = df_sprints.groupby('Sprint')['Lag'].mean().reset_index()
    fig_line = px.line(lag_trend, x='Sprint', y='Lag', markers=True)
    fig_line.add_hline(y=4.0, line_dash="dot", line_color="red", annotation_text="Target (4h)")
    st.plotly_chart(fig_line, width='stretch')
with r2_c3:
    st.markdown("#### 📉 Sprint Velocity")
    pivot_vel = df_sprints.pivot(index="Workstream", columns="Sprint", values="Velocity")
    st.plotly_chart(px.imshow(pivot_vel, text_auto=".0%", color_continuous_scale="RdYlGn", aspect="auto"), width='stretch')

st.markdown("---")

# ==========================================
# ROW 3
# ==========================================
st.subheader("🧪Quality Assurance & Bug Tracking")
r3_c1, r3_c2 = st.columns([1, 1.2])

with r3_c1:
    st.markdown("#### 📉 Defect Resolution Speed (MTTR)")
    fig_defects = px.scatter(df_defects, x='Date', y='Resolution_Days', size='Resolution_Days', color='Workstream')
    st.plotly_chart(fig_defects, width='stretch')

with r3_c2:
    st.markdown("#### 📋 Critical Defect Resolution Log")
    # Filtriamo i critici e ordiniamo per tempo di risoluzione per mostrare i problemi unici generati
    critical_bugs = df_defects[df_defects['Severity'] == 'Critical'].sort_values('Resolution_Days', ascending=False).head(10)
    
    st.dataframe(
        critical_bugs[['ID', 'Date', 'Description', 'Workstream', 'Resolution_Days', 'Severity']].style.set_properties(**{
            'font-size': '11px'
        }),
        width='stretch',
        hide_index=True,
        column_config={
            "Description": st.column_config.TextColumn("Issue Description", width="large"),
            "Date": st.column_config.DatetimeColumn("Date", format="D MMM YYYY")
        }
    )
