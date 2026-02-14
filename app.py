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
# CONFIGURATION (LOCKED: 2025)
# ==========================================
st.set_page_config(page_title="STC Leadership Dashboard 2025", layout="wide")

COLOR_RED, COLOR_AMBER, COLOR_GREEN = "#FF4B4B", "#FFA500", "#09AB3B"
PROJECT_START, PROJECT_END = datetime(2025, 5, 1), datetime(2025, 8, 31)
SNAPSHOT_DATE = datetime(2025, 8, 20) 

PHASE_START = datetime(2025, 6, 10) 
PHASE_STABLE = datetime(2025, 7, 1)  

WORKSTREAMS = {
    'Student Lifecycle': ['Design Enrollment Flow', 'Configure Student Master Data', 'Automate Fee Invoicing'],
    'Fleet Management': ['Define Vehicle Types', 'Configure Maintenance Plans', 'Fuel Consumption Tracker'],
    'Instructor Scheduling': ['Design Shift Planning UI', 'Configure HR Rules', 'Instructor Payroll Mapping'],
    'Exam Booking (App)': ['Design App Screens', 'Develop Booking API', 'Geolocation Engine'],
    'Finance & Regulatory': ['Configure VAT Rules', 'Motorizzazione Interface', 'Regional Tax Calculator']
}

TEAMS = {
    'Italy': ['Antonio', 'Francesco', 'Enzo', 'Emilio', 'Sofia'], 
    'Colombia': ['Mateo', 'Valentina', 'Juan', 'Camila', 'Diego']
}

# ==========================================
# DATA ENGINE
# ==========================================
@st.cache_data
def generate_data():
    tasks = []
    for i in range(1, 151):
        ws_name = np.random.choice(list(WORKSTREAMS.keys()))
        task_base = np.random.choice(WORKSTREAMS[ws_name])
        unique_task_name = f"{task_base} [Ref: {2025}-{i:03d}]"
        
        region = 'Italy' if any(n in task_base for n in ['Design', 'Define', 'Configure']) else 'Colombia'
        owner = np.random.choice(TEAMS[region])
        
        p_start = PROJECT_START + timedelta(days=np.random.randint(0, 90))
        p_dur = np.random.randint(5, 15)
        
        if p_start < PHASE_START:
            delay = np.random.uniform(1.25, 1.30) # SPI ~0.78
        elif p_start < PHASE_STABLE:
            delay = np.random.uniform(1.10, 1.15) # SPI ~0.88
        else:
            delay = np.random.uniform(0.98, 1.02) # SPI ~0.99

        a_end = p_start + timedelta(days=int(p_dur * delay))
        spi = p_dur / (p_dur * delay)
        
        # STATUS LOGIC: Existing, In Progress, Finished
        if a_end < SNAPSHOT_DATE: 
            status = "Finished ✅"
        elif p_start < SNAPSHOT_DATE: 
            status = "In Progress ⏳"
        else: 
            status = "Existing (To Do) 📅"
            
        rag = 'Red' if spi < 0.85 else ('Amber' if spi < 0.95 else 'Green')
        tasks.append({'Task': unique_task_name, 'Workstream': ws_name, 'Owner': owner, 'Actual_End': a_end, 'SPI': round(spi, 2), 'RAG': rag, 'Status': status})
    
    sprints = []
    for s_num in range(1, 9):
        for ws in WORKSTREAMS.keys():
            if s_num <= 2: vel, lag = np.random.uniform(0.58, 0.65), np.random.uniform(22, 26)
            elif s_num <= 4: vel, lag = np.random.uniform(0.78, 0.88), np.random.uniform(12, 18)
            else: vel, lag = np.random.uniform(0.92, 1.0), np.random.uniform(2, 5)
            sprints.append({'Sprint': f"Sprint {s_num}", 'Workstream': ws, 'Velocity': round(vel, 2), 'Lag': round(lag, 1)})
    
    defects = []
    for i in range(1, 71):
        ws = np.random.choice(list(WORKSTREAMS.keys()))
        rep_date = PROJECT_START + timedelta(days=int(np.random.beta(2, 5) * 120))
        # Resolution logic tied to the project phasing
        if rep_date < PHASE_START: res_days = np.random.randint(14, 22)
        elif rep_date < PHASE_STABLE: res_days = np.random.randint(6, 12)
        else: res_days = np.random.randint(1, 4)
            
        defects.append({
            'ID': f'DEF-{i:03d}', 
            'Workstream': ws, 
            'Severity': np.random.choice(['Critical', 'High', 'Medium']), 
            'Date': rep_date, 
            'Resolution_Days': res_days
        })
    
    return pd.DataFrame(tasks), pd.DataFrame(sprints), pd.DataFrame(defects)

