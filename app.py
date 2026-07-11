import streamlit as st
import pandas as pd
import datetime
import requests

st.title("🦅 Institutional Earnings Engine (Diagnostic Mode)")

# 1. Check Secrets
try:
    API_KEY = st.secrets["POLYGON_API_KEY"]
    st.success("🔒 API Key loaded securely from vault.")
except Exception as e:
    st.error(f"🔒 Vault Configuration Error: {e}")
    st.stop()

# 2. Simple Toggle Test
st.write("### 🎛️ Test Control Horizon")
time_horizon = st.radio(
    "Toggle this radio button to test server stability:",
    options=["7-Day Window", "30-Day Outlook"]
)
st.write(f"Selected Option: **{time_horizon}**")

# 3. Primitive Data Fetch
st.write("### 📊 Pulling Live Data...")

url = f"https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2026-06-01/2026-07-01?adjusted=true&sort=asc&apiKey={API_KEY}"

try:
    res = requests.get(url, timeout=10)
    if res.status_code == 200:
        data = res.json()
        if 'results' in data and len(data['results']) > 0:
            latest_close = data['results'][-1]['c']
            st.metric(label="Apple (AAPL) Last Close", value=f"${latest_close}")
        else:
            st.warning("Connected to Polygon, but no data records returned.")
    else:
        st.error(f"Polygon API Connection Failed. Status Code: {res.status_code}")
except Exception as e:
    st.error(f"Network error occurred: {e}")
