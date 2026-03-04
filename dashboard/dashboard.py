import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Sales Intelligence Dashboard", layout="wide")

# ================= DARK THEME =================
st.markdown("""
<style>

html, body, [class*="css"] {
    background-color:#0b0f1a;
    color:white;
}

.metric-card{
background:linear-gradient(135deg,#1f2937,#111827);
padding:20px;
border-radius:12px;
text-align:center;
}

.metric-title{
color:#9ca3af;
}

.metric-value{
font-size:28px;
font-weight:bold;
color:#22c55e;
}

</style>
""", unsafe_allow_html=True)

st.title("🚀 Business Sales Intelligence Dashboard")

# ================= LOAD DATA =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR,"data","sales_data.csv")

df = pd.read_csv(data_path,encoding="latin1")
df["Order Date"] = pd.to_datetime(df["Order Date"],errors="coerce")

# ================= TOP FILTER BAR =================
st.markdown("### Dashboard Filters")

f1,f2,f3,f4 = st.columns(4)

with f1:
    date_range = st.date_input(
        "Date Range",
        [df["Order Date"].min(), df["Order Date"].max()]
    )

with f2:
    regions = st.multiselect(
        "Region",
        df["Region"].unique(),
        default=df["Region"].unique()
    )

with f3:
    categories = st.multiselect(
        "Category",
        df["Category"].unique(),
        default=df["Category"].unique()
    )

with f4:
    segments = st.multiselect(
        "Segment",
        df["Segment"].unique(),
        default=df["Segment"].unique()
    )

# ================= APPLY FILTERS =================
filtered_df = df[
(df["Order Date"] >= pd.to_datetime(date_range[0])) &
(df["Order Date"] <= pd.to_datetime(date_range[1])) &
(df["Region"].isin(regions)) &
(df["Category"].isin(categories)) &
(df["Segment"].isin(segments))
]

# ================= KPI METRICS =================
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
orders = len(filtered_df)

profit_margin = (total_profit/total_sales)*100 if total_sales>0 else 0
avg_order = total_sales/orders if orders>0 else 0

k1,k2,k3,k4,k5 = st.columns(5)

k1.metric("Revenue",f"${total_sales:,.0f}")
k2.metric("Profit",f"${total_profit:,.0f}")
k3.metric("Orders",orders)
k4.metric("Profit Margin",f"{profit_margin:.2f}%")
k5.metric("Avg Order Value",f"${avg_order:,.0f}")

st.divider()

# ================= SALES TREND =================
filtered_df["Month"] = filtered_df["Order Date"].dt.to_period("M")

monthly = filtered_df.groupby("Month")["Sales"].sum().reset_index()
monthly["Month"] = monthly["Month"].astype(str)

fig_trend = px.line(
monthly,
x="Month",
y="Sales",
markers=True,
color_discrete_sequence=["#22c55e"]
)

fig_trend.update_layout(template="plotly_dark")

# ================= CATEGORY =================
category = filtered_df.groupby("Category")[["Sales","Profit"]].sum().reset_index()

fig_cat = px.bar(
category,
x="Category",
y="Sales",
color="Profit",
color_continuous_scale="Turbo"
)

fig_cat.update_layout(template="plotly_dark")

# ================= REGION =================
region = filtered_df.groupby("Region")[["Sales","Profit"]].sum().reset_index()

fig_region = px.bar(
region,
x="Region",
y="Sales",
color="Profit",
color_continuous_scale="Rainbow"
)

fig_region.update_layout(template="plotly_dark")

# ================= DASHBOARD GRID =================
c1,c2 = st.columns(2)

with c1:
    st.subheader("Revenue Trend")
    st.plotly_chart(fig_trend,use_container_width=True)

with c2:
    st.subheader("Category Performance")
    st.plotly_chart(fig_cat,use_container_width=True)

c3,c4 = st.columns(2)

with c3:
    st.subheader("Regional Sales")
    st.plotly_chart(fig_region,use_container_width=True)

with c4:
    st.subheader("Top Products")

    top = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    )

    st.dataframe(top)

st.success("Dashboard ready with dark mode & interactive filters")