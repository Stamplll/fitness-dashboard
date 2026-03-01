import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Fitness Tracker", layout="wide")

st.title("🏃‍♂️ Fitness Tracker Dashboard")
st.write("เลือกประเภทกีฬาและช่วงวันที่เพื่อกรองข้อมูล แล้วกราฟจะปรับตาม")

# Load data
df = pd.read_csv("data.csv")
df["date"] = pd.to_datetime(df["date"])

# Sidebar filters
st.sidebar.header("ตัวกรองกีฬา")
sports = df["sport"].unique().tolist()
selected_sports = []
for s in sports:
    if st.sidebar.checkbox(s, value=True):
        selected_sports.append(s)

st.sidebar.header("ตัวกรองวันที่")
min_date = df["date"].min()
max_date = df["date"].max()
start_date, end_date = st.sidebar.date_input(
    "เลือกช่วงวันที่",
    [min_date, max_date],
)

# Apply filters
filtered = df[
    (df["sport"].isin(selected_sports)) &
    (df["date"] >= pd.to_datetime(start_date)) &
    (df["date"] <= pd.to_datetime(end_date))
]

# Empty state
if filtered.empty:
    st.warning("กรุณาเลือกอย่างน้อย 1 ประเภทกีฬา หรือปรับช่วงวันที่ใหม่")
    st.stop()

# KPI
st.subheader("📊 KPI Summary")
total_calories = filtered["calories"].sum()
total_distance = filtered["distance_km"].sum()
total_minutes = filtered["minutes"].sum()
total_activities = len(filtered)

avg_calories = filtered["calories"].mean()
avg_distance = filtered["distance_km"].mean()
avg_minutes = filtered["minutes"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("🔥 Total Calories", f"{total_calories:.0f}")
col2.metric("📏 Total Distance (km)", f"{total_distance:.1f}")
col3.metric("⏱ Total Minutes", f"{total_minutes:.0f}")
col4.metric("✅ Activities", f"{total_activities}")

col5, col6, col7 = st.columns(3)
col5.metric("🔥 Avg Calories", f"{avg_calories:.0f}")
col6.metric("📏 Avg Distance", f"{avg_distance:.1f}")
col7.metric("⏱ Avg Minutes", f"{avg_minutes:.0f}")

st.caption("ค่าด้านบนคือภาพรวมของกิจกรรมที่ถูกเลือกในช่วงวันที่ที่กำหนด")
st.divider()

# Charts
st.subheader("🔥 แคลอรี่ที่เผาผลาญต่อวัน (Bar Chart)")
calories_per_day = filtered.groupby("date")["calories"].sum().reset_index()
calories_per_day = calories_per_day.sort_values("date")
fig_bar = px.bar(calories_per_day, x="date", y="calories", color="date")
st.plotly_chart(fig_bar, use_container_width=True)
st.caption("แสดงจำนวนแคลอรี่รวมในแต่ละวัน")

st.divider()

st.subheader("📈 ระยะทางรวมต่อวัน (Line Chart)")
distance_per_day = filtered.groupby("date")["distance_km"].sum().reset_index()
distance_per_day = distance_per_day.sort_values("date")
fig_line = px.line(distance_per_day, x="date", y="distance_km", markers=True)
st.plotly_chart(fig_line, use_container_width=True)
st.caption("แสดงระยะทางรวมในแต่ละวัน")

st.divider()

st.subheader("🔹 เวลา vs แคลอรี่ (Scatter Plot)")
fig_scatter = px.scatter(
    filtered,
    x="minutes",
    y="calories",
    color="sport",
    size="calories",
    trendline="ols",
    hover_data=["date"],
)
st.plotly_chart(fig_scatter, use_container_width=True)
st.caption("ดูความสัมพันธ์ระหว่างเวลาที่ใช้กับแคลอรี่")

st.divider()

# Data section
st.subheader("📋 Data Preview")
show_all = st.checkbox("แสดงข้อมูลทั้งหมด (ไม่กรองกีฬา)")
display_df = df if show_all else filtered
display_df = display_df.sort_values("date")

st.caption(f"จำนวนแถวที่แสดง: {len(display_df)}")
st.dataframe(display_df)

st.divider()
st.caption("Made with ❤️ using Streamlit")