import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen

st.title("PETA KLASTERISASI WILAYAH TERDAMPAK BANJIR DI INDONESIA")
st.divider()
if "df_clustered" not in st.session_state:
    st.warning("Silakan upload dataset dan lakukan proses klasterisasi terlebih dahulu!")
    st.stop()

df_result: pd.DataFrame = st.session_state["df_clustered"].copy()

# Koordinat centroid tiap provinsi
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

# Mapping Nama Provinsi → Kode BPS Numerik
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

# Normalisasi Nama Provinsi
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
        "Pilih Jenis Gaya Peta!",
        ["carto-positron", "carto-darkmatter", "open-street-map", "white-bg"],
        index=0,
    )

    selected_hover = st.multiselect(
        "Pilih data untuk ditampilkan di hover!",
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

# Load GeoJSON
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

st.markdown("#### Peta Klasterisasi Berdasarkan Indikator Dampak Banjir")

# Plot
if geojson and feature_id_key:
    df_choropleth = df_map.dropna(subset=["kode_bps"]).copy()
    df_choropleth["kode_bps"] = df_choropleth["kode_bps"].astype(int)
    df_marker = df_map[df_map["kode_bps"].isna()].copy()

    hover_cols = {col: True for col in selected_hover}
    for c in ["kode_bps", "lat", "lon", "Provinsi_norm"]:
        hover_cols[c] = False

    # Base choropleth
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

    # Overlay marker provinsi pemekaran ke figure yang SAMA
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
                    # Jangan duplikat entri legend jika klaster sudah ada
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

else:
    # Fallback bubble map
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

# Detail Informasi Setiap Provinsi
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

# Download Hasil Klasterisasi
st.write()
st.markdown("#### Unduh Hasil Klasterisasi")
csv = (
    df_result.drop(
        columns=["Provinsi_norm", "lat", "lon", "kode_bps", "label_klaster"],
        errors="ignore",
    )
    .to_csv(index=False)
    .encode("utf-8")
)
st.download_button(
    "⬇️ Download CSV", csv, "hasil_klasterisasi.csv", "text/csv"
)
