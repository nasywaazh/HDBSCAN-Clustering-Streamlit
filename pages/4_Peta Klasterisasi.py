import streamlit as st
import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

st.title("PETA KLASTERISASI WILAYAH TERDAMPAK BANJIR DI INDONESIA")
if "cluster_labels" not in st.session_state or "data" not in st.session_state:
    st.warning("Silakan lakukan klasterisasi terlebih dahulu di halaman sebelumnya!")
    st.stop()

df = st.session_state["data"].copy()
df["Cluster"] = st.session_state["cluster_labels"]

# Load Peta Indonesia
url = "https://raw.githubusercontent.com/ans-4175/peta-indonesia-geojson/master/indonesia-prov.geojson"
map_indo = gpd.read_file(url)

# Normalisasi nama provinsi
map_indo = map_indo.rename(columns={"Propinsi": "Provinsi"})
df["Provinsi"] = df["Provinsi"].str.upper()
map_indo["Provinsi"] = map_indo["Provinsi"].str.upper()

# Merge data
map_cluster = map_indo.merge(df, on="Provinsi", how="left")

# Visualisasi peta
fig, ax = plt.subplots(figsize=(10, 12))
map_cluster.plot(
    column="Cluster",
    cmap="Set2",
    linewidth=0.8,
    ax=ax,
    edgecolor="black",
    legend=True,
    missing_kwds={
        "color": "lightgrey",
        "label": "Data Tidak Tersedia"
    }
)

ax.set_title("Peta Klasterisasi Wilayah Terdampak Banjir di Indonesia", fontsize=14)
ax.axis("off")
st.pyplot(fig)

# Legenda
st.markdown("#### 2. Keterangan Klaster")
unique_clusters = sorted(df["Cluster"].unique())

for c in unique_clusters:
    if c == -1:
        st.markdown(f"- **Cluster -1 (Noise)** : Provinsi tidak termasuk klaster manapun")
    else:
        st.markdown(f"- **Cluster {c}**")

st.markdown("#### 3. Data Klaster per Provinsi")
st.dataframe(df)
