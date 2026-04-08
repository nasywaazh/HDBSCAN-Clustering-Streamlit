import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen

st.title("PETA KLASTERISASI PROVINSI INDONESIA")

# ── Guard: butuh hasil klasterisasi ──────────────────────────────────────────
if "df_clustered" not in st.session_state:
    st.warning(
        "Data klasterisasi belum tersedia. "
        "Silakan jalankan proses **Pemodelan Klasterisasi** terlebih dahulu!"
    )
    st.stop()

df_result: pd.DataFrame = st.session_state["df_clustered"].copy()

# ── Mapping nama provinsi → kode BPS (ISO 3166-2:ID) ─────────────────────────
# GeoJSON Indonesia menggunakan kode provinsi BPS / ISO.
# Sesuaikan mapping ini dengan nama kolom "Provinsi" di dataset Anda.
PROV_CODE_MAP: dict[str, str] = {
    "Aceh": "ID-AC",
    "Sumatera Utara": "ID-SU",
    "Sumatera Barat": "ID-SB",
    "Riau": "ID-RI",
    "Jambi": "ID-JA",
    "Sumatera Selatan": "ID-SS",
    "Bengkulu": "ID-BE",
    "Lampung": "ID-LA",
    "Kepulauan Bangka Belitung": "ID-BB",
    "Kepulauan Riau": "ID-KR",
    "DKI Jakarta": "ID-JK",
    "Jawa Barat": "ID-JB",
    "Jawa Tengah": "ID-JT",
    "DI Yogyakarta": "ID-YO",
    "Jawa Timur": "ID-JI",
    "Banten": "ID-BT",
    "Bali": "ID-BA",
    "Nusa Tenggara Barat": "ID-NB",
    "Nusa Tenggara Timur": "ID-NT",
    "Kalimantan Barat": "ID-KB",
    "Kalimantan Tengah": "ID-KT",
    "Kalimantan Selatan": "ID-KS",
    "Kalimantan Timur": "ID-KI",
    "Kalimantan Utara": "ID-KU",
    "Sulawesi Utara": "ID-SA",
    "Sulawesi Tengah": "ID-ST",
    "Sulawesi Selatan": "ID-SN",
    "Sulawesi Tenggara": "ID-SG",
    "Gorontalo": "ID-GO",
    "Sulawesi Barat": "ID-SR",
    "Maluku": "ID-MA",
    "Maluku Utara": "ID-MU",
    "Papua Barat": "ID-PB",
    "Papua": "ID-PA",
    # Nama alternatif / singkatan yang sering muncul di dataset
    "Kepulauan Bangka-Belitung": "ID-BB",
    "Bangka Belitung": "ID-BB",
    "Kep. Bangka Belitung": "ID-BB",
    "Kep. Riau": "ID-KR",
    "Yogyakarta": "ID-YO",
    "D.I. Yogyakarta": "ID-YO",
    "D.K.I. Jakarta": "ID-JK",
    "Jakarta": "ID-JK",
}

# ── Load GeoJSON provinsi Indonesia ─────────────────────────────────────────
GEOJSON_URL = (
    "https://raw.githubusercontent.com/superpikar/indonesia-geojson/"
    "master/indonesia-en.geojson"
)

@st.cache_data(show_spinner="Memuat data GeoJSON peta Indonesia…")
def load_geojson(url: str) -> dict:
    with urlopen(url) as resp:
        return json.load(resp)

try:
    geojson = load_geojson(GEOJSON_URL)
except Exception as e:
    st.error(
        f"Gagal memuat GeoJSON: {e}\n\n"
        "Pastikan koneksi internet tersedia, atau ganti `GEOJSON_URL` "
        "dengan path file GeoJSON lokal."
    )
    st.stop()

# ── Siapkan data untuk peta ───────────────────────────────────────────────────
df_map = df_result.copy()

# Tambah kolom kode provinsi
df_map["kode_provinsi"] = df_map["Provinsi"].map(PROV_CODE_MAP)

# Provinsi yang tidak ter-mapping
unmapped = df_map[df_map["kode_provinsi"].isna()]["Provinsi"].tolist()
if unmapped:
    st.warning(
        f"⚠️ Provinsi berikut tidak ditemukan dalam mapping kode: **{', '.join(unmapped)}**. "
        "Silakan perbarui `PROV_CODE_MAP` di `peta_klasterisasi.py`."
    )

# Label klaster (termasuk noise)
df_map["label_klaster"] = df_map["Cluster"].apply(
    lambda x: "Noise (-1)" if x == -1 else f"Klaster {x}"
)

