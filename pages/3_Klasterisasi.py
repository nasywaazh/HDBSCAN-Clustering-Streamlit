import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.plt as plt
from sklearn.preprocessing import StandardScaler
from factor_analyzer.factor_analyzer import calculate_kmo, calculate_bartlett_sphericity
from statsmodels.stats.outliers_influence import variance_inflation_factor

st.title("KLASTERISASI HDBSCAN DAN BAYESIAN OPTIMIZATION")
st.divider()

# Data yang diupload pengguna
if "data" not in st.session_state:
    st.warning("Silakan upload dataset terlebih dahulu di halaman Data!")
    st.stop()

df = st.session_state["data"]

# Standarisasi data
st.subheader("1. Preprocessing Data")
data_numeric = df.drop(columns=["Provinsi"])
scaler = StandardScaler()
scaled_standard = pd.DataFrame(
    scaler.fit_transform(data_numeric),
    columns=data_numeric.columns)

with st.expander("Hasil Standarisasi Data"):
    st.dataframe(scaled_standard)

# Uji statistik
st.subheader("Uji Statistik")
kmo_all, kmo_model = calculate_kmo(scaled_standard)
chi_square_value, p_value = calculate_bartlett_sphericity(scaled_standard)
col1, col2 = st.columns(2)

## KMO
with col1:
    st.metric("Nilai KMO:", f"{kmo_model:.4f}")
    if kmo_model > 0.5:
        st.success("Data sudah representatif")
    else:
        st.error("Data tidak representatif")

## Bartlett
with col2:
    st.metric("Bartlett p-value:", f"{p_value:.6f}")
    if p_value < 0.05:
        st.success("Terdapat korelasi yang signifikan antarvariabel")
    else:
        st.error("Tidak ada korelasi yang signifikan antarvariabel")

## Multikolinieritas
X_vif = scaled_standard.copy()
vif_data = pd.DataFrame()
vif_data["Features"] = X_vif.columns
vif_data["VIF"] = [
    variance_inflation_factor(X_vif.values, i)
    for i in range(X_vif.shape[1])
]

with st.expander("Uji Multikolinieritas (VIF)"):
    st.dataframe(vif_data)
    if (vif_data["VIF"] > 10).any():
        st.warning("Terdapat multikolinieritas (VIF > 10)")
    else:
        st.success("Tidak ada multikolinieritas tinggi")
