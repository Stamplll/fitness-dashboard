import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Fitness Tracker", layout="wide")

st.title("🏃‍♂️ Fitness Tracker Dashboard")
st.write("เลือกประเภทกีฬาเพื่อกรองข้อมูล แล้วกราฟจะปรับตาม")

# Load data
df = pd.read_csv("data.csv")
df["date"] = pd.to_datetime(df["date"])

# Filter by sport
sports = df["sport"].unique().tolist()
selected_sports = []

st.sidebar.header("ตัวกรองกีฬา")
for s in sports:
    if st.sidebar.checkbox(s, value=True):
        selected_sports.append(s)

filtered = df[df["sport"].isin(selected_sports)]

# Empty state
if filtered.empty:
    st.warning("กรุณาเลือกอย่างน้อย 1 ประเภทกีฬา")
    st.stop()

# KPI
total_calories = filtered["calories"].sum()
total_distance = filtered["distance_km"].sum()
total_minutes = filtered["minutes"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("🔥 Calories", f"{total_calories:.0f}")
col2.metric("📏 Distance (km)", f"{total_distance:.1f}")
col3.metric("⏱ Minutes", f"{total_minutes:.0f}")

st.divider()

# Charts
st.subheader("🔥 แคลอรี่ที่เผาผลาญต่อวัน (Bar Chart)")
calories_per_day = filtered.groupby("date")["calories"].sum().reset_index()
fig_bar = px.bar(calories_per_day, x="date", y="calories", color="date")
st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("📈 ระยะทางรวมต่อวัน (Line Chart)")
distance_per_day = filtered.groupby("date")["distance_km"].sum().reset_index()
fig_line = px.line(distance_per_day, x="date", y="distance_km", markers=True)
st.plotly_chart(fig_line, use_container_width=True)

st.subheader("🔹 เวลา vs แคลอรี่ (Scatter Plot)")
fig_scatter = px.scatter(
    filtered,
    x="minutes",
    y="calories",
    color="sport",
    size="distance_km",
    hover_data=["date"],
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("📋 ตารางข้อมูล")
st.dataframe(filtered)

st.subheader("📊 KPI Summary")
st.caption("ค่าด้านบนคือภาพรวมของกิจกรรมที่ถูกเลือกในช่วงวันที่ที่กำหนด")
st.subheader("🔥 แคลอรี่ที่เผาผลาญต่อวัน (Bar Chart)")
st.subheader("📈 ระยะทางรวมต่อวัน (Line Chart)")
st.subheader("🔹 เวลา vs แคลอรี่ (Scatter Plot)")

st.caption("แสดงจำนวนแคลอรี่รวมในแต่ละวัน")
st.caption("แสดงระยะทางรวมในแต่ละวัน")
st.divider()

st.sidebar.header("ตัวกรองวันที่")
min_date = df["date"].min()
max_date = df["date"].max()
start_date, end_date = st.sidebar.date_input(
    "เลือกช่วงวันที่",
    [min_date, max_date],
)
filtered = df[
    (df["sport"].isin(selected_sports)) &
    (df["date"] >= pd.to_datetime(start_date)) &
    (df["date"] <= pd.to_datetime(end_date))
]

total_activities = len(filtered)
avg_calories = filtered["calories"].mean()
avg_distance = filtered["distance_km"].mean()
avg_minutes = filtered["minutes"].mean()