from dataclasses import dataclass

import pandas as pd

from config import REQUIRED_COLUMNS


class DataValidationError(ValueError):
    pass


def validate_sales_dataframe(sales: pd.DataFrame) -> None:
    missing = [col for col in REQUIRED_COLUMNS if col not in sales.columns]
    if missing:
        raise DataValidationError(f"Missing required columns: {', '.join(missing)}")

    if "session_id" not in sales.columns and "ga_session_id" not in sales.columns:
        raise DataValidationError("A `session_id` or `ga_session_id` column is required.")


def get_session_column(sales: pd.DataFrame) -> str:
    return "session_id" if "session_id" in sales.columns else "ga_session_id"


def _map_binary(series: pd.Series, true_label: str, false_label: str) -> pd.Series:
    def mapper(value):
        if pd.isna(value):
            return "Unknown"
        if value is True or value == 1 or str(value).lower() in {"1", "true"}:
            return true_label
        if value is False or value == 0 or str(value).lower() in {"0", "false"}:
            return false_label
        return "Unknown"

    return series.map(mapper)


@dataclass
class SalesMetrics:
    total_revenue: float
    total_orders: int
    total_sessions: int
    avg_item_value: float
    conversion_rate: float
    revenue_by_continent: pd.Series
    revenue_by_continent_pct: pd.Series
    revenue_by_country: pd.Series
    revenue_by_category: pd.Series
    revenue_by_device: pd.Series
    revenue_by_device_pct: pd.Series
    revenue_by_channel: pd.Series
    revenue_by_channel_pct: pd.Series
    revenue_by_traffic_source: pd.Series
    revenue_by_os: pd.Series
    revenue_by_browser: pd.Series
    monthly_revenue: pd.Series
    monthly_growth_pct: pd.Series
    revenue_by_weekday: pd.Series
    revenue_weekend_vs_weekday: pd.Series
    revenue_registered_vs_anon: pd.Series
    revenue_by_verification: pd.Series
    revenue_by_subscription: pd.Series
    date_min: str
    date_max: str
    has_date: bool

    def to_kpi_text(self) -> str:
        weekday_str = self.revenue_by_weekday.to_string() if self.has_date else "No data"
        weekend_str = self.revenue_weekend_vs_weekday.to_string() if self.has_date else "No data"
        monthly_rev_str = self.monthly_revenue.to_string() if self.has_date else "No data"
        monthly_gro_str = self.monthly_growth_pct.to_string() if self.has_date else "No data"

        return f"""
PERIOD: {self.date_min} to {self.date_max}
Total sessions: {self.total_sessions:,}
Total orders: {self.total_orders:,}
Total revenue: ${self.total_revenue:,.0f}

REVENUE BY CONTINENT (% of total):
{self.revenue_by_continent_pct.to_string()}

TOP 5 COUNTRIES BY REVENUE:
{self.revenue_by_country.to_string()}

TOP 5 PRODUCT CATEGORIES BY REVENUE:
{self.revenue_by_category.to_string()}

REVENUE BY DEVICE (% of total):
{self.revenue_by_device_pct.to_string()}

REVENUE BY TRAFFIC CHANNEL (% of total):
{self.revenue_by_channel_pct.to_string()}

TOP 5 TRAFFIC SOURCES BY REVENUE:
{self.revenue_by_traffic_source.to_string()}

TOP 5 OPERATING SYSTEMS BY REVENUE:
{self.revenue_by_os.to_string()}

TOP 5 BROWSERS BY REVENUE:
{self.revenue_by_browser.to_string()}

MONTHLY REVENUE:
{monthly_rev_str}

MONTH-OVER-MONTH GROWTH (%):
{monthly_gro_str}

REVENUE BY DAY OF WEEK:
{weekday_str}

WEEKEND VS WEEKDAY REVENUE:
{weekend_str}

REVENUE: ANONYMOUS VS REGISTERED USERS:
{self.revenue_registered_vs_anon.to_string()}

REGISTERED USERS — VERIFIED VS UNVERIFIED REVENUE:
{self.revenue_by_verification.to_string()}

REGISTERED USERS — SUBSCRIBED VS UNSUBSCRIBED REVENUE:
{self.revenue_by_subscription.to_string()}
"""


def _empty_series() -> pd.Series:
    return pd.Series(dtype=float)


