import streamlit as st
import pandas as pd
import plotly.express as px
import requests

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

# Nama provinsi UPPERCASE agar cocok dengan GeoJSON
df["Provinsi_Map"] = df["Provinsi"].str.upper()

# =========================
# LOAD GEOJSON INDONESIA
# =========================
@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/ans-4175/peta-indonesia-geojson/master/indonesia-prov.geojson"
    response = requests.get(url, timeout=10)
    return response.json()

try:
    geojson = load_geojson()
except Exception as e:
    st.error(f"Gagal memuat GeoJSON: {e}")
    st.stop()

# =========================
# DEBUG: CEK KECOCOKAN NAMA PROVINSI
# =========================
with st.expander("🔍 Debug: Cek Kecocokan Nama Provinsi (hapus setelah peta muncul)"):
    geojson_names = sorted([f["properties"]["Propinsi"] for f in geojson["features"]])
    dataset_names = sorted(df["Provinsi_Map"].tolist())

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Nama di Dataset:**")
        st.write(dataset_names)
    with col2:
        st.markdown("**Nama di GeoJSON:**")
        st.write(geojson_names)

    # Tampilkan nama yang TIDAK cocok
    tidak_cocok = [n for n in dataset_names if n not in geojson_names]
    if tidak_cocok:
        st.error(f"Nama berikut TIDAK ditemukan di GeoJSON: {tidak_cocok}")
    else:
        st.success("Semua nama provinsi cocok!")

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
# PETA CHOROPLETH UTAMA
# =========================
fig = px.choropleth(
    df,
    geojson=geojson,
    locations="Provinsi_Map",
    featureidkey="properties.Propinsi",
    color="Cluster_Label",
    color_discrete_map=color_map,
    hover_name="Provinsi_Map",
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
    height=550
)
st.plotly_chart(fig, use_container_width=True)

# =========================
# DETAIL PROVINSI
# =========================
st.markdown("### Detail Provinsi")
st.caption("Hover pada peta untuk melihat ringkasan, atau pilih provinsi di bawah untuk detail lengkap.")

selected_prov = st.selectbox(
    "Pilih Provinsi:",
    options=sorted(df["Provinsi"].unique())
)

detail = df[df["Provinsi"] == selected_prov]
if not detail.empty:
    row = detail.iloc[0]
    cluster_val = int(row["Cluster"])

    col1, col2 = st.columns([1, 3])
    with col1:
        if cluster_val == -1:
            st.error("Noise (-1)")
            st.caption("Tidak masuk klaster utama")
        else:
            st.success(f"Klaster {cluster_val}")
    with col2:
        st.markdown(f"#### {selected_prov}")
        st.markdown("**Indikator Dampak Banjir:**")
        detail_table = detail[numeric_cols].T.rename(
            columns={detail.index[0]: "Nilai"}
        )
        st.dataframe(detail_table, use_container_width=True)
