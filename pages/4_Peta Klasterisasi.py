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
df["Cluster_Label"] = df["Cluster"].apply(
    lambda x: "Noise (-1)" if x == -1 else f"Klaster {x}"
)

# =========================
# MAPPING NAMA PROVINSI
# =========================
mapping = {
    "ACEH"                      : "DI. ACEH",
    "DI YOGYAKARTA"             : "DAERAH ISTIMEWA YOGYAKARTA",
    "KEPULAUAN BANGKA BELITUNG" : "BANGKA BELITUNG",
    "NUSA TENGGARA BARAT"       : "NUSATENGGARA BARAT",
    "PAPUA BARAT DAYA"          : "PAPUA BARAT",
    "PAPUA PEGUNUNGAN"          : "PAPUA",
    "PAPUA SELATAN"             : "PAPUA",
    "PAPUA TENGAH"              : "PAPUA",
}
df["Provinsi_Map"] = df["Provinsi"].str.upper().replace(mapping)

# =========================
# LOAD GEOJSON LOKAL
# =========================
@st.cache_data
def load_geojson():
    with open("indonesia-prov.geojson", "r") as f:
        return json.load(f)

geojson = load_geojson()

# =========================
# VARIABEL NUMERIK
# =========================
numeric_cols = [c for c in df.select_dtypes(include="number").columns if c != "Cluster"]

# =========================
# WARNA DISKRIT PER KLASTER
# =========================
palette = px.colors.qualitative.Set2
cluster_labels_sorted = sorted(df["Cluster"].unique())
color_map = {}
color_idx = 0
for c in cluster_labels_sorted:
    if c == -1:
        color_map["Noise (-1)"] = "#aaaaaa"
    else:
        color_map[f"Klaster {c}"] = palette[color_idx % len(palette)]
        color_idx += 1

category_order = [f"Klaster {c}" for c in cluster_labels_sorted if c != -1] + ["Noise (-1)"]

# =========================
# PETA CHOROPLETH
# =========================
fig = px.choropleth(
    df,
    geojson=geojson,
    locations="Provinsi_Map",
    featureidkey="properties.Propinsi",
    color="Cluster_Label",
    color_discrete_map=color_map,
    hover_name="Provinsi",
    hover_data={col: True for col in numeric_cols} | {
        "Cluster_Label": True,
        "Provinsi_Map": False
    },
    title="Peta Klasterisasi Dampak Banjir di Indonesia",
    category_orders={"Cluster_Label": category_order}
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    legend_title_text="Klaster",
    height=600
)
st.plotly_chart(fig, use_container_width=True)
