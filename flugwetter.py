import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

st.set_page_config(page_title="Hauchenberg Heliogramm", layout="wide")
st.title("🪂 Hauchenberg Heliogramm (ICON-D2)")

# 1. Wetterdaten laden
@st.cache_data(ttl=600)
def get_weather():
    url = "https://api.open-meteo.com/v1/dwd-icon?latitude=47.653&longitude=10.162&hourly=windspeed_10m,windspeed_925hPa,windspeed_850hPa,windspeed_800hPa,winddirection_10m,winddirection_925hPa,winddirection_850hPa,winddirection_800hPa&timezone=Europe%2FBerlin&forecast_days=2"
    return requests.get(url).json()

try:
    data = get_weather()["hourly"]
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time']).dt.strftime('%H:%00')
    
    # Wir nehmen nur die nächsten 18 Stunden für die Übersichtlichkeit
    df = df.head(18)

    # 2. Daten für Heatmap vorbereiten (Zeilen = Höhen, Spalten = Zeit)
    heights = ["2000m (800hPa)", "1500m (850hPa)", "800m (925hPa)", "Boden (10m)"]
    z_wind = [df['windspeed_800hPa'].tolist(), df['windspeed_850hPa'].tolist(), 
              df['windspeed_925hPa'].tolist(), df['windspeed_10m'].tolist()]
    
    # 3. Heliogramm Grafik bauen
    fig = go.Figure()

    # Hintergrund-Farben (Heatmap)
    fig.add_trace(go.Heatmap(
        z=z_wind, x=df['time'], y=heights,
        colorscale=[[0, 'green'], [0.5, 'yellow'], [1, 'red']],
        showscale=True, colorbar=dict(title="km/h")
    ))

    # Windpfeile oben drauf setzen
    for h_idx, h_key in enumerate(['800hPa', '850hPa', '925hPa', '10m']):
        for i in range(len(df)):
            fig.add_annotation(
                x=df['time'].iloc[i], y=heights[h_idx],
                text="↑", showarrow=False,
                font=dict(size=22, color="black"),
                textangle=df[f'winddirection_{h_key}'].iloc[i] + 180
            )

    fig.update_layout(height=500, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)
    
    st.success("Daten aktuell. Viel Erfolg am Hauchenberg!")

except Exception as e:
    st.error("Wetter-Server antwortet gerade nicht. Bitte Seite in 10 Sek. neu laden.")
    st.write(f"Technischer Fehler: {e}")