# Warna per klaster
unique_labels = sorted(df_map["label_klaster"].unique())
PALETTE = [
    "#2ECC71", "#3498DB", "#E74C3C", "#F39C12",
    "#9B59B6", "#1ABC9C", "#E67E22", "#E91E63",
    "#00BCD4", "#8BC34A",
]
color_discrete_map = {}
cluster_idx = 0
for lbl in unique_labels:
    if lbl == "Noise (-1)":
        color_discrete_map[lbl] = "#AAAAAA"
    else:
        color_discrete_map[lbl] = PALETTE[cluster_idx % len(PALETTE)]
        cluster_idx += 1

# Kolom numerik untuk hover
numeric_cols = df_map.select_dtypes(include=np.number).columns.drop(
    ["Cluster"], errors="ignore"
).tolist()

# ── Sidebar: pilih variabel hover ─────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Pengaturan Peta")
    selected_hover = st.multiselect(
        "Tampilkan variabel di tooltip",
        options=numeric_cols,
        default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols,
    )
    show_border = st.checkbox("Tampilkan batas provinsi", value=True)
    map_style = st.selectbox(
        "Gaya peta dasar",
        ["carto-positron", "carto-darkmatter", "open-street-map", "white-bg"],
        index=0,
    )

# ── Plot Choropleth ───────────────────────────────────────────────────────────
st.markdown("### 🗺️ Peta Sebaran Klaster Provinsi")

hover_data_dict = {col: True for col in selected_hover}
hover_data_dict["kode_provinsi"] = False  # sembunyikan kode teknis

fig = px.choropleth_mapbox(
    df_map,
    geojson=geojson,
    locations="kode_provinsi",
    featureidkey="properties.state_code",   # sesuaikan dengan key GeoJSON
    color="label_klaster",
    color_discrete_map=color_discrete_map,
    category_orders={"label_klaster": unique_labels},
    hover_name="Provinsi",
    hover_data=hover_data_dict,
    mapbox_style=map_style,
    zoom=3.8,
    center={"lat": -2.5, "lon": 118},
    opacity=0.75,
    labels={"label_klaster": "Klaster"},
    title="Klasterisasi HDBSCAN + Bayesian Optimization",
)

fig.update_layout(
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    height=580,
    legend=dict(
        title="Klaster",
        orientation="v",
        x=0.01,
        y=0.98,
        bgcolor="rgba(255,255,255,0.85)",
        bordercolor="#CCCCCC",
        borderwidth=1,
    ),
)

if not show_border:
    fig.update_traces(marker_line_width=0)

st.plotly_chart(fig, use_container_width=True)

# ── Ringkasan jumlah anggota per klaster ─────────────────────────────────────
st.markdown("### 📊 Ringkasan Anggota per Klaster")

summary = (
    df_map.groupby("label_klaster")["Provinsi"]
    .apply(lambda x: ", ".join(sorted(x)))
    .reset_index()
    .rename(columns={"label_klaster": "Klaster", "Provinsi": "Anggota Provinsi"})
)
summary.insert(
    1,
    "Jumlah Provinsi",
    df_map.groupby("label_klaster")["Provinsi"].count().values,
)
st.dataframe(summary, use_container_width=True, hide_index=True)

# ── Bar chart distribusi klaster ─────────────────────────────────────────────
st.markdown("### 📈 Distribusi Jumlah Provinsi per Klaster")

count_df = df_map["label_klaster"].value_counts().reset_index()
count_df.columns = ["Klaster", "Jumlah Provinsi"]
count_df["Warna"] = count_df["Klaster"].map(color_discrete_map)

fig_bar = go.Figure(
    go.Bar(
        x=count_df["Klaster"],
        y=count_df["Jumlah Provinsi"],
        marker_color=count_df["Warna"],
        text=count_df["Jumlah Provinsi"],
        textposition="outside",
    )
)
fig_bar.update_layout(
    xaxis_title="Klaster",
    yaxis_title="Jumlah Provinsi",
    plot_bgcolor="white",
    height=350,
    margin=dict(t=20, b=40),
)
st.plotly_chart(fig_bar, use_container_width=True)

# ── Download hasil ───────────────────────────────────────────────────────────
st.markdown("### 💾 Unduh Hasil Klasterisasi")
csv_data = df_result.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download CSV Hasil Klasterisasi",
    data=csv_data,
    file_name="hasil_klasterisasi.csv",
    mime="text/csv",
)
