import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.title("PETA INTERAKTIF KLASTERISASI DAMPAK BANJIR")

# =========================
# VALIDASI DATA
# =========================
if "cluster_labels" not in st.session_state or "data" not in st.session_state:
    st.warning("Silakan lakukan klasterisasi terlebih dahulu!")
    st.stop()

df = st.session_state["data"].copy()
df["Cluster"] = st.session_state["cluster_labels"]

# Label cluster (termasuk noise)
df["Klaster"] = df["Cluster"].apply(
    lambda x: "Noise (-1)" if x == -1 else f"Klaster {x}"
)

# =========================
# FILTER KLASTER (INTERAKTIF)
# =========================
cluster_options = ["Semua"] + sorted(df["Klaster"].unique())
selected_cluster = st.selectbox("Pilih Klaster", cluster_options)

if selected_cluster != "Semua":
    df = df[df["Klaster"] == selected_cluster]

# =========================
# MAPPING NAMA PROVINSI
# =========================
mapping = {
    "ACEH": "DI. ACEH",
    "DI YOGYAKARTA": "DAERAH ISTIMEWA YOGYAKARTA",
    "KEPULAUAN BANGKA BELITUNG": "BANGKA BELITUNG",
    "NUSA TENGGARA BARAT": "NUSATENGGARA BARAT",
    "PAPUA BARAT DAYA": "PAPUA BARAT",
    "PAPUA PEGUNUNGAN": "PAPUA",
    "PAPUA SELATAN": "PAPUA",
    "PAPUA TENGAH": "PAPUA",
}

df["Provinsi_Map"] = df["Provinsi"].str.upper().replace(mapping)

# =========================
# LOAD GEOJSON
# =========================
@st.cache_data
def load_geojson():
    with open("indonesia-prov.geojson", "r") as f:
        return json.load(f)

geojson = load_geojson()

# =========================
# KOLOM NUMERIK
# =========================
numeric_cols = [
    c for c in df.select_dtypes(include="number").columns
    if c != "Cluster"
]

# =========================
# WARNA KLASTER
# =========================
palette = px.colors.qualitative.Set2
cluster_labels_sorted = sorted(df["Cluster"].unique())

color_map = {}
color_idx = 0

for c in cluster_labels_sorted:
    if c == -1:
        color_map["Noise (-1)"] = "#bbbbbb"
    else:
        color_map[f"Klaster {c}"] = palette[color_idx % len(palette)]
        color_idx += 1

category_order = [
    f"Klaster {c}" for c in cluster_labels_sorted if c != -1
] + ["Noise (-1)"]

# =========================
# HOVER CUSTOM
# =========================
df["hover_text"] = df.apply(
    lambda row: (
        f"<b>{row['Provinsi']}</b><br>"
        f"<b>Klaster:</b> {row['Klaster']}<br><br>"
        + "<br>".join([
            f"<b>{col}:</b> {int(row[col]):,}"
            for col in numeric_cols
        ])
    ),
    axis=1
)

# =========================
# PETA CHOROPLETH
# =========================
fig = px.choropleth(
    df,
    geojson=geojson,
    locations="Provinsi_Map",
    featureidkey="properties.Propinsi",
    color="Klaster",
    color_discrete_map=color_map,
    category_orders={"Klaster": category_order},
    custom_data=["hover_text"]
)

fig.update_traces(
    hovertemplate="%{customdata[0]}<extra></extra>"
)

fig.update_geos(
    fitbounds="locations",
    visible=False,
    bgcolor="#f0f4f8"
)

fig.update_layout(
    title=dict(
        text="Peta Klasterisasi Dampak Banjir di Indonesia",
        x=0.5
    ),
    margin={"r": 10, "t": 50, "l": 10, "b": 10},
    legend=dict(
        title="Klaster",
        bgcolor="rgba(255,255,255,0.85)"
    ),
    height=650
)

st.plotly_chart(fig, use_container_width=True)
