import pandas as pd
from plotly import express as px
from plotly import graph_objects as go
import streamlit as st

st.title("Stock Price App")


@st.cache_data
def load_data():
    df = pd.read_csv("data/market_cap.csv")
    df["Date"] = pd.to_datetime(df["Date"], format="ISO8601", utc=True)
    return df


@st.cache_data
def draw_chart(df: pd.DataFrame, frequency: str = "Q") -> go.Figure:
    periodic = df.groupby(
        ["Ticker", pd.PeriodIndex(df["Date"], freq=frequency)], as_index=False
    ).median()
    periodic = periodic.sort_values(["Date"], ascending=True, ignore_index=True)
    periodic["MarketCap"] = periodic.groupby("Ticker")["MarketCap"].transform(
        lambda x: x.interpolate()
    )

    fig = px.bar(
        periodic,
        x="Ticker",
        y="MarketCap",
        color="Ticker",
        barmode="group",
        animation_frame="Date",
        animation_group="Ticker",
        # range_y=[0, periodic["MarketCap"].max()],
        title="Yahoo Finance Market Cap",
        category_orders={"Ticker": sorted(periodic["Ticker"].unique())},
        height=600,
    )
    fig.update_traces(width=1)
    fig.update_layout(bargap=1)

    return fig


df = load_data()

frequency = st.radio("Granularity", ["Q", "M", "w"], index=0)

plot = draw_chart(df, frequency=frequency)

st.plotly_chart(plot)
