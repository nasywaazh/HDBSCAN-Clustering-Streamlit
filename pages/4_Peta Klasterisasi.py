import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.title("Peta Klasterisasi Dampak Banjir di Indonesia")

# =========================
# VALIDASI DATA
# =========================
if "df_clustered" not in st.session_state:
    st.warning("Silakan lakukan klasterisasi terlebih dahulu di halaman Klasterisasi!")
    st.stop()

df = st.session_state["df_clustered"]

# =========================
# LOAD PETA INDONESIA
# =========================
@st.cache_data
def load_map():
    url = "https://raw.githubusercontent.com/ans-4175/peta-indonesia-geojson/master/indonesia-prov.geojson"
    gdf = gpd.read_file(url)
    gdf = gdf.rename(columns={"Propinsi": "Provinsi"})
    return gdf

gdf = load_map()

# =========================
# CLEAN DATA (WAJIB!)
# =========================
df["Provinsi"] = df["Provinsi"].str.strip().str.upper()
gdf["Provinsi"] = gdf["Provinsi"].str.strip().str.upper()

# =========================
# MERGE DATA
# =========================
gdf = gdf.merge(df, on="Provinsi", how="left")

# =========================
# HANDLE NILAI KOSONG
# =========================
gdf["Cluster"] = gdf["Cluster"].fillna(-1)

# =========================
# FILTER KLASTER (OPSIONAL)
# =========================
cluster_options = ["Semua"] + sorted(gdf["Cluster"].unique().tolist())
selected_cluster = st.selectbox("Pilih Klaster", cluster_options)

if selected_cluster != "Semua":
    gdf_plot = gdf[gdf["Cluster"] == selected_cluster]
else:
    gdf_plot = gdf

# =========================
# WARNA KLASTER
# =========================
cluster_colors = {
    0: "#66c2a5",
    1: "#fc8d62",
    2: "#8da0cb",
    3: "#e78ac3",  # jika cluster lebih dari 3
    -1: "#d3d3d3"
}

gdf_plot["color"] = gdf_plot["Cluster"].map(cluster_colors)

# =========================
# PLOT PETA
# =========================
fig, ax = plt.subplots(figsize=(12, 8))

gdf_plot.plot(
    ax=ax,
    color=gdf_plot["color"],
    edgecolor="black",
    linewidth=0.5
)

ax.set_title("Peta Klasterisasi Dampak Banjir di Indonesia", fontsize=14)
ax.axis("off")

# =========================
# LEGEND DINAMIS
# =========================
unique_clusters = sorted(gdf["Cluster"].unique())

legend_patches = []
for c in unique_clusters:
    label = f"Klaster {c}" if c != -1 else "Noise (-1)"
    color = cluster_colors.get(c, "#cccccc")
    legend_patches.append(mpatches.Patch(color=color, label=label))

ax.legend(
    handles=legend_patches,
    title="Klaster",
    loc="lower left"
)

# =========================
# TAMPILKAN
# =========================
st.pyplot(fig)

# =========================
# DEBUG (OPSIONAL - HAPUS SAAT FINAL)
# =========================
with st.expander("Debug Data"):
    st.write("Preview Data Clustering:")
    st.dataframe(df.head())

    st.write("Preview Geo Data:")
    st.dataframe(gdf[["Provinsi", "Cluster"]].head())
