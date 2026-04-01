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
    lambda x: f"Noise (-1)" if x == -1 else f"Klaster {x}"
)

# =========================
# LOAD GEOJSON INDONESIA
# =========================
@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/ans-4175/peta-indonesia-geojson/master/indonesia-prov.geojson"
    response = requests.get(url)
    return response.json()

geojson = load_geojson()

# =========================
# NORMALISASI NAMA PROVINSI
# =========================
# Ambil nama provinsi dari GeoJSON untuk pencocokan
geojson_names = [f["properties"]["Propinsi"] for f in geojson["features"]]

# Normalisasi ke Title Case agar cocok dengan GeoJSON
df["Provinsi_Map"] = df["Provinsi"].str.title()

# =========================
# PILIH VARIABEL NUMERIK
# =========================
numeric_cols = [c for c in df.select_dtypes(include="number").columns if c != "Cluster"]

# =========================
# FILTER KLASTER
# =========================
st.markdown("### Filter Klaster")
all_clusters = sorted(df["Cluster"].unique())
cluster_filter = st.multiselect(
    "Pilih klaster yang ingin ditampilkan:",
    options=all_clusters,
    default=all_clusters,
    format_func=lambda x: "Noise (-1)" if x == -1 else f"Klaster {x}"
)
filtered_df = df[df["Cluster"].isin(cluster_filter)]

# =========================
# WARNA DISKRIT PER KLASTER
# =========================
palette = px.colors.qualitative.Set2
cluster_labels_sorted = sorted(df["Cluster"].unique())
color_map = {}
color_idx = 0
for c in cluster_labels_sorted:
    if c == -1:
        color_map[f"Noise (-1)"] = "#aaaaaa"
    else:
        color_map[f"Klaster {c}"] = palette[color_idx % len(palette)]
        color_idx += 1

# =========================
# PETA CHOROPLETH
# =========================
fig = px.choropleth(
    filtered_df,
    geojson=geojson,
    locations="Provinsi_Map",
    featureidkey="properties.Propinsi",
    color="Cluster_Label",
    color_discrete_map=color_map,
    hover_name="Provinsi_Map",
    hover_data={col: True for col in numeric_cols} | {"Cluster_Label": True, "Provinsi_Map": False},
    title="Peta Klasterisasi Dampak Banjir di Indonesia",
    category_orders={"Cluster_Label": [f"Klaster {c}" for c in cluster_labels_sorted if c != -1] + ["Noise (-1)"]}
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    legend_title_text="Klaster"
)
st.plotly_chart(fig, use_container_width=True)

# =========================
# DETAIL PROVINSI VIA SELECTBOX
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
        detail_table = detail[numeric_cols].T.rename(columns={detail.index[0]: "Nilai"})
        st.dataframe(detail_table, use_container_width=True)
