import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

st.set_page_config(page_title="Hauchenberg Profi", layout="wide")
st.title("🪂 Hauchenberg Höhenwind-Profil")

# 1. Daten für verschiedene Höhen abrufen (Boden, 925hPa, 850hPa, 800hPa)
url = "https://api.open-meteo.com/v1/dwd-icon?latitude=47.653&longitude=10.162&hourly=windspeed_10m,windspeed_925hPa,windspeed_850hPa,windspeed_800hPa,winddirection_10m,winddirection_925hPa,winddirection_850hPa,winddirection_800hPa&timezone=Europe%2FBerlin&forecast_days=2"

try:
    data = requests.get(url).json()["hourly"]
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])

    # 2. Grafik erstellen (Heliogramm-Style)
    fig = go.Figure()

    # Wir definieren die Höhenstufen (ca. 700m, 800m, 1500m, 2000m)
    heights = [("Boden", "10m"), ("800m", "925hPa"), ("1500m", "850hPa"), ("2000m", "800hPa")]

    for label, h_key in heights:
        speed_key = f"windspeed_{h_key}"
        dir_key = f"winddirection_{h_key}"
        
        # Wind-Linie für jede Höhe
        fig.add_trace(go.Scatter(
            x=df['time'], y=[label] * len(df),
            mode='text',
            text=["↑"] * len(df), # Pfeil-Symbol
            textfont=dict(size=20, color="black"),
            textangle=df[dir_key] + 180, # Richtung anpassen
            name=label,
            hovertext=df[speed_key].astype(str) + " km/h"
        ))

    fig.update_layout(
        height=600,
        title="Windrichtung und Stärke nach Höhe",
        xaxis_title="Uhrzeit",
        yaxis_title="Höhe MSL",
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)
    st.info("Die Pfeile zeigen an, woher der Wind weht. 'Oben' im Bild ist Norden.")

except Exception as e:
    st.error(f"Fehler beim Laden der Profi-Daten: {e}")