df_timeline, df_sprints, df_defects = generate_data()

# ==========================================
# DASHBOARD LAYOUT
# ==========================================
st.title("🚀 STC Leadership Dashboard | Autoscuola ERP 2025")
st.markdown(f"**Snapshot Date:** {SNAPSHOT_DATE.strftime('%d-%m-%Y')} | **Status:** 🟢 Project Stabilized")

col1, col2, col3, col4 = st.columns(4)
col1.metric("SPI (Performance)", "0.99", "Target: 1.0")
col2.metric("Critical Defects", "2", "-5 vs Q2", delta_color="inverse")
col3.metric("Handover Lag", "4.1 Hrs", "-18 Hrs Improvement", delta_color="inverse")
col4.metric("Sprint Velocity", "96%", "+30% Recovery")

tab1, tab2, tab3 = st.tabs(["📉 Timeline & SPI", "🌍 Regional Agile", "🐛 Quality Assurance"])

# --- TAB 1 (LOCKED: Corrected SPI & Status Table) ---
with tab1:
    st.subheader("📈 SPI Recovery Trend")
    df_timeline['Week_Start'] = df_timeline['Actual_End'].apply(lambda d: d - timedelta(days=d.weekday()))
    spi_trend = df_timeline.groupby('Week_Start')['SPI'].mean().reset_index()
    fig_spi = px.line(spi_trend, x='Week_Start', y='SPI', markers=True, labels={'SPI': 'Project Efficiency'})
    fig_spi.add_shape(type="line", x0=PHASE_START, y0=0, x1=PHASE_START, y1=1, yref="paper", line=dict(color="orange", width=2, dash="dash"))
    fig_spi.add_shape(type="line", x0=PHASE_STABLE, y0=0, x1=PHASE_STABLE, y1=1, yref="paper", line=dict(color="green", width=2, dash="dash"))
    st.plotly_chart(fig_spi, width="stretch")
    
    st.markdown("#### 📋 Critical Task Console (Top 10)")
    st.dataframe(df_timeline[df_timeline['RAG'] == 'Red'].sort_values('SPI').head(10)[['Task', 'Owner', 'Status', 'SPI', 'RAG']], width="stretch")

# --- TAB 2 ---
with tab2:
    st.subheader("👕 Agile & Regional Efficiency")
    fig_handover = px.bar(df_sprints, x='Sprint', y='Lag', color='Workstream', barmode='group')
    st.plotly_chart(fig_handover, width="stretch")
    pivot_vel = df_sprints.pivot(index="Workstream", columns="Sprint", values="Velocity")
    st.plotly_chart(px.imshow(pivot_vel, text_auto=".0%", color_continuous_scale="RdYlGn", aspect="auto"), width="stretch")

# --- TAB 3 (UPDATED: Resolution Days on Y-Axis) ---
with tab3:
    st.subheader("🐛 Quality: Resolution Time Trend (MTTR)")
    
    # Chart 3 Logic: Y-axis is now Resolution_Days
    fig_defects = px.scatter(
        df_defects, 
        x=df_defects['Date'].tolist(), 
        y='Resolution_Days', 
        size='Resolution_Days', 
        color='Workstream',
        hover_data=['Severity', 'Resolution_Days'],
        labels={'Resolution_Days': 'Days to Fix (MTTR)', 'x': 'Date Reported'},
        title="UAT Defect Resolution Speed over 2025"
    )
    st.plotly_chart(fig_defects, width="stretch")