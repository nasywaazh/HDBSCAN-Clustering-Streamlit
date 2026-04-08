import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen

st.title("PETA KLASTERISASI PROVINSI INDONESIA")

# ── Guard ────────────────────────────────────────────────────────────────────
if "df_clustered" not in st.session_state:
    st.warning("Data klasterisasi belum tersedia. Jalankan Pemodelan Klasterisasi terlebih dahulu!")
    st.stop()

df_result: pd.DataFrame = st.session_state["df_clustered"].copy()

# ── Koordinat centroid tiap provinsi ─────────────────────────────────────────
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
    "Papua Selatan": (-6.500000, 140.000000),
    "Papua Pegunungan": (-4.000000, 138.500000),
    "Papua Tengah": (-3.500000, 135.500000),
}

# Mapping nama provinsi → kode ISO (untuk choropleth GeoJSON)
ISO_MAP = {
    "Aceh": "ID-AC", "Sumatera Utara": "ID-SU", "Sumatera Barat": "ID-SB",
    "Riau": "ID-RI", "Jambi": "ID-JA", "Sumatera Selatan": "ID-SS",
    "Bengkulu": "ID-BE", "Lampung": "ID-LA",
    "Kepulauan Bangka Belitung": "ID-BB", "Kepulauan Riau": "ID-KR",
    "Daerah Khusus Ibukota Jakarta": "ID-JK", "Jawa Barat": "ID-JB",
    "Jawa Tengah": "ID-JT", "Daerah Istimewa Yogyakarta": "ID-YO",
    "Jawa Timur": "ID-JI", "Banten": "ID-BT", "Bali": "ID-BA",
    "Nusa Tenggara Barat": "ID-NB", "Nusa Tenggara Timur": "ID-NT",
    "Kalimantan Barat": "ID-KB", "Kalimantan Tengah": "ID-KT",
    "Kalimantan Selatan": "ID-KS", "Kalimantan Timur": "ID-KI",
    "Kalimantan Utara": "ID-KU", "Sulawesi Utara": "ID-SA",
    "Sulawesi Tengah": "ID-ST", "Sulawesi Selatan": "ID-SN",
    "Sulawesi Tenggara": "ID-SG", "Gorontalo": "ID-GO",
    "Sulawesi Barat": "ID-SR", "Maluku": "ID-MA", "Maluku Utara": "ID-MU",
    "Papua Barat": "ID-PB", "Papua Barat Daya": "ID-PB",
    "Papua": "ID-PA", "Papua Selatan": "ID-PA",
    "Papua Pegunungan": "ID-PA", "Papua Tengah": "ID-PA",
}

# ── Normalisasi nama provinsi ─────────────────────────────────────────────────
ALIAS = {
    "Dki Jakarta": "Daerah Khusus Ibukota Jakarta",
    "Di Yogyakarta": "Daerah Istimewa Yogyakarta",
    "D.I. Yogyakarta": "Daerah Istimewa Yogyakarta",
    "D.K.I. Jakarta": "Daerah Khusus Ibukota Jakarta",
    "Kep. Bangka Belitung": "Kepulauan Bangka Belitung",
    "Kep. Riau": "Kepulauan Riau",
    "Bangka Belitung": "Kepulauan Bangka Belitung",
    "Yogyakarta": "Daerah Istimewa Yogyakarta",
    "Jakarta": "Daerah Khusus Ibukota Jakarta",
}

def normalize_province(name: str) -> str:
    t = name.strip().title()
    return ALIAS.get(t, t)

df_result["Provinsi_norm"] = df_result["Provinsi"].apply(normalize_province)

# ── Label & warna klaster ─────────────────────────────────────────────────────
df_result["label_klaster"] = df_result["Cluster"].apply(
    lambda x: "Noise" if x == -1 else f"Klaster {x}"
)

def sort_key(lbl):
    return 999 if lbl == "Noise" else int(lbl.split()[-1])

unique_labels = sorted(df_result["label_klaster"].unique(), key=sort_key)

PALETTE = ["#2ECC71", "#3498DB", "#E74C3C", "#F39C12",
           "#9B59B6", "#1ABC9C", "#E67E22", "#E91E63",
           "#00BCD4", "#8BC34A"]
