import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.express as px

from src.data_loader import load_data
from src.demand_prediction import predict_passengers
from src.resource_optimizer import recommend_coaches


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Smart Railway Planner",
    page_icon="🚆",
    layout="wide"
)

# -----------------------------
# Custom CSS Styling
# -----------------------------
st.markdown("""
<style>

.main-title {
    font-size:48px;
    font-weight:700;
    text-align:center;
    padding:15px;
    border-radius:10px;
    background: linear-gradient(90deg,#1f77b4,#00c6ff);
    color:white;
}

.section-title{
    font-size:28px;
    font-weight:600;
    margin-top:20px;
    margin-bottom:10px;
    color:#1f77b4;
}

.metric-box{
    background:linear-gradient(135deg,#667eea,#764ba2);
    padding:20px;
    border-radius:12px;
    color:white;
    text-align:center;
    font-size:20px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.markdown('<div class="main-title">🚆 Smart Railway Resource Planning System</div>', unsafe_allow_html=True)

st.write("")

# -----------------------------
# Load Dataset
# -----------------------------
data = load_data("data/railway_dataset.csv")

# -----------------------------
# Dataset Overview
# -----------------------------
st.markdown('<div class="section-title">📊 Dataset Overview</div>', unsafe_allow_html=True)

col1,col2,col3 = st.columns(3)

col1.metric("Total Records",len(data))
col2.metric("Unique Routes",data["Source"].nunique())
col3.metric("Platforms",data["Platform"].nunique())

st.write("")

# -----------------------------
# Prediction Panel
# -----------------------------
st.markdown('<div class="section-title">🔮 Passenger Demand Prediction</div>', unsafe_allow_html=True)

col1,col2,col3,col4 = st.columns(4)

day = col1.slider("Day",1,31,15)
month = col2.slider("Month",1,12,6)
holiday = col3.selectbox("Holiday",[0,1])
capacity = col4.number_input("Train Capacity",100,2000,1000)

if st.button("Predict Demand"):

    predicted = predict_passengers(day,month,holiday)

    coaches = recommend_coaches(predicted,capacity)

    c1,c2 = st.columns(2)

    with c1:
        st.markdown(f"""
        <div class="metric-box">
        🚆 Predicted Passengers<br>
        <h2>{predicted}</h2>
        </div>
        """,unsafe_allow_html=True)

    with c2:
        if coaches>0:
            st.markdown(f"""
            <div class="metric-box">
            ➕ Extra Coaches Needed<br>
            <h2>{coaches}</h2>
            </div>
            """,unsafe_allow_html=True)
        else:
            st.success("No extra coaches required")

st.write("")

# -----------------------------
# Visualization Section
# -----------------------------
st.markdown('<div class="section-title">📈 Passenger Demand Insights</div>', unsafe_allow_html=True)

col1,col2 = st.columns(2)

# Route demand
route_data = data.groupby(["Source","Destination"])["Passengers"].sum().reset_index()
route_data["Route"] = route_data["Source"]+" → "+route_data["Destination"]

fig1 = px.bar(
    route_data,
    x="Route",
    y="Passengers",
    title="Passenger Demand by Route",
)

col1.plotly_chart(fig1,use_container_width=True)

# Platform utilization
platform_data = data.groupby("Platform")["Passengers"].sum().reset_index()

fig2 = px.pie(
    platform_data,
    values="Passengers",
    names="Platform",
    title="Platform Usage Distribution"
)

col2.plotly_chart(fig2,use_container_width=True)

st.write("")

# -----------------------------
# Time Demand Analysis
# -----------------------------
st.markdown('<div class="section-title">⏰ Monthly Passenger Trends</div>', unsafe_allow_html=True)

monthly = data.groupby("Month")["Passengers"].sum().reset_index()

fig3 = px.line(
    monthly,
    x="Month",
    y="Passengers",
    markers=True,
    title="Passenger Demand by Month"
)

st.plotly_chart(fig3,use_container_width=True)

st.write("")

# -----------------------------
# Raw Dataset Viewer
# -----------------------------
st.markdown('<div class="section-title">📂 Dataset Viewer</div>', unsafe_allow_html=True)

st.dataframe(data.head(50))