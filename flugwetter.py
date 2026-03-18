import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.title("Hauchenberg Flugwetter")

# Daten abrufen
url = "https://api.open-meteo.com/v1/dwd-icon?latitude=47.653&longitude=10.162&hourly=windspeed_10m,winddirection_10m,temperature_2m&timezone=Europe%2FBerlin"
data = requests.get(url).json()

# Tabelle bauen
df = pd.DataFrame({
    "Zeit": pd.to_datetime(data["hourly"]["time"]),
    "Wind_kmh": data["hourly"]["windspeed_10m"],
    "Temp": data["hourly"]["temperature_2m"]
})

# Einfache Grafik
fig = px.line(df, x="Zeit", y=["Wind_kmh", "Temp"], title="Hauchenberg 3-Tage-Trend")
st.plotly_chart(fig)