color_map = {}
ci = 0
for lbl in unique_labels:
    if lbl == "Noise":
        color_map[lbl] = "#AAAAAA"
    else:
        color_map[lbl] = PALETTE[ci % len(PALETTE)]
        ci += 1

# ── Kolom numerik ─────────────────────────────────────────────────────────────
numeric_cols = df_result.select_dtypes(include=np.number).columns.drop(
    ["Cluster"], errors="ignore").tolist()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Pengaturan Peta")
    selected_hover = st.multiselect(
        "Tampilkan variabel di tooltip",
        options=numeric_cols,
        default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols,
    )
    map_style = st.selectbox(
        "Gaya peta dasar",
        ["carto-positron", "carto-darkmatter", "open-street-map", "white-bg"],
        index=0,
    )
    show_debug = st.checkbox("🔍 Debug info", value=False)

# ── Tambahkan koordinat ───────────────────────────────────────────────────────
df_result["lat"] = df_result["Provinsi_norm"].map(lambda p: CENTROIDS.get(p, (None, None))[0])
df_result["lon"] = df_result["Provinsi_norm"].map(lambda p: CENTROIDS.get(p, (None, None))[1])
df_result["iso_code"] = df_result["Provinsi_norm"].map(ISO_MAP)

if show_debug:
    st.markdown("**Tabel normalisasi provinsi:**")
    st.dataframe(df_result[["Provinsi", "Provinsi_norm", "iso_code", "label_klaster"]])

missing_coord = df_result[df_result["lat"].isna()]["Provinsi"].tolist()
if missing_coord:
    st.warning(f"Provinsi tanpa koordinat (tidak ditampilkan): **{', '.join(missing_coord)}**")

df_map = df_result.dropna(subset=["lat", "lon"]).copy()

# ── Load GeoJSON ──────────────────────────────────────────────────────────────
GEOJSON_URLS = [
    "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-en.geojson",
    "https://raw.githubusercontent.com/ans-4175/peta-indonesia-geojson/master/indonesia-prov.geojson",
]

@st.cache_data(show_spinner="Memuat GeoJSON…")
def load_geojson(urls):
    for url in urls:
        try:
            with urlopen(url, timeout=10) as resp:
                gj = json.load(resp)
            props = gj["features"][0]["properties"]
            # Cari key yang valuenya mengandung "ID-"
            for k, v in props.items():
                if isinstance(v, str) and v.startswith("ID-"):
                    return gj, f"properties.{k}"
            # Kandidat nama key umum
            for candidate in ["state_code", "kode", "id", "ISO", "CODE", "code", "KODE"]:
                if candidate in props:
                    return gj, f"properties.{candidate}"
        except Exception:
            continue
    return None, None

geojson, feature_id_key = load_geojson(tuple(GEOJSON_URLS))

st.markdown("### 🗺️ Peta Sebaran Klaster Provinsi")

