import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.title("Peta Klasterisasi")

# =========================
# DATA
# =========================
if "df_clustered" not in st.session_state:
    st.warning("Silakan lakukan klasterisasi terlebih dahulu!")
    st.stop()

df = st.session_state["df_clustered"]

# =========================
# CLEANING
# =========================
df["Provinsi"] = df["Provinsi"].str.upper().str.strip()

mapping = {
    "DKI JAKARTA": "DAERAH KHUSUS IBUKOTA JAKARTA",
    "DI YOGYAKARTA": "DAERAH ISTIMEWA YOGYAKARTA",
    "KEP. BANGKA BELITUNG": "KEPULAUAN BANGKA BELITUNG",
    "KEP. RIAU": "KEPULAUAN RIAU"
}

df["Provinsi"] = df["Provinsi"].replace(mapping)
df["Cluster"] = df["Cluster"].astype(str)

# =========================
# GEOJSON
# =========================
url = "https://raw.githubusercontent.com/ans-4175/peta-indonesia-geojson/master/indonesia-prov.geojson"
geojson = requests.get(url).json()

# =========================
# WARNA
# =========================
color_map = {
    "0": "#66c2a5",
    "1": "#fc8d62",
    "2": "#8da0cb",
    "-1": "#d3d3d3"
}

# =========================
# PLOT
# =========================
fig = px.choropleth(
    df,
    geojson=geojson,
    locations="Provinsi",
    featureidkey="properties.Propinsi",
    color="Cluster",
    color_discrete_map=color_map,
    hover_name="Provinsi"
)

fig.update_geos(
    fitbounds="locations",
    visible=False
)

st.plotly_chart(fig, use_container_width=True)
