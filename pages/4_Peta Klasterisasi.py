import streamlit as st
import pandas as pd
import json
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

# =========================
# LOAD GEOJSON INDONESIA
# =========================
url_geojson = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-prov.geojson"
response = requests.get(url_geojson)
geojson = response.json()

# =========================
# NORMALISASI NAMA PROVINSI
# =========================
df["Provinsi"] = df["Provinsi"].str.upper()

# =========================
# PILIH VARIABEL NUMERIK
# =========================
numeric_cols = df.select_dtypes(include="number").columns.drop("Cluster")

# =========================
# PETA CHOROPLETH
# =========================
fig = px.choropleth(
    df,
    geojson=geojson,
    locations="Provinsi",
    featureidkey="properties.Propinsi",
    color="Cluster",
    color_continuous_scale="Set2",
    hover_data=numeric_cols,
    title="Peta Klasterisasi Dampak Banjir di Indonesia"
)

fig.update_geos(fitbounds="locations", visible=False)

st.plotly_chart(fig, use_container_width=True)

# =========================
# INTERAKSI KLIK PROVINSI
# =========================
st.markdown("### Detail Provinsi (Klik pada peta)")

clicked = st.plotly_chart(fig, use_container_width=True)

# Streamlit belum native support klik → workaround pakai selectbox
selected_prov = st.selectbox(
    "Pilih Provinsi untuk melihat detail:",
    df["Provinsi"].unique()
)

# =========================
# DETAIL DATA
# =========================
detail = df[df["Provinsi"] == selected_prov]

if not detail.empty:
    st.markdown(f"#### {selected_prov}")

    cluster = int(detail["Cluster"].values[0])
    st.markdown(f"**Cluster:** {cluster}")

    if cluster == -1:
        st.info("Provinsi ini termasuk kategori **Noise (tidak masuk klaster utama)**")

    st.markdown("**Indikator Dampak Banjir:**")
    st.dataframe(detail[numeric_cols].T.rename(columns={detail.index[0]: "Nilai"}))

# =========================
# OPSIONAL: FILTER KLASTER
# =========================
st.markdown("### Filter Klaster")

cluster_filter = st.multiselect(
    "Pilih klaster yang ingin ditampilkan:",
    options=sorted(df["Cluster"].unique()),
    default=sorted(df["Cluster"].unique())
)

filtered_df = df[df["Cluster"].isin(cluster_filter)]

fig_filtered = px.choropleth(
    filtered_df,
    geojson=geojson,
    locations="Provinsi",
    featureidkey="properties.Propinsi",
    color="Cluster",
    hover_data=numeric_cols,
    title="Peta Klasterisasi (Filtered)"
)

fig_filtered.update_geos(fitbounds="locations", visible=False)

st.plotly_chart(fig_filtered, use_container_width=True)
