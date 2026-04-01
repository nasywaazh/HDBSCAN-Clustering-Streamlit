import plotly.express as px

# pastikan cluster jadi string (biar dianggap kategori)
df["Cluster"] = df["Cluster"].astype(str)

# warna manual (biar konsisten dengan skripsi)
color_map = {
    "0": "#66c2a5",
    "1": "#fc8d62",
    "2": "#8da0cb",
    "-1": "#d3d3d3"
}

fig = px.choropleth(
    df,
    geojson=geojson,
    locations="Provinsi",
    featureidkey="properties.Propinsi",
    color="Cluster",
    color_discrete_map=color_map   # ✅ FIX DI SINI
)

fig.update_geos(fitbounds="locations", visible=False)

st.plotly_chart(fig)
