import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.title("Peta Klasterisasi")

# ambil data hasil clustering
if "df_clustered" not in st.session_state:
    st.warning("Lakukan klasterisasi dulu!")
    st.stop()

df = st.session_state["df_clustered"]

# load geojson
url = "https://raw.githubusercontent.com/ans-4175/peta-indonesia-geojson/master/indonesia-prov.geojson"
geojson = json.loads(pd.read_json(url).to_json())

# samakan nama
df["Provinsi"] = df["Provinsi"].str.upper().str.strip()

# plot
fig = px.choropleth(
    df,
    geojson=geojson,
    locations="Provinsi",
    featureidkey="properties.Propinsi",
    color="Cluster",
    color_continuous_scale="Set2",
)

fig.update_geos(fitbounds="locations", visible=False)

st.plotly_chart(fig)
