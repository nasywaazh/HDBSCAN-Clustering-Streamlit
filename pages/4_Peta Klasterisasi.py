import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen

st.set_page_config(
    page_title="Peta Klasterisasi Wilayah Terdampak Banjir",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #f0f6ff !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #1a3a5c;
}
[data-testid="stMain"] { background: #f0f6ff !important; }
.main .block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1080px !important;
}
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #d0e4f7 !important;
}
[data-testid="stSidebar"] * { color: #1a5fa8 !important; }

.page-header {
    background: linear-gradient(135deg, #1565c0 0%, #1976d2 55%, #0288d1 100%);
    border-radius: 20px;
    padding: 2.2rem 2.8rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}
.page-title {
    font-size: 3rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.25;
    margin: 0 0 0.6rem 0;
}
.page-sub {
    font-size: 1.1rem;
    color: #bbdefb;
    line-height: 1.7;
    margin: 0;
}

[data-testid="stMarkdownContainer"] h3 {
    background: linear-gradient(135deg, #e3f2fd 0%, #eff8ff 100%);
    border: 1px solid #c2dff5;
    border-radius: 12px;
    padding: 0.75rem 1.2rem;
    margin: 1.4rem 0 0.8rem 0;
    font-size: 1.1rem;
    font-weight: 800;
    color: #1565c0 !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

[data-testid="stMarkdownContainer"] h4 {
    font-size: 1rem;
    font-weight: 700;
    color: #1565c0 !important;
    margin: 1.2rem 0 0.6rem 0;
}

[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-size: 0.9rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

[data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label {
    font-weight: 700 !important;
    color: #1565c0 !important;
    font-size: 0.88rem !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #e8f4fd 0%, #f0f9ff 100%);
    border: 1px solid #c2dff5;
    border-radius: 14px;
    padding: 1rem 1.2rem !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    color: #7bafd4 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.5rem !important;
    font-weight: 800 !important;
    color: #1565c0 !important;
}

/* Download button */
[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #1565c0, #0288d1) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.4rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s ease !important;
}
[data-testid="stDownloadButton"] button:hover {
    opacity: 0.88 !important;
}

/* Divider */
hr {
    border: none !important;
    border-top: 1px solid #d0e4f7 !important;
    margin: 1.2rem 0 !important;
}

/* Map container card */
.map-card {
    background: #ffffff;
    border: 1px solid #c2dff5;
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1.2rem;
}

/* Sidebar header */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    background: linear-gradient(135deg, #e3f2fd 0%, #eff8ff 100%) !important;
    border: 1px solid #c2dff5 !important;
    border-radius: 10px !important;
    padding: 0.6rem 1rem !important;
    font-size: 0.95rem !important;
    font-weight: 800 !important;
    color: #1565c0 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    margin-bottom: 1rem !important;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #e8f4fd; }
::-webkit-scrollbar-thumb { background: #90caf9; border-radius: 3px; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"], .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ── HELPERS ─────────────────────────────────────────────────────────────────

def sec(title):
    st.markdown(f"### {title}")


def step_label(text):
    st.caption(f"🔹 {text.upper()}")


# ── PAGE HEADER ──────────────────────────────────────────────────────────────

st.markdown("""
<div class="page-header">
    <h1 class="page-title">PETA KLASTERISASI WILAYAH TERDAMPAK BANJIR DI INDONESIA</h1>
    <p class="page-sub">
        Visualisasi geografis hasil klasterisasi HDBSCAN pada seluruh provinsi di Indonesia
        berdasarkan indikator dampak banjir
    </p>
</div>
""", unsafe_allow_html=True)

if "df_clustered" not in st.session_state:
    st.warning("Silakan upload dataset dan lakukan proses klasterisasi terlebih dahulu!")
    st.stop()

df_result: pd.DataFrame = st.session_state["df_clustered"].copy()

# ── KOORDINAT & MAPPING ──────────────────────────────────────────────────────

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
for lbl in unique_labels:
    if lbl not in color_map:
        color_map[lbl] = "#3498DB"
color_map["Noise"] = "#AAAAAA"

numeric_cols = (
    df_result.select_dtypes(include=np.number)
    .columns.drop(["Cluster"], errors="ignore")
    .tolist()
)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### ⚙️ Pengaturan Peta")
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

# ── KOORDINAT & KODE BPS ─────────────────────────────────────────────────────

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

# ── GEOJSON ──────────────────────────────────────────────────────────────────

GEOJSON_URLS = [
    "https://raw.githubusercontent.com/ans-4175/peta-indonesia-geojson/master/indonesia-prov.geojson",
    "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-en.geojson",
]

@st.cache_data(show_spinner="Memuat GeoJSON…")
def load_geojson(urls):
    for url in urls:
        try:
            with urlopen(url, timeout=15) as resp:
                gj = json.load(resp)
            props = gj["features"][0]["properties"]
            for candidate in ["kode", "Kode", "KODE"]:
                if candidate in props and isinstance(props[candidate], (int, float)):
                    return gj, f"properties.{candidate}"
            for k, v in props.items():
                if isinstance(v, (int, float)) and 10 <= v <= 99:
                    return gj, f"properties.{k}"
            for k, v in props.items():
                if isinstance(v, str) and v.startswith("ID-"):
                    return gj, f"properties.{k}"
        except Exception:
            continue
    return None, None

geojson, feature_id_key = load_geojson(tuple(GEOJSON_URLS))

# ── SECTION 1: PETA ──────────────────────────────────────────────────────────

sec("1. PETA KLASTERISASI")
step_label("Distribusi Klaster Berdasarkan Indikator Dampak Banjir")

st.markdown('<div class="map-card">', unsafe_allow_html=True)

if geojson and feature_id_key:
    df_choropleth = df_map.dropna(subset=["kode_bps"]).copy()
    df_choropleth["kode_bps"] = df_choropleth["kode_bps"].astype(int)
    df_marker = df_map[df_map["kode_bps"].isna()].copy()

    hover_cols = {col: True for col in selected_hover}
    for c in ["kode_bps", "lat", "lon", "Provinsi_norm"]:
        hover_cols[c] = False

    fig = px.choropleth_mapbox(
        df_choropleth,
        geojson=geojson,
        locations="kode_bps",
        featureidkey=feature_id_key,
        color="label_klaster",
        color_discrete_map=color_map,
        category_orders={"label_klaster": unique_labels},
        hover_name="Provinsi",
        hover_data=hover_cols,
        mapbox_style=map_style,
        zoom=3.8,
        center={"lat": -2.5, "lon": 118},
        opacity=0.75,
        labels={"label_klaster": "Klaster"},
    )

    if not df_marker.empty:
        existing_labels = set(df_choropleth["label_klaster"].unique())
        for lbl in df_marker["label_klaster"].unique():
            sub = df_marker[df_marker["label_klaster"] == lbl]
            customdata = (
                sub[selected_hover].values
                if selected_hover
                else np.empty((len(sub), 0))
            )
            hover_lines = ["<b>%{text}</b>"] + [
                f"{col}: %{{customdata[{i}]}}" for i, col in enumerate(selected_hover)
            ]
            fig.add_trace(
                go.Scattermapbox(
                    lat=sub["lat"],
                    lon=sub["lon"],
                    mode="markers+text",
                    marker=dict(
                        size=22,
                        color=color_map.get(lbl, "#999"),
                        opacity=0.9,
                    ),
                    text=sub["Provinsi"],
                    textposition="top center",
                    textfont=dict(size=10, color="#333"),
                    customdata=customdata,
                    hovertemplate="<br>".join(hover_lines) + "<extra></extra>",
                    name=lbl,
                    legendgroup=lbl,
                    showlegend=(lbl not in existing_labels),
                )
            )

    fig.update_layout(
        margin={"r": 0, "t": 10, "l": 0, "b": 0},
        height=600,
        legend=dict(
            title="Klaster",
            orientation="v",
            x=0.01,
            y=0.98,
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor="#CCC",
            borderwidth=1,
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

    if not df_marker.empty:
        nama_pemekaran = ", ".join(sorted(df_marker["Provinsi"].tolist()))
        st.info(f"🗺️ Provinsi pemekaran ditampilkan sebagai marker: **{nama_pemekaran}**")

else:
    st.info("GeoJSON tidak dapat dimuat — menampilkan bubble map.")
    fig = go.Figure()
    for lbl in unique_labels:
        sub = df_map[df_map["label_klaster"] == lbl]
        customdata = (
            sub[selected_hover].values if selected_hover
            else np.empty((len(sub), 0))
        )
        hover_lines = ["<b>%{text}</b>", f"Klaster: {lbl}"] + [
            f"{col}: %{{customdata[{i}]}}" for i, col in enumerate(selected_hover)
        ]
        fig.add_trace(
            go.Scattermapbox(
                lat=sub["lat"], lon=sub["lon"],
                mode="markers+text",
                marker=dict(size=18, color=color_map.get(lbl, "#999"), opacity=0.85),
                text=sub["Provinsi"],
                textposition="top center",
                customdata=customdata,
                hovertemplate="<br>".join(hover_lines) + "<extra></extra>",
                name=lbl,
            )
        )
    fig.update_layout(
        mapbox_style=map_style,
        mapbox=dict(zoom=3.8, center={"lat": -2.5, "lon": 118}),
        margin={"r": 0, "t": 10, "l": 0, "b": 0},
        height=600,
        legend=dict(title="Klaster", bgcolor="rgba(255,255,255,0.85)"),
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── SECTION 2: DETAIL PROVINSI ───────────────────────────────────────────────

sec("2. DETAIL INFORMASI PROVINSI")
step_label("Pilih Provinsi untuk Melihat Detail Data")

selected_prov = st.selectbox(
    "Pilih Provinsi",
    sorted(df_result["Provinsi"].unique())
)
prov_data = df_result[df_result["Provinsi"] == selected_prov].iloc[0]

st.markdown(f"#### {prov_data['label_klaster']}")

cols = st.columns(3)
for i, col in enumerate(numeric_cols):
    cols[i % 3].metric(
        label=col.replace("_", " "),
        value=f"{prov_data[col]:,.0f}"
    )

# ── SECTION 3: DOWNLOAD ──────────────────────────────────────────────────────

sec("3. UNDUH HASIL KLASTERISASI")
step_label("Download data hasil klasterisasi dalam format CSV")

csv = (
    df_result.drop(
        columns=["Provinsi_norm", "lat", "lon", "kode_bps", "label_klaster"],
        errors="ignore",
    )
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(
    "⬇️ Download CSV",
    csv,
    "hasil_klasterisasi.csv",
    "text/csv"
)