def compute_metrics(sales: pd.DataFrame) -> SalesMetrics:
    validate_sales_dataframe(sales)

    session_col = get_session_column(sales)
    has_date = "date" in sales.columns

    total_revenue = float(sales["price"].sum())
    total_sessions = int(sales[session_col].nunique())

    if "order_id" in sales.columns:
        total_orders = int(sales["order_id"].dropna().nunique())
    else:
        total_orders = int(sales.loc[sales["price"].notna(), session_col].nunique())

    avg_item_value = total_revenue / total_orders if total_orders > 0 else 0.0
    conversion_rate = (total_orders / total_sessions * 100) if total_sessions > 0 else 0.0

    revenue_by_continent = (
        sales.groupby("continent")["price"].sum().sort_values(ascending=False)
        if "continent" in sales.columns
        else _empty_series()
    )
    revenue_by_continent_pct = (
        (revenue_by_continent / total_revenue * 100).round(2) if total_revenue > 0 else _empty_series()
    )

    revenue_by_country = (
        sales.groupby("country")["price"].sum().sort_values(ascending=False).head(5)
        if "country" in sales.columns
        else _empty_series()
    )
    revenue_by_category = (
        sales.groupby("product_category")["price"].sum().sort_values(ascending=False).head(5)
        if "product_category" in sales.columns
        else _empty_series()
    )

    revenue_by_device = (
        sales.groupby("device")["price"].sum().sort_values(ascending=False)
        if "device" in sales.columns
        else _empty_series()
    )
    revenue_by_device_pct = (
        (revenue_by_device / total_revenue * 100).round(2) if total_revenue > 0 else _empty_series()
    )

    revenue_by_channel = (
        sales.groupby("traffic_channel")["price"].sum().sort_values(ascending=False)
        if "traffic_channel" in sales.columns
        else _empty_series()
    )
    revenue_by_channel_pct = (
        (revenue_by_channel / total_revenue * 100).round(2) if total_revenue > 0 else _empty_series()
    )

    revenue_by_traffic_source = (
        sales.groupby("traffic_source")["price"].sum().sort_values(ascending=False).head(5)
        if "traffic_source" in sales.columns
        else _empty_series()
    )
    revenue_by_os = (
        sales.groupby("operating_system")["price"].sum().sort_values(ascending=False).head(5)
        if "operating_system" in sales.columns
        else _empty_series()
    )
    revenue_by_browser = (
        sales.groupby("browser")["price"].sum().sort_values(ascending=False).head(5)
        if "browser" in sales.columns
        else _empty_series()
    )

    monthly_revenue = _empty_series()
    monthly_growth_pct = _empty_series()
    revenue_by_weekday = _empty_series()
    revenue_weekend_vs_weekday = _empty_series()

    if has_date:
        sales_time = sales.set_index("date")
        monthly_revenue = sales_time.resample("ME")["price"].sum()
        monthly_growth_pct = (monthly_revenue.pct_change() * 100).round(2)

        weekday_df = sales.copy()
        weekday_df["day_of_week"] = weekday_df["date"].dt.day_name()
        revenue_by_weekday = (
            weekday_df.groupby("day_of_week")["price"]
            .sum()
            .reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        )

        weekday_df["is_weekend"] = weekday_df["date"].dt.dayofweek >= 5
        revenue_weekend_vs_weekday = weekday_df.groupby("is_weekend")["price"].sum()
        revenue_weekend_vs_weekday.index = revenue_weekend_vs_weekday.index.map(
            {False: "Weekday", True: "Weekend"}
        )

    revenue_registered_vs_anon = _empty_series()
    revenue_by_verification = _empty_series()
    revenue_by_subscription = _empty_series()

    if "registered_user_id" in sales.columns:
        user_df = sales.copy()
        user_df["is_registered"] = user_df["registered_user_id"].notna()
        revenue_registered_vs_anon = user_df.groupby("is_registered")["price"].sum()
        revenue_registered_vs_anon.index = revenue_registered_vs_anon.index.map(
            {False: "Anonymous", True: "Registered"}
        )

        registered = user_df[user_df["is_registered"]]
        if not registered.empty:
            if "is_verified" in registered.columns:
                revenue_by_verification = registered.groupby(
                    _map_binary(registered["is_verified"], "Verified", "Unverified")
                )["price"].sum()
            if "is_unsubscribed" in registered.columns:
                revenue_by_subscription = registered.groupby(
                    _map_binary(registered["is_unsubscribed"], "Unsubscribed", "Subscribed")
                )["price"].sum()

    date_min = sales["date"].min().date().isoformat() if has_date else "Unknown"
    date_max = sales["date"].max().date().isoformat() if has_date else "Unknown"

    return SalesMetrics(
        total_revenue=total_revenue,
        total_orders=total_orders,
        total_sessions=total_sessions,
        avg_item_value=avg_item_value,
        conversion_rate=conversion_rate,
        revenue_by_continent=revenue_by_continent,
        revenue_by_continent_pct=revenue_by_continent_pct,
        revenue_by_country=revenue_by_country,
        revenue_by_category=revenue_by_category,
        revenue_by_device=revenue_by_device,
        revenue_by_device_pct=revenue_by_device_pct,
        revenue_by_channel=revenue_by_channel,
        revenue_by_channel_pct=revenue_by_channel_pct,
        revenue_by_traffic_source=revenue_by_traffic_source,
        revenue_by_os=revenue_by_os,
        revenue_by_browser=revenue_by_browser,
        monthly_revenue=monthly_revenue,
        monthly_growth_pct=monthly_growth_pct,
        revenue_by_weekday=revenue_by_weekday,
        revenue_weekend_vs_weekday=revenue_weekend_vs_weekday,
        revenue_registered_vs_anon=revenue_registered_vs_anon,
        revenue_by_verification=revenue_by_verification,
        revenue_by_subscription=revenue_by_subscription,
        date_min=date_min,
        date_max=date_max,
        has_date=has_date,
    )
