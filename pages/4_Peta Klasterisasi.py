import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen

st.set_page_config(
    page_title="Peta Klasterisasi",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= CSS =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #f0f6ff;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.page-header {
    background: linear-gradient(135deg, #1565c0, #0288d1);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}
.page-title {
    font-size: 2.6rem;
    font-weight: 800;
    color: white;
}
.page-sub {
    color: #bbdefb;
}

.section-card {
    background: white;
    border-radius: 18px;
    border: 1px solid #d4e8f8;
    margin-bottom: 1rem;
}
.section-header {
    background: #e3f2fd;
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #d4e8f8;
}
.section-title {
    color: #1565c0;
    font-weight: 800;
}
.section-body {
    padding: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="page-header">
    <h1 class="page-title">PETA KLASTERISASI DAMPAK BANJIR</h1>
    <p class="page-sub">
        Visualisasi hasil klasterisasi wilayah terdampak banjir di Indonesia
    </p>
</div>
""", unsafe_allow_html=True)

# ================= VALIDASI DATA =================
if "df_clustered" not in st.session_state:
    st.warning("Silakan upload data dan lakukan klasterisasi terlebih dahulu!")
    st.stop()

df_result = st.session_state["df_clustered"].copy()

# ================= DATA TAMBAHAN =================
CENTROIDS = {
    "Aceh": (4.695135, 96.749397),
    "Sumatera Utara": (2.115201, 99.544901),
    "Sumatera Barat": (-0.739610, 100.800018),
    "Riau": (0.293416, 101.706939),
    "Jambi": (-1.612130, 103.611506),
    "Sumatera Selatan": (-3.319493, 103.914399),
    "Bengkulu": (-3.793099, 102.265930),
    "Lampung": (-4.557573, 105.406811),
    "Kepulauan Bangka Belitung": (-2.741051, 106.440849),
    "Kepulauan Riau": (3.945651, 108.142572),
    "Daerah Khusus Ibukota Jakarta": (-6.200000, 106.816666),
    "Jawa Barat": (-7.090911, 107.668887),
    "Jawa Tengah": (-7.150975, 110.140259),
    "Daerah Istimewa Yogyakarta": (-7.873590, 110.426100),
    "Jawa Timur": (-7.536064, 112.238631),
    "Banten": (-6.405688, 106.064384),
    "Bali": (-8.340539, 115.091949),
    "Nusa Tenggara Barat": (-8.652406, 117.361649),
    "Nusa Tenggara Timur": (-8.657383, 121.079813),
    "Kalimantan Barat": (-0.013819, 109.822035),
    "Kalimantan Tengah": (-1.681488, 113.382355),
    "Kalimantan Selatan": (-3.093091, 115.283460),
    "Kalimantan Timur": (1.640522, 116.419389),
    "Kalimantan Utara": (3.073099, 116.041513),
    "Sulawesi Utara": (0.624895, 123.975071),
    "Sulawesi Tengah": (-1.430247, 121.445017),
    "Sulawesi Selatan": (-3.662521, 119.974358),
    "Sulawesi Tenggara": (-4.144527, 122.174774),
    "Gorontalo": (0.544216, 123.058036),
    "Sulawesi Barat": (-2.843724, 119.232185),
    "Maluku": (-3.237018, 130.145440),
    "Maluku Utara": (1.570812, 127.808751),
    "Papua Barat": (-1.336248, 133.174698),
    "Papua Barat Daya": (-1.800000, 132.000000),
    "Papua": (-4.269928, 138.080353),
    "Papua Selatan": (-6.500000, 140.500000),
    "Papua Pegunungan": (-4.200000, 138.800000),
    "Papua Tengah": (-3.800000, 135.500000),
}

KODE_MAP = {
    "Aceh": 11, "Sumatera Utara": 12, "Sumatera Barat": 13,
    "Riau": 14, "Jambi": 15, "Sumatera Selatan": 16,
    "Bengkulu": 17, "Lampung": 18, "Kepulauan Bangka Belitung": 19,
    "Kepulauan Riau": 21, "Daerah Khusus Ibukota Jakarta": 31,
    "Jawa Barat": 32, "Jawa Tengah": 33, "Daerah Istimewa Yogyakarta": 34,
    "Jawa Timur": 35, "Banten": 36, "Bali": 51,
    "Nusa Tenggara Barat": 52, "Nusa Tenggara Timur": 53,
    "Kalimantan Barat": 61, "Kalimantan Tengah": 62,
    "Kalimantan Selatan": 63, "Kalimantan Timur": 64, "Kalimantan Utara": 65,
    "Sulawesi Utara": 71, "Sulawesi Tengah": 72, "Sulawesi Selatan": 73,
    "Sulawesi Tenggara": 74, "Gorontalo": 75, "Sulawesi Barat": 76,
    "Maluku": 81, "Maluku Utara": 82,
    "Papua Barat": 91, "Papua": 94,
    # Pemekaran 2022 — belum ada polygon di GeoJSON lama → ditampilkan sbg marker
    "Papua Barat Daya": None,
    "Papua Selatan": None,
    "Papua Pegunungan": None,
    "Papua Tengah": None,
}

ALIAS = {
    "DKI Jakarta": "Daerah Khusus Ibukota Jakarta",
    "Dki Jakarta": "Daerah Khusus Ibukota Jakarta",
    "D.K.I. Jakarta": "Daerah Khusus Ibukota Jakarta",
    "Jakarta": "Daerah Khusus Ibukota Jakarta",
    "DI Yogyakarta": "Daerah Istimewa Yogyakarta",
    "Di Yogyakarta": "Daerah Istimewa Yogyakarta",
    "D.I. Yogyakarta": "Daerah Istimewa Yogyakarta",
    "Yogyakarta": "Daerah Istimewa Yogyakarta",
    "Kep. Bangka Belitung": "Kepulauan Bangka Belitung",
    "Bangka Belitung": "Kepulauan Bangka Belitung",
    "Kep. Riau": "Kepulauan Riau",
}

def normalize_province(name: str) -> str:
    stripped = name.strip()
    if stripped in ALIAS:
        return ALIAS[stripped]
    titled = stripped.title()
    if titled in ALIAS:
        return ALIAS[titled]
    return stripped

df_result["Provinsi_norm"] = df_result["Provinsi"].apply(normalize_province)

# Label Klaster
df_result["label_klaster"] = df_result["Cluster"].apply(
    lambda x: "Noise" if x == -1 else f"Klaster {x}"
)

def sort_key(lbl):
    return 999 if lbl == "Noise" else int(lbl.split()[-1])

unique_labels = sorted(df_result["label_klaster"].unique(), key=sort_key)

color_map = {
    "Klaster 0": "#FFA500", 
    "Klaster 1": "#FF0000",
    "Klaster 2": "#FFFF00",
}

# Tambahkan default untuk klaster lain
for lbl in unique_labels:
    if lbl not in color_map:
        color_map[lbl] = "#3498DB" 

color_map["Noise"] = "#AAAAAA"

# Kolom Numerik
numeric_cols = (
    df_result.select_dtypes(include=np.number)
    .columns.drop(["Cluster"], errors="ignore")
    .tolist()
)

# Sidebar
with st.sidebar:
    st.header("Pengaturan Peta")
    map_style = st.selectbox(
        "Gaya Peta",
        ["carto-positron", "carto-darkmatter", "open-street-map", "white-bg"],
        index=0,
    )

    selected_hover = st.multiselect(
        "Data Hover",
        options=numeric_cols,
        default=numeric_cols 
    )

# Tambahkan Koordinat & Kode BPS
df_result["lat"] = df_result["Provinsi_norm"].map(
    lambda p: CENTROIDS.get(p, (None, None))[0]
)
df_result["lon"] = df_result["Provinsi_norm"].map(
    lambda p: CENTROIDS.get(p, (None, None))[1]
)
df_result["kode_bps"] = df_result["Provinsi_norm"].map(KODE_MAP)

missing_coord = df_result[df_result["lat"].isna()]["Provinsi"].tolist()
if missing_coord:
    st.warning(f"Provinsi tanpa koordinat: **{', '.join(missing_coord)}**")

df_map = df_result.dropna(subset=["lat", "lon"]).copy()

# ================= LOAD GEOJSON =================
@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/ans-4175/peta-indonesia-geojson/master/indonesia-prov.geojson"
    with urlopen(url) as resp:
        return json.load(resp)

geojson = load_geojson()

# ================= CARD: MAP =================
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <h2 class="section-title">Peta Klasterisasi</h2>
    </div>
    <div class="section-body">
""", unsafe_allow_html=True)

fig = px.choropleth_mapbox(
    df_map,
    geojson=geojson,
    locations="kode_bps",
    featureidkey="properties.kode",
    color="label_klaster",
    mapbox_style="carto-positron",
    zoom=3.8,
    center={"lat": -2.5, "lon": 118},
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# ================= DETAIL PROVINSI =================
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <h2 class="section-title">Detail Provinsi</h2>
    </div>
    <div class="section-body">
""", unsafe_allow_html=True)

selected_prov = st.selectbox("Pilih Provinsi", df_result["Provinsi"].unique())
data = df_result[df_result["Provinsi"] == selected_prov].iloc[0]

st.markdown(f"### {data['label_klaster']}")

cols = st.columns(3)
numeric_cols = df_result.select_dtypes(include=np.number).columns.drop("Cluster")

for i, col in enumerate(numeric_cols):
    cols[i % 3].metric(col, f"{data[col]:,.0f}")

st.markdown("</div></div>", unsafe_allow_html=True)

# ================= DOWNLOAD =================
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <h2 class="section-title">Download Data</h2>
    </div>
    <div class="section-body">
""", unsafe_allow_html=True)

csv = df_result.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "hasil.csv")

st.markdown("</div></div>", unsafe_allow_html=True)
