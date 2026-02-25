import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Client Business Intelligence Dashboard", layout="wide")

st.title("📊 Business Sales Intelligence – Executive Dashboard")

# ================= LOAD DATA =================
df = pd.read_csv("../data/sales_data.csv", encoding="latin1")
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

# ================= SIDEBAR FILTERS =================
st.sidebar.header("🔍 Business Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    [df["Order Date"].min(), df["Order Date"].max()]
)

regions = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

categories = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Order Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order Date"] <= pd.to_datetime(date_range[1])) &
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories))
]

# ================= KPI METRICS =================
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
orders = len(filtered_df)
profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0
avg_order_value = total_sales / orders if orders > 0 else 0

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("💰 Revenue", f"${total_sales:,.0f}")
k2.metric("📈 Profit", f"${total_profit:,.0f}")
k3.metric("📦 Orders", orders)
k4.metric("📊 Profit Margin", f"{profit_margin:.2f}%")
k5.metric("🧾 Avg Order Value", f"${avg_order_value:,.0f}")

st.divider()

# ================= SALES TREND =================
st.subheader("📈 Revenue Trend Over Time")

filtered_df["Month"] = filtered_df["Order Date"].dt.to_period("M")
monthly_sales = filtered_df.groupby("Month")["Sales"].sum().reset_index()
monthly_sales["Month"] = monthly_sales["Month"].astype(str)

fig_trend = px.line(monthly_sales, x="Month", y="Sales", markers=True)
st.plotly_chart(fig_trend, use_container_width=True)

# ================= CATEGORY PROFITABILITY =================
st.subheader("💼 Category Profitability")

category_perf = filtered_df.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
category_perf["Profit Margin %"] = (category_perf["Profit"] / category_perf["Sales"]) * 100

fig_cat = px.bar(
    category_perf,
    x="Category",
    y="Profit Margin %",
    text_auto=True,
    color="Profit Margin %"
)
st.plotly_chart(fig_cat, use_container_width=True)

# ================= REGION PERFORMANCE =================
st.subheader("🌍 Regional Performance")

region_perf = filtered_df.groupby("Region")[["Sales", "Profit"]].sum().reset_index()

fig_region = px.bar(
    region_perf,
    x="Region",
    y="Sales",
    color="Profit",
    text_auto=True
)
st.plotly_chart(fig_region, use_container_width=True)

# ================= PRODUCT ANALYSIS =================
st.subheader("🏆 Product Performance")

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

colA, colB = st.columns(2)

with colA:
    st.markdown("### Top 10 Revenue Products")
    st.dataframe(top_products.head(10))

with colB:
    st.markdown("### Bottom 10 Products (Risk)")
    st.dataframe(top_products.tail(10))

# ================= BUSINESS INSIGHTS =================
st.divider()
st.subheader("📌 Executive Insights & Recommendations")

# INSIGHTS LOGIC
best_region = region_perf.sort_values("Profit", ascending=False).iloc[0]["Region"]
worst_region = region_perf.sort_values("Profit").iloc[0]["Region"]
best_category = category_perf.sort_values("Profit", ascending=False).iloc[0]["Category"]

st.markdown(f"""
### 🔍 Key Insights
- **{best_region}** is the most profitable region.
- **{worst_region}** is underperforming and needs attention.
- **{best_category}** category delivers the highest profit margin.
- Average order value is **${avg_order_value:.0f}**, indicating scope for upselling.
""")

# ACTIONABLE RECOMMENDATIONS
st.markdown("""
### 🎯 Actionable Business Recommendations
1. **Scale High-Profit Categories**
   - Increase inventory and marketing spend for high-margin categories.
   - Bundle best-selling products to increase average order value.

2. **Fix Underperforming Regions**
   - Introduce region-specific discounts or local campaigns.
   - Analyze logistics and delivery costs in low-profit regions.

3. **Product Portfolio Optimization**
   - Discontinue or reprice bottom 10 low-performing products.
   - Focus promotions on top 20% revenue-generating products.

4. **Revenue Growth Strategy**
   - Launch seasonal campaigns during high-growth months.
   - Implement loyalty programs to improve repeat purchases.

5. **Profit Improvement**
   - Review cost structure for categories with high sales but low profit.
   - Negotiate supplier costs for frequently sold products.
""")

st.success("✅ Dashboard ready for business decision-making and client presentation.")