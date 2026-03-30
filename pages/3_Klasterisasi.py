import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from factor_analyzer.factor_analyzer import calculate_kmo, calculate_bartlett_sphericity
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.neighbors import LocalOutlierFactor
from sklearn.decomposition import PCA

st.title("KLASTERISASI HDBSCAN & BAYESIAN OPTIMIZATION")
st.divider()

# Data yang diupload pengguna
if "data" not in st.session_state:
    st.warning("Silakan upload dataset terlebih dahulu di halaman Data!")
    st.stop()

df = st.session_state["data"]

menu = st.tabs([
    "Preprocessing Data",
    "Pemodelan Klasterisasi",
    "Hasil Klasterisasi"
])

# Preprocessing data
with menu[0]:
    # Standarisasi data
    st.markdown("1. Standarisasi Data")
    data_numeric = df.drop(columns=["Provinsi"])
    scaler = StandardScaler()
    scaled_standard = pd.DataFrame(
        scaler.fit_transform(data_numeric),
        columns=data_numeric.columns)
    st.dataframe(scaled_standard)

    # Uji statistik
    st.markdown("2. Uji Statistik")
    kmo_all, kmo_model = calculate_kmo(scaled_standard)
    chi_square_value, p_value = calculate_bartlett_sphericity(scaled_standard)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Uji Kaiser-Meyer-Olkin (KMO)", f"{kmo_model:.4f}")

    if kmo_model > 0.5:
        st.success("Data sudah representatif")
    else:
        st.error("Data belum representatif")
        
    with col2:
        st.metric("Uji Bartlett (p-value)", f"{p_value:.6f}")

    if p_value < 0.05:
        st.success("Terdapat korelasi signifikan antar variabel")
        korelasi_ok = True
    else:
        st.warning("Tidak ada korelasi signifikan")
        korelasi_ok = False

    X_vif = scaled_standard.copy()
    vif_data = pd.DataFrame()
    vif_data["Variabel"] = X_vif.columns
    vif_data["VIF"] = [
        variance_inflation_factor(X_vif.values, i)
        for i in range(X_vif.shape[1])
    ]

    st.write("Uji Multikolinieritas dengan Variance Inflation Factor (VIF):")
    st.dataframe(vif_data)
    high_vif = vif_data[vif_data["VIF"] >= 5]
    if not high_vif.empty:
        variabels = ", ".join(high_vif["Variabel"].tolist())
        st.warning(
            f"Variabel {variabels} memiliki nilai VIF ≥ 5 "
            "yang mengindikasikan adanya multikolinieritas yang tinggi."
        )
        multikolinieritas = True
    else:
        st.success("Tidak terdapat multikolinieritas tinggi (VIF < 5)")
        multikolinieritas = False

    # Deteksi outlier
    st.markdown("3. Deteksi Outlier (Local Outlier Factor)")
    lof = LocalOutlierFactor(n_neighbors=20)
    y_pred = lof.fit_predict(scaled_standard)
    lof_scores = -lof.negative_outlier_factor_
    df_lof = df.copy()
    df_lof["LOF Score"] = lof_scores
    threshold = lof_scores.std()
    df_lof["Label"] = np.where(
        df_lof["LOF Score"] > threshold,
        "Outlier",
        "Normal"
    )
    st.dataframe(df_lof[["Provinsi", "LOF Score", "Label"]])

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(data=df_lof, x="Provinsi", y="LOF Score", hue="Label", ax=ax)
    plt.xticks(rotation=90)
    plt.axhline(threshold, linestyle="--")
    plt.title("Visualisasi LOF")
    st.pyplot(fig)

    # Reduksi data
    st.markdown("4. Reduksi Data (Principal Component Analysis)")
    if multikolinieritas and korelasi_ok:
        pca = PCA()
        pca.fit(scaled_standard)
        eigenvalues = pca.explained_variance_
        proporsi = pca.explained_variance_ratio_ * 100
        kumulatif = np.cumsum(proporsi)
        pca_df = pd.DataFrame({
            "Komponen": [f"PC{i+1}" for i in range(len(eigenvalues))],
            "Eigenvalue": eigenvalues,
            "Proporsi Varians (%)": proporsi,
            "Kumulatif (%)": kumulatif
        })
        st.dataframe(pca_df)

        valid_pc = pca_df[pca_df["Eigenvalue"] > 1]
        n_components = len(valid_pc)
        if kumulatif[n_components - 1] < 80:
            n_components = np.argmax(kumulatif >= 80) + 1

        st.success(f"Jumlah komponen yang digunakan berdasarkan kriteria eigenvalue > 1 dan proporsi variansi kumulatif ≥ 80% : {n_components}")
        pca_final = PCA(n_components=n_components)
        pca_result = pd.DataFrame(
            pca_final.fit_transform(scaled_standard),
            columns=[f"PC{i+1}" for i in range(n_components)]
        )
        st.dataframe(pca_result)
        
        st.session_state["X_clustering"] = pca_result
    else:
        st.info("PCA tidak diperlukan")
        st.session_state["X_clustering"] = scaled_standard
