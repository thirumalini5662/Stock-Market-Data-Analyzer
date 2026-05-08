import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8001"

# 🔥 TITLE
st.title("📊 Smart Stock Analyzer")
st.caption("Analyze stocks, run strategies, and visualize trends")

# 🔹 INPUT
ticker = st.text_input("Enter Stock Ticker", "RELIANCE.NS")

# 🔹 REFRESH BUTTON
if st.button("Refresh Data"):
    r = requests.get(f"{API_URL}/refresh/{ticker}")
    st.success(r.json())

# 🔹 BACKTEST BUTTON
if st.button("Run Backtest"):
    r = requests.get(f"{API_URL}/backtest/{ticker}")
    data = r.json()

    if "error" in data:
        st.error(data["error"])
    else:
        st.success(f"Return: {data['total_return_percent']} %")

        # 📈 PROFIT STATUS
        if data["total_return_percent"] > 0:
            st.success("📈 Strategy Profitable")
        else:
            st.error("📉 Strategy Losing")

        # 🔥 BUY / SELL SIGNAL
        r_chart = requests.get(f"{API_URL}/chart/{ticker}")
        chart_data = r_chart.json()

        if isinstance(chart_data, list) and len(chart_data) > 50:
            df = pd.DataFrame(chart_data)
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)

            df["sma20"] = df["close"].rolling(20).mean()
            df["sma50"] = df["close"].rolling(50).mean()

            last = df.iloc[-1]

            if last["sma20"] > last["sma50"]:
                st.success("🟢 BUY SIGNAL")
            elif last["sma20"] < last["sma50"]:
                st.error("🔴 SELL SIGNAL")
            else:
                st.warning("⚪ HOLD")

# 🔹 CHART SECTION
st.subheader("📈 Price + Indicators")

r = requests.get(f"{API_URL}/chart/{ticker}")
data = r.json()

if isinstance(data, list) and len(data) > 0:
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)

    df["sma20"] = df["close"].rolling(20).mean()
    df["sma50"] = df["close"].rolling(50).mean()

    st.line_chart(df[["close", "sma20", "sma50"]])
else:
    st.warning("No chart data available")


