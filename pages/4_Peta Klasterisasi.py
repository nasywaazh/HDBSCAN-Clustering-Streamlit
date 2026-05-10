import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen

try:
    from papua_geom import PAPUA_GEOM
    PAPUA_GEOM_AVAILABLE = True
except ImportError:
    PAPUA_GEOM_AVAILABLE = False

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
    font-size: 1.05rem;
    font-weight: 800;
    color: #1565c0 !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* METRIC CARDS */
.metric-grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin: 0.8rem 0 1rem 0; }
.metric-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 0.8rem 0 1rem 0; }
.metric-grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 0.8rem 0 1rem 0; }
.metric-card {
    background: linear-gradient(135deg, #e8f4fd 0%, #f0f9ff 100%);
    border: 1px solid #c2dff5;
    border-radius: 14px;
    padding: 1.1rem 1.2rem;
    text-align: center;
}
.metric-label {
    font-size: 1rem;
    font-weight: 700;
    color: #7bafd4;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin: 0 0 0.5rem 0;
}
.metric-value {
    font-size: 1.4rem;
    font-weight: 800;
    color: #1565c0;
    line-height: 1;
    margin: 0;
}
.metric-card.klaster-0  { border-color: #E07B39; background: linear-gradient(135deg, #fff3e0, #fff8f0); }
.metric-card.klaster-0 .metric-value { color: #bf5f1a; }
.metric-card.klaster-0 .metric-label { color: #e07b39; }
.metric-card.klaster-1  { border-color: #C0392B; background: linear-gradient(135deg, #fdecea, #fff5f5); }
.metric-card.klaster-1 .metric-value { color: #922b21; }
.metric-card.klaster-1 .metric-label { color: #c0392b; }
.metric-card.klaster-2  { border-color: #c8a800; background: linear-gradient(135deg, #fffde7, #fffff5); }
.metric-card.klaster-2 .metric-value { color: #9a7d0a; }
.metric-card.klaster-2 .metric-label { color: #b8960c; }
.metric-card.noise { border-color: #90a4ae; background: linear-gradient(135deg, #eceff1, #f5f7f8); }
.metric-card.noise .metric-value { color: #546e7a; }
.metric-card.noise .metric-label { color: #78909c; }

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

/* SAFE TABLE */
.safe-table-wrap {
    overflow-x: auto; overflow-y: auto;
    max-height: 420px; border-radius: 10px;
    border: 1px solid #d4e8f8; margin-bottom: 1rem;
}
.safe-table-wrap thead th {
    position: sticky; top: 0; z-index: 2;
    background: linear-gradient(135deg, #e3f2fd, #eff8ff);
}
.safe-table-wrap table {
    width: 100%; border-collapse: collapse;
    font-size: 0.82rem; font-family: 'Plus Jakarta Sans', sans-serif;
    background: #ffffff;
}
.safe-table-wrap th {
    padding: 0.6rem 0.9rem; text-align: left; font-weight: 700;
    color: #1565c0; border-bottom: 1px solid #d4e8f8; white-space: nowrap;
}
.safe-table-wrap td { padding: 0.5rem 0.9rem; color: #1a3a5c; border-bottom: 1px solid #eaf4fc; }
.safe-table-wrap tr:last-child td { border-bottom: none; }
.safe-table-wrap tr:hover td { background: #f0f9ff; }

/* PROVINCE DETAIL HEADER */
.prov-header {
    background: linear-gradient(135deg, #e3f2fd 0%, #eff8ff 100%);
    border: 1px solid #c2dff5;
    border-radius: 14px;
    padding: 1.2rem 1.6rem;
    margin-bottom: 1rem;
}
.prov-name { font-size: 1.4rem; font-weight: 800; color: #1565c0; margin: 0 0 0.75rem 0; }
.prov-meta {
    display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center;
}
.badge {
    display: inline-block; font-size: 0.78rem; font-weight: 700;
    letter-spacing: 0.06em; padding: 0.3rem 0.9rem;
    border-radius: 20px; text-transform: uppercase; white-space: nowrap;
}
.badge-klaster   { background: linear-gradient(135deg, #1565c0, #0288d1); color: #fff; }
.badge-noise     { background: #b0bec5; color: #fff; }
.badge-label     {
    background: #e3f2fd; color: #1565c0;
    border: 1px solid #c2dff5; font-weight: 600;
    text-transform: none; letter-spacing: 0;
    font-size: 0.82rem; padding: 0.3rem 0.9rem;
}

/* DOWNLOAD */
[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #1565c0, #0288d1) !important;
    color: #ffffff !important; border: none !important;
    border-radius: 10px !important; font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 0.88rem !important;
    padding: 0.55rem 1.4rem !important; cursor: pointer !important;
}
[data-testid="stDownloadButton"] button:hover { opacity: 0.88 !important; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #e8f4fd; }
::-webkit-scrollbar-thumb { background: #90caf9; border-radius: 3px; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"], .stDeployButton { display: none; }
[data-testid="stSelectbox"] > div > div > div[data-baseweb="select"] ~ div { display: none !important; }
</style>
""", unsafe_allow_html=True)


# HELPERS
def sec(title):
    st.markdown(f"### {title}")


# LABEL CONFIGS
LEGEND_LABEL = {
    0:  "Klaster 0 – Moderat (Pengungsian & Genangan Tinggi)",
    1:  "Klaster 1 – Tinggi (Fatalitas & Kerusakan Struktural Tinggi)",
    2:  "Klaster 2 – Rendah",
    -1: "Noise – Ekstrem",
}

SHORT_LABEL = {
    0:  "Klaster 0",
    1:  "Klaster 1",
    2:  "Klaster 2",
    -1: "Noise",
}

FULL_LABEL = {
    0:  "Klaster 0 - Moderat (Pengungsian & Genangan Tinggi)",
    1:  "Klaster 1 - Tinggi (Fatalitas & Kerusakan Struktural Tinggi)",
    2:  "Klaster 2 - Rendah",
    -1: "Noise - Ekstrem",
}

COLOR_PALETTE = {
    0:  "#E07B39",
    1:  "#C0392B",
    2:  "#D4AC0D",
    -1: "#AAAAAA",
}

CARD_CLASS = {
    0:  "klaster-0",
    1:  "klaster-1",
    2:  "klaster-2",
    -1: "noise",
}

PEMEKARAN_LIST = ["Papua Barat Daya", "Papua Selatan", "Papua Pegunungan", "Papua Tengah"]


# PAGE HEADER (guard)
if "df_clustered" not in st.session_state:
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">PETA KLASTERISASI WILAYAH TERDAMPAK BANJIR DI INDONESIA</h1>
        <p class="page-sub">Visualisasi geospasial hasil klasterisasi provinsi di Indonesia berdasarkan
        indikator dampak banjir menggunakan algoritma HDBSCAN dan Bayesian Optimization</p>
    </div>""", unsafe_allow_html=True)
    st.warning("Silakan upload dataset dan lakukan proses klasterisasi terlebih dahulu!")
    st.stop()

df_result: pd.DataFrame = st.session_state["df_clustered"].copy()

# KOORDINAT & MAPPING
CENTROIDS = {
    "Aceh": (4.695135, 96.749397), "Sumatera Utara": (2.115201, 99.544901),
    "Sumatera Barat": (-0.739610, 100.800018), "Riau": (0.293416, 101.706939),
    "Jambi": (-1.612130, 103.611506), "Sumatera Selatan": (-3.319493, 103.914399),
    "Bengkulu": (-3.793099, 102.265930), "Lampung": (-4.557573, 105.406811),
    "Kepulauan Bangka Belitung": (-2.741051, 106.440849),
    "Kepulauan Riau": (3.945651, 108.142572),
    "Daerah Khusus Ibukota Jakarta": (-6.200000, 106.816666),
    "Jawa Barat": (-7.090911, 107.668887), "Jawa Tengah": (-7.150975, 110.140259),
    "Daerah Istimewa Yogyakarta": (-7.873590, 110.426100),
    "Jawa Timur": (-7.536064, 112.238631), "Banten": (-6.405688, 106.064384),
    "Bali": (-8.340539, 115.091949), "Nusa Tenggara Barat": (-8.652406, 117.361649),
    "Nusa Tenggara Timur": (-8.657383, 121.079813),
    "Kalimantan Barat": (-0.013819, 109.822035),
    "Kalimantan Tengah": (-1.681488, 113.382355),
    "Kalimantan Selatan": (-3.093091, 115.283460),
    "Kalimantan Timur": (1.640522, 116.419389),
    "Kalimantan Utara": (3.073099, 116.041513),
    "Sulawesi Utara": (0.624895, 123.975071), "Sulawesi Tengah": (-1.430247, 121.445017),
    "Sulawesi Selatan": (-3.662521, 119.974358),
    "Sulawesi Tenggara": (-4.144527, 122.174774),
    "Gorontalo": (0.544216, 123.058036), "Sulawesi Barat": (-2.843724, 119.232185),
    "Maluku": (-3.237018, 130.145440), "Maluku Utara": (1.570812, 127.808751),
    "Papua Barat": (-1.336248, 133.174698),
    "Papua Barat Daya": (-2.533293, 132.526978),
    "Papua": (-2.500000, 137.000000),
    "Papua Selatan": (-7.321823, 139.901685),
    "Papua Pegunungan": (-4.200000, 138.850000),
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
    "Papua Barat": 91, "Papua Barat Daya": 92,
    "Papua": 94, "Papua Selatan": 95,
    "Papua Pegunungan": 96, "Papua Tengah": 97,
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
    if stripped in ALIAS: return ALIAS[stripped]
    titled = stripped.title()
    if titled in ALIAS: return ALIAS[titled]
    return stripped


# DATA PREP
df_result["Provinsi_norm"] = df_result["Provinsi"].apply(normalize_province)
df_result["cluster_num"]   = df_result["Cluster"]
df_result["label_klaster"] = df_result["cluster_num"].apply(
    lambda n: LEGEND_LABEL.get(n, f"Klaster {n}")
)
df_result["lat"]      = df_result["Provinsi_norm"].map(lambda p: CENTROIDS.get(p, (None, None))[0])
df_result["lon"]      = df_result["Provinsi_norm"].map(lambda p: CENTROIDS.get(p, (None, None))[1])
df_result["kode_bps"] = df_result["Provinsi_norm"].map(KODE_MAP)

all_cluster_nums = sorted(df_result["cluster_num"].unique(), key=lambda x: (x == -1, x))
unique_labels    = [LEGEND_LABEL.get(n, f"Klaster {n}") for n in all_cluster_nums]
COLOR_MAP        = {LEGEND_LABEL.get(n, f"Klaster {n}"): COLOR_PALETTE.get(n, "#3498DB")
                    for n in all_cluster_nums}

numeric_cols = (
    df_result.select_dtypes(include=np.number)
    .columns.drop(["Cluster", "cluster_num"], errors="ignore")
    .tolist()
)

# PAGE HEADER
st.markdown("""
<div class="page-header">
    <h1 class="page-title">PETA KLASTERISASI WILAYAH TERDAMPAK BANJIR DI INDONESIA</h1>
    <p class="page-sub">
        Visualisasi geospasial hasil klasterisasi provinsi di Indonesia berdasarkan indikator
        dampak banjir menggunakan algoritma HDBSCAN dan Bayesian Optimization
    </p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR
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
        default=numeric_cols,
    )

# LOAD & PATCH GEOJSON
GEOJSON_URLS = [
    "https://raw.githubusercontent.com/ans-4175/peta-indonesia-geojson/master/indonesia-prov.geojson",
    "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-en.geojson",
]


@st.cache_data(show_spinner="Memuat GeoJSON…")
def load_and_patch_geojson(urls, papua_geom_available: bool):
    geojson = None
    feature_id_key = None
    prop_key = None

    for url in urls:
        try:
            with urlopen(url, timeout=15) as resp:
                gj = json.load(resp)
            props = gj["features"][0]["properties"]
            for candidate in ["kode", "Kode", "KODE"]:
                if candidate in props and isinstance(props[candidate], (int, float)):
                    feature_id_key = f"properties.{candidate}"
                    prop_key = candidate
                    geojson = gj
                    break
            if feature_id_key is None:
                for k, v in props.items():
                    if isinstance(v, (int, float)) and 10 <= v <= 99:
                        feature_id_key = f"properties.{k}"
                        prop_key = k
                        geojson = gj
                        break
            if geojson:
                break
        except Exception:
            continue

    if geojson is None:
        return None, None

    if not papua_geom_available:
        return geojson, feature_id_key

    from papua_geom import PAPUA_GEOM
    geojson = json.loads(json.dumps(geojson))
    new_features = []
    for feat in geojson["features"]:
        kode = int(feat["properties"].get(prop_key, 0))
        if kode in (91, 94) and kode in PAPUA_GEOM:
            feat = json.loads(json.dumps(feat))
            feat["geometry"] = PAPUA_GEOM[kode]
        new_features.append(feat)
    for kode, nama in {92: "Papua Barat Daya", 95: "Papua Selatan",
                       96: "Papua Pegunungan", 97: "Papua Tengah"}.items():
        if kode in PAPUA_GEOM:
            new_features.append({
                "type": "Feature",
                "properties": {prop_key: kode, "kode": kode, "Provinsi": nama},
                "geometry": PAPUA_GEOM[kode],
            })
    geojson["features"] = new_features
    return geojson, feature_id_key


geojson, feature_id_key = load_and_patch_geojson(tuple(GEOJSON_URLS), PAPUA_GEOM_AVAILABLE)

if not PAPUA_GEOM_AVAILABLE:
    st.warning(
        "⚠️ File `papua_geom.py` tidak ditemukan"
    )

df_map = df_result.dropna(subset=["lat", "lon"]).copy()

# PETA KLASTERISASI
sec("1. PETA KLASTERISASI")

hover_cols_cfg = {col: True for col in selected_hover}
for c in ["kode_bps", "lat", "lon", "Provinsi_norm", "cluster_num"]:
    hover_cols_cfg[c] = False

df_choropleth = df_map.dropna(subset=["kode_bps"]).copy()
df_choropleth["kode_bps"] = df_choropleth["kode_bps"].astype(int)

if geojson and feature_id_key:
    fig = px.choropleth_mapbox(
        df_choropleth,
        geojson=geojson,
        locations="kode_bps",
        featureidkey=feature_id_key,
        color="label_klaster",
        color_discrete_map=COLOR_MAP,
        category_orders={"label_klaster": unique_labels},
        hover_name="Provinsi",
        hover_data=hover_cols_cfg,
        mapbox_style=map_style,
        zoom=3.8,
        center={"lat": -2.5, "lon": 118},
        opacity=0.80,
        labels={"label_klaster": "Label Klaster"},
    )

    fig.update_traces(
        marker_line_color="#2C2C2A",
        marker_line_width=0.9,
    )
else:
    fig = go.Figure()
    for n in all_cluster_nums:
        lbl = LEGEND_LABEL.get(n, f"Klaster {n}")
        sub = df_map[df_map["cluster_num"] == n]
        customdata = sub[selected_hover].values if selected_hover else np.empty((len(sub), 0))
        hover_lines = ["<b>%{text}</b>"] + [
            f"{col}: %{{customdata[{i}]}}" for i, col in enumerate(selected_hover)
        ]
        fig.add_trace(go.Scattermapbox(
            lat=sub["lat"], lon=sub["lon"], mode="markers+text",
            marker=dict(size=18, color=COLOR_PALETTE.get(n, "#3498DB"), opacity=0.85),
            text=sub["Provinsi"], textposition="top center",
            customdata=customdata,
            hovertemplate="<br>".join(hover_lines) + "<extra></extra>",
            name=lbl,
        ))
    fig.update_layout(
        mapbox_style=map_style,
        mapbox=dict(zoom=3.8, center={"lat": -2.5, "lon": 118}),
    )

fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=560,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    legend=dict(
        # LEGEND KLASTER
        orientation="v",
        x=0.01,
        y=0.02,
        xanchor="left",
        yanchor="bottom",
        bgcolor="rgba(255,255,255,0.92)",
        bordercolor="#c2dff5",
        borderwidth=1,
        font=dict(size=11, family="Plus Jakarta Sans", color="#1a3a5c"),
    ),
    hoverlabel=dict(
        bgcolor="white", bordercolor="#c2dff5",
        font_size=12, font_family="Plus Jakarta Sans", font_color="#1a3a5c",
    ),
)

st.plotly_chart(fig, use_container_width=True)

# METRIC RINGKASAN KLASTER
klaster_counts = df_result.groupby("cluster_num").size().to_dict()
n_cards = len(all_cluster_nums)

cards_html = f'<div class="metric-grid-{min(n_cards, 4)}">'
for n in all_cluster_nums:
    short_lbl = SHORT_LABEL.get(n, f"Klaster {n}")
    count     = klaster_counts.get(n, 0)
    css_class = CARD_CLASS.get(n, "")
    cards_html += f"""
    <div class="metric-card {css_class}">
        <p class="metric-label">{short_lbl}</p>
        <p class="metric-value">{count} Provinsi</p>
    </div>"""
cards_html += "</div>"
st.markdown(cards_html, unsafe_allow_html=True)

# DETAIL PROVINSI
sec("2. DETAIL INFORMASI PROVINSI")

selected_prov = st.selectbox(
    "PILIH PROVINSI UNTUK MELIHAT DETAIL",
    sorted(df_result["Provinsi"].unique()),
)

# SESUDAH
prov_row  = df_result[df_result["Provinsi"] == selected_prov].iloc[0]
cluster_n = int(prov_row["cluster_num"])
full_lbl  = FULL_LABEL.get(cluster_n, f"Klaster {cluster_n}")
is_noise  = cluster_n == -1
badge_cls = "badge badge-noise" if is_noise else "badge badge-klaster"

st.markdown(f"""
<div class="prov-header">
    <p class="prov-name">{selected_prov}</p>
    <div class="prov-meta">
        <span class="{badge_cls}">{full_lbl}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Metrik indikator
EXCLUDE_COLS = {"lat", "lon", "kode_bps", "cluster_num"}
items = []
for col in numeric_cols:
    if col in EXCLUDE_COLS:
        continue
    val = prov_row[col]
    val_str = f"{val:,.2f}" if isinstance(val, float) and val != int(val) else f"{int(val):,}"
    items.append((col.replace("_", " "), val_str))

chunk_size = 3
for i in range(0, len(items), chunk_size):
    chunk = items[i:i + chunk_size]
    cards = "".join(
        f'<div class="metric-card">'
        f'<p class="metric-label">{label}</p>'
        f'<p class="metric-value" style="font-size:1.3rem;">{value}</p>'
        f'</div>'
        for label, value in chunk
    )
    st.markdown(f'<div class="metric-grid-{len(chunk)}">{cards}</div>', unsafe_allow_html=True)

# SECTION 3: DOWNLOAD
sec("3. DOWNLOAD HASIL KLASTERISASI")

csv = (
    df_result.drop(
        columns=["Provinsi_norm", "lat", "lon", "kode_bps", "label_klaster", "cluster_num"],
        errors="ignore",
    )
    .to_csv(index=False)
    .encode("utf-8")
)
st.download_button(
    label="⬇️ DOWNLOAD CSV",
    data=csv,
    file_name="hasil_klasterisasi.csv",
    mime="text/csv",
)
