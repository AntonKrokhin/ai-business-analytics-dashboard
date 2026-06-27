import pandas as pd
import plotly.express as px
import streamlit as st

from ai_report import generate_ai_report
from metrics import DataValidationError, SalesMetrics, compute_metrics

st.set_page_config(
    page_title="AI Business Analytics Dashboard",
    layout="wide",
)

if "ai_report" not in st.session_state:
    st.session_state.ai_report = None


def render_kpi_cards(metrics: SalesMetrics) -> None:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${metrics.total_revenue:,.2f}")
    col2.metric("Unique Sessions", f"{metrics.total_sessions:,}")
    col3.metric("Total Orders", f"{metrics.total_orders:,}")


def render_charts(metrics: SalesMetrics) -> None:
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("Top 5 Countries by Revenue")
        if not metrics.revenue_by_country.empty:
            fig_country = px.bar(
                metrics.revenue_by_country.reset_index(),
                x="country",
                y="price",
                labels={"price": "Revenue ($)", "country": "Country"},
                color="price",
                color_continuous_scale="Mint",
            )
            st.plotly_chart(fig_country, use_container_width=True)
        else:
            st.info("No country data available.")

    with row1_col2:
        st.subheader("Top 5 Categories by Revenue")
        if not metrics.revenue_by_category.empty:
            fig_cat = px.bar(
                metrics.revenue_by_category.reset_index(),
                x="product_category",
                y="price",
                labels={"price": "Revenue ($)", "product_category": "Category"},
                color="price",
                color_continuous_scale="Mint",
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("No category data available.")

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.subheader("Revenue by Device (%)")
        if not metrics.revenue_by_device_pct.empty:
            fig_device = px.bar(
                metrics.revenue_by_device_pct.reset_index(),
                x="device",
                y="price",
                labels={"price": "% of Total Revenue", "device": "Device"},
                color="price",
                color_continuous_scale="Mint",
            )
            st.plotly_chart(fig_device, use_container_width=True)
        else:
            st.info("No device data available.")

    with row2_col2:
        st.subheader("Revenue by Channel (%)")
        if not metrics.revenue_by_channel_pct.empty:
            fig_channel = px.bar(
                metrics.revenue_by_channel_pct.reset_index(),
                x="traffic_channel",
                y="price",
                labels={"price": "% of Total Revenue", "traffic_channel": "Channel"},
                color="price",
                color_continuous_scale="Mint",
            )
            st.plotly_chart(fig_channel, use_container_width=True)
        else:
            st.info("No channel data available.")


st.title("AI Business Analytics Dashboard")

uploaded_file = st.file_uploader(
    "Upload a sales CSV file for analytics and an AI-generated report",
    type=["csv"],
)

if uploaded_file is None:
    st.info("Upload a CSV file to launch the dashboard.")
    st.stop()

try:
    sales = pd.read_csv(uploaded_file)
    if "date" in sales.columns:
        sales["date"] = pd.to_datetime(sales["date"])
except Exception as exc:
    st.error(f"Failed to read CSV: {exc}")
    st.stop()

try:
    metrics = compute_metrics(sales)
except DataValidationError as exc:
    st.error(str(exc))
    st.stop()
except Exception as exc:
    st.error(f"Failed to compute metrics: {exc}")
    st.stop()

st.success(f"Loaded {len(sales):,} rows | Period: {metrics.date_min} → {metrics.date_max}")

st.divider()
render_kpi_cards(metrics)
st.divider()
render_charts(metrics)
st.divider()

st.subheader("AI Report")
col_btn, col_dl = st.columns([3, 1])

with col_btn:
    generate_clicked = st.button("Generate Analytics Report", use_container_width=True)

if generate_clicked:
    st.session_state.ai_report = None
    with st.spinner("AI is analyzing metrics..."):
        try:
            st.session_state.ai_report = generate_ai_report(metrics)
        except Exception as exc:
            st.error(f"Groq API error: {exc}")

if st.session_state.ai_report:
    st.markdown(st.session_state.ai_report)