# ── Plot ──────────────────────────────────────────────────────────────────────
if geojson and feature_id_key:
    if show_debug:
        sample_props = geojson["features"][0]["properties"]
        st.caption(f"GeoJSON key digunakan: `{feature_id_key}`")
        st.caption(f"Sample properties GeoJSON: `{sample_props}`")
        # Tampilkan semua value dari key tersebut di GeoJSON
        key_name = feature_id_key.replace("properties.", "")
        all_geo_ids = [f["properties"].get(key_name) for f in geojson["features"]]
        st.caption(f"Semua ID di GeoJSON: `{all_geo_ids[:5]}` ...")
        st.caption(f"Contoh iso_code dataset: `{df_map['iso_code'].dropna().unique()[:5].tolist()}`")

    df_choropleth = df_map.dropna(subset=["iso_code"]).copy()

    hover_cols = {col: True for col in selected_hover}
    for c in ["iso_code", "lat", "lon", "Provinsi_norm"]:
        hover_cols[c] = False

    fig = px.choropleth_mapbox(
        df_choropleth,
        geojson=geojson,
        locations="iso_code",
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
    fig.update_layout(
        margin={"r": 0, "t": 10, "l": 0, "b": 0},
        height=580,
        legend=dict(
            title="Klaster", orientation="v", x=0.01, y=0.98,
            bgcolor="rgba(255,255,255,0.85)", bordercolor="#CCC", borderwidth=1,
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Provinsi pemekaran tanpa ISO → overlay marker
    df_extra = df_map[df_map["iso_code"].isna()]
    if not df_extra.empty:
        st.caption(f"ℹ️ {len(df_extra)} provinsi pemekaran ditampilkan sebagai marker:")
        fig_extra = go.Figure()
        for lbl in df_extra["label_klaster"].unique():
            sub = df_extra[df_extra["label_klaster"] == lbl]
            fig_extra.add_trace(go.Scattermapbox(
                lat=sub["lat"], lon=sub["lon"],
                mode="markers+text",
                marker=dict(size=14, color=color_map.get(lbl, "#999")),
                text=sub["Provinsi"], textposition="top center",
                name=lbl,
            ))
        fig_extra.update_layout(
            mapbox_style=map_style,
            mapbox=dict(zoom=3.5, center={"lat": -2.5, "lon": 118}),
            margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=350,
        )
        st.plotly_chart(fig_extra, use_container_width=True)

else:
    # Fallback: bubble map (tidak butuh GeoJSON)
    st.info("GeoJSON tidak dapat dimuat — menampilkan bubble map.")
    fig = go.Figure()
    for lbl in unique_labels:
        sub = df_map[df_map["label_klaster"] == lbl]
        customdata = sub[selected_hover].values if selected_hover else np.empty((len(sub), 0))
        hover_lines = ["<b>%{text}</b>", f"Klaster: {lbl}"] + \
                      [f"{col}: %{{customdata[{i}]}}" for i, col in enumerate(selected_hover)]
        fig.add_trace(go.Scattermapbox(
            lat=sub["lat"], lon=sub["lon"],
            mode="markers+text",
            marker=dict(size=18, color=color_map.get(lbl, "#999"), opacity=0.85),
            text=sub["Provinsi"],
            textposition="top center",
            customdata=customdata,
            hovertemplate="<br>".join(hover_lines) + "<extra></extra>",
            name=lbl,
        ))
    fig.update_layout(
        mapbox_style=map_style,
        mapbox=dict(zoom=3.8, center={"lat": -2.5, "lon": 118}),
        margin={"r": 0, "t": 10, "l": 0, "b": 0},
        height=580,
        legend=dict(title="Klaster", bgcolor="rgba(255,255,255,0.85)"),
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Ringkasan ─────────────────────────────────────────────────────────────────
st.markdown("### 📊 Ringkasan Anggota per Klaster")
summary = (
    df_result.groupby("label_klaster")["Provinsi"]
    .apply(lambda x: ", ".join(sorted(x)))
    .reset_index()
    .rename(columns={"label_klaster": "Klaster", "Provinsi": "Anggota Provinsi"})
)
summary.insert(1, "Jumlah Provinsi",
               df_result.groupby("label_klaster")["Provinsi"].count().values)
st.dataframe(summary, use_container_width=True, hide_index=True)

# ── Bar chart ─────────────────────────────────────────────────────────────────
st.markdown("### 📈 Distribusi Jumlah Provinsi per Klaster")
count_df = df_result["label_klaster"].value_counts().reset_index()
count_df.columns = ["Klaster", "Jumlah"]
count_df["Warna"] = count_df["Klaster"].map(color_map)
fig_bar = go.Figure(go.Bar(
    x=count_df["Klaster"], y=count_df["Jumlah"],
    marker_color=count_df["Warna"],
    text=count_df["Jumlah"], textposition="outside",
))
fig_bar.update_layout(
    xaxis_title="Klaster", yaxis_title="Jumlah Provinsi",
    plot_bgcolor="white", height=350, margin=dict(t=20, b=40),
)
st.plotly_chart(fig_bar, use_container_width=True)

# ── Download ──────────────────────────────────────────────────────────────────
st.markdown("### 💾 Unduh Hasil Klasterisasi")
csv = df_result.drop(
    columns=["Provinsi_norm", "lat", "lon", "iso_code"], errors="ignore"
).to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download CSV", csv, "hasil_klasterisasi.csv", "text/csv")
