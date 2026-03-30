import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from factor_analyzer.factor_analyzer import calculate_kmo, calculate_bartlett_sphericity
from statsmodels.stats.outliers_influence import variance_inflation_factor

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
st.subheader("Preprocessing Data")
with menu[0]:
    tab1, tab2, tab3, tab4 = st.tabs([
        "Standarisasi Data",
        "Uji Statistik",
        "Deteksi Outlier (LOF)",
        "Reduksi Data (PCA)"
    ])

# Standarisasi data
with tab1:
    st.subheader("Standarisasi Data")
    data_numeric = df.drop(columns=["Provinsi"])
    scaler = StandardScaler()
    scaled_standard = pd.DataFrame(
        scaler.fit_transform(data_numeric),
        columns=data_numeric.columns
    )
    st.dataframe(scaled_standard)

# Uji statistik
with tab2:
    st.subheader("Uji Statistik")
    # KMO & Bartlett
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

    # VIF
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
