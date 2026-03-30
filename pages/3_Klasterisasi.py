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
import hdbscan
from hdbscan.validity import validity_index
from bayes_opt import BayesianOptimization
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import cdist
from scipy.sparse.csgraph import minimum_spanning_tree
from itertools import combinations
from scipy.spatial import ConvexHull
from matplotlib.patches import Polygon

st.title("KLASTERISASI HDBSCAN DAN BAYESIAN OPTIMIZATION")
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
    st.markdown("#### 1. Standarisasi Data")
    data_numeric = df.drop(columns=["Provinsi"])
    scaler = StandardScaler()
    scaled_standard = pd.DataFrame(
        scaler.fit_transform(data_numeric),
        columns=data_numeric.columns)
    st.dataframe(scaled_standard)

    # Uji statistik
    st.markdown("#### 2. Uji Statistik")
    kmo_all, kmo_model = calculate_kmo(scaled_standard)
    chi_square_value, p_value = calculate_bartlett_sphericity(scaled_standard)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Uji Kaiser-Meyer-Olkin (KMO)", f"{kmo_model:.4f}")
        st.caption("Kriteria Nilai KMO > 0.5")
        if kmo_model > 0.5:
            st.success("Data sudah representatif")
        else:
            st.error("Data belum representatif")
        
    with col2:
        st.metric("Uji Bartlett", f"{p_value:.6f}")
        st.caption("Kriteria p-value < 0.05")
        if p_value < 0.05:
            st.success("Terdapat korelasi signifikan antarvariabel")
            korelasi_ok = True
        else:
            st.warning("Tidak terdapat korelasi signifikan antarvariabel")
            korelasi_ok = False

    X_vif = scaled_standard.copy()
    vif_data = pd.DataFrame()
    vif_data["Variabel"] = X_vif.columns
    vif_data["VIF"] = [
        variance_inflation_factor(X_vif.values, i)
        for i in range(X_vif.shape[1])
    ]

    st.write("Uji Multikolinieritas dengan Variance Inflation Factor (VIF)")
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
    st.markdown("#### 3. Deteksi Outlier (Local Outlier Factor)")
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
    sns.barplot(data=df_lof, x="Provinsi", y="LOF Score", hue="Label",
                palette={"Normal": "Skyblue", "Outlier": "Salmon"} , ax=ax)
    plt.xticks(rotation=90)
    plt.axhline(threshold, linestyle="--")
    plt.title("Visualisasi LOF")
    st.pyplot(fig)

    # Reduksi data
    st.markdown("#### 4. Reduksi Data (Principal Component Analysis)")
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
            "Proporsi Varians Kumulatif (%)": kumulatif
        })
        st.dataframe(pca_df)

        valid_pc = pca_df[pca_df["Eigenvalue"] > 1]
        n_components = len(valid_pc)
        if kumulatif[n_components - 1] < 80:
            n_components = np.argmax(kumulatif >= 80) + 1

        st.success(f"Jumlah komponen yang digunakan berdasarkan kriteria eigenvalue > 1 dan proporsi variansi kumulatif ≥ 80% adalah {n_components} komponen")
        pca_final = PCA(n_components=n_components)
        pca_result = pd.DataFrame(
            pca_final.fit_transform(scaled_standard),
            columns=[f"PC{i+1}" for i in range(n_components)]
        )
        st.dataframe(pca_result)
        
        st.session_state["X_clustering"] = pca_result
        st.session_state["X_plot"] = pca_result
    else:
        st.info("PCA tidak diperlukan")
        st.session_state["X_clustering"] = scaled_standard
        st.session_state["X_plot"] = scaled_standard

# Pemodelan klasterisasi
if "X_clustering" not in st.session_state:
    st.warning("Silakan lakukan preprocessing data terlebih dahulu!")
    st.stop()
X_clustering = st.session_state["X_clustering"].values

# Rumus perhitungan DCSI
def get_eps_i(X_cluster, min_samples, quantile=0.5):
    n = len(X_cluster)
    if n < 2:
        return None
    k = min(min_samples, n - 1)
    nbrs = NearestNeighbors(n_neighbors=k).fit(X_cluster)
    distances, _ = nbrs.kneighbors(X_cluster)
    return np.quantile(distances[:, -1], quantile)

def get_core_points(X_cluster, min_samples, eps_i):
    n = len(X_cluster)
    if n < 2 or eps_i is None:
        return np.array([], dtype=int)
    nbrs = NearestNeighbors(radius=eps_i).fit(X_cluster)
    neighbors = nbrs.radius_neighbors(X_cluster, return_distance=False)
    core_mask = np.array([len(nb) >= min_samples for nb in neighbors])
    return np.where(core_mask)[0]

def compute_connectedness(X_cluster, min_samples, eps_i):
    core_idx = get_core_points(X_cluster, min_samples, eps_i)
    if len(core_idx) < 2:
        return np.inf
    X_core = X_cluster[core_idx]
    dist_matrix = cdist(X_core, X_core)
    mst = minimum_spanning_tree(dist_matrix).toarray()
    return np.max(mst)

def compute_separation(X_ci, X_cj, min_samples, eps_i, eps_j):
    core_i = get_core_points(X_ci, min_samples, eps_i)
    core_j = get_core_points(X_cj, min_samples, eps_j)
    if len(core_i) == 0 or len(core_j) == 0:
        return np.inf
    X_core_i = X_ci[core_i]
    X_core_j = X_cj[core_j]
    dist = cdist(X_core_i, X_core_j)
    return np.min(dist)

def dcsi_index(X, labels, min_samples):
    mask = labels != -1
    X_valid = X[mask]
    labels_valid = labels[mask]
    clusters = np.unique(labels_valid)
    if len(clusters) < 2:
        return None
    eps_dict = {}
    conn_dict = {}
    for c in clusters:
        X_c = X_valid[labels_valid == c]
        eps = get_eps_i(X_c, min_samples)
        eps_dict[c] = eps
        conn_dict[c] = compute_connectedness(X_c, min_samples, eps)

    total = 0
    weight_sum = 0
    for ci, cj in combinations(clusters, 2):
        X_ci = X_valid[labels_valid == ci]
        X_cj = X_valid[labels_valid == cj]
        sep = compute_separation(
            X_ci, X_cj, min_samples,
            eps_dict[ci], eps_dict[cj])
        max_conn = max(conn_dict[ci], conn_dict[cj])
        if np.isinf(sep) or np.isinf(max_conn) or (sep + max_conn) == 0:
            continue
        score = sep / (sep + max_conn)
        weight = len(X_ci) + len(X_cj)
        total += score * weight
        weight_sum += weight
    if weight_sum == 0:
        return None
    return total / weight_sum

with menu[1]:
    # Pencarian parameter optimal
    st.markdown("#### 1. Pencarian Parameter Optimal (Bayesian Optimization)")
    with st.spinner("Mencari parameter optimal..."):
        X_clustering = np.array(X_clustering)
        X_plot = st.session_state.get("X_plot", st.session_state["X_clustering"])
        def objective(min_cluster_size, min_samples):
            min_cluster_size = int(np.floor(min_cluster_size))
            min_samples = int(np.floor(min_samples))
            if min_cluster_size < 2 or min_samples < 1:
                return -1.0
            if min_samples > min_cluster_size:
                return -1.0

            clusterer = hdbscan.HDBSCAN(
                min_cluster_size=min_cluster_size,
                min_samples=min_samples,
                metric="euclidean"
            )
            labels = clusterer.fit_predict(X_clustering)

            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            if n_clusters < 2:
                return -1.0

            try:
                dbcv = validity_index(X_clustering, labels)
                return dbcv
            except:
                return -1.0

        pbounds = {"min_cluster_size": (2, 7), "min_samples": (1, 6)}

        optimizer = BayesianOptimization(f = objective,
                                         pbounds = pbounds,
                                         random_state = 42,
                                         verbose = 2)
        optimizer.maximize(init_points = 8, n_iter = 30)
        best_params = optimizer.max["params"]
        best_dbcv = optimizer.max["target"]

    st.success("Parameter optimal ditemukan!")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("min_cluster_size", int(np.floor(best_params["min_cluster_size"])))
    with col2:
        st.metric("min_samples", int(np.floor(best_params["min_samples"])))
    with col3:
        st.metric("Best DBCV Score", f"{best_dbcv:.4f}")

    targets = optimizer.space.target
    iterations = np.arange(1, len(targets) + 1)
    best_so_far = np.maximum.accumulate(targets)
    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        ax1.plot(iterations, best_so_far, marker='o')
        ax1.set_title("Best DBCV Over Time")
        ax1.set_xlabel("Iterasi")
        ax1.set_ylabel("Best DBCV Score")
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        ax2.plot(iterations, targets, marker='o')
        ax2.axhline(best_dbcv, color='red', linestyle="--", label=f"Best DBCV = {best_dbcv:.4f}")
        ax2.set_title("Bayesian Optimization Convergence")
        st.pyplot(fig2)

    # Model HDBSCAN
    st.markdown("#### 2. Visualisasi Distribusi Klaster")
    hdbscan_model = hdbscan.HDBSCAN(
        min_cluster_size=int(np.floor(best_params["min_cluster_size"])),
        min_samples=int(np.floor(best_params["min_samples"])),
        prediction_data=True)
    hdbscan_model.fit(X_clustering)
    cluster_labels = hdbscan_model.labels_
    st.session_state["cluster_labels"] = cluster_labels

    df_result = df.copy()
    df_result["Cluster"] = cluster_labels

    X_plot = st.session_state.get("X_plot", pd.DataFrame(X_clustering))
    xcol, ycol = X_plot.columns[0], X_plot.columns[1]

    fig, ax = plt.subplots(figsize=(10, 6))
    unique_labels = sorted(set(cluster_labels))
    n_clusters = len([l for l in unique_labels if l != -1])
    palette = sns.color_palette("Set2", n_clusters)

    color_map = {}
    palette_idx = 0
    for label in unique_labels:
        if label == -1:
            color_map[label] = "gray"
        else:
            color_map[label] = palette[palette_idx]
            palette_idx += 1

    for label in unique_labels:
        idx = cluster_labels == label
        points = X_plot[idx].reset_index(drop=True)
        color = color_map[label]

        ax.scatter(
            points[xcol], points[ycol],
            s=60,
            c='gray' if label == -1 else [color],
            label='Noise' if label == -1 else f'Cluster {label}',
            edgecolor='k',
            alpha=0.6 if label == -1 else 0.9
        )

        if label != -1 and len(points) >= 3:
            try:
                hull = ConvexHull(points[[xcol, ycol]])
                hull_points = points.iloc[hull.vertices][[xcol, ycol]]
                polygon = Polygon(
                    hull_points.values,
                    closed=True,
                    facecolor=color,
                    alpha=0.2,
                    edgecolor=color,
                    linewidth=2
                )
                ax.add_patch(polygon)
            except Exception:
                pass  

    ax.set_title("Distribusi Klaster HDBSCAN + Bayesian Optimization", fontsize=14)
    ax.set_xlabel(xcol)
    ax.set_ylabel(ycol)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(title="Cluster")
    ax.grid(True, linestyle='--', alpha=0.3)
    st.pyplot(fig)

    # Evaluasi model HDBSCAN
    st.markdown("#### 3. Evaluasi Model")
    dbcv_score = validity_index(X_clustering, cluster_labels)
    min_samples = int(best_params["min_samples"])
    dcsi_score = dcsi_index(X_clustering, cluster_labels, min_samples)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("DBCV Score", f"{dbcv_score:.4f}")
        st.caption("Kriteria DBCV Score > 0.5")
    with col2:
        if dcsi_score is not None:
            st.metric("DCSI Score", f"{dcsi_score:.4f}")
            st.caption("Kriteria DCSI Score > 0.5")
        else:
            st.warning("DCSI tidak dapat dihitung")

    if dcsi_score is not None:
        if dbcv_score > 0.5 and dcsi_score > 0.5:
            st.success("Kualitas klaster sudah baik dengan stabilitas dan pemisahan yang jelas antarklaster")
        elif dbcv_score > 0.5 and dcsi_score <= 0.5:
            st.warning("Kualitas klaster  cukup baik berdasarkan DBCV, namun kurang optimal berdasarkan DCSI")
        elif dbcv_score <= 0.5 and dcsi_score > 0.5:
            st.warning("Kualitas klaster cukup baik berdasarkan DCSI, namun kurang optimal berdasarkan DBCV")
        else:
            st.error("Kualitas klaster yang buruk berdasarkan DBCV dan DCSI")
    else:
        if dbcv_score > 0.5:
            st.success("Kualitas klaster sudah baik berdasarkan DBCV")
        else:
            st.error("Kualitas klaster kurang optimal berdasarkan DBCV")

# Hasil klasterisasi
with menu[2]:
    if "cluster_labels" not in st.session_state:
        st.warning("Silakan jalankan proses klasterisasi terlebih dahulu!")
        st.stop()
    cluster_labels = st.session_state.cluster_labels
    df_result = df.copy()
    df_result["Cluster"] = cluster_labels

    # Dataframe hasil klasterisasi
    st.markdown("#### 1. Hasil Klasterisasi")
    st.dataframe(df_result)

    # Karakteristik setiap klaster
    st.markdown("#### 2. Karakteristik Setiap Klaster")
    numeric_cols = df_result.select_dtypes(include=np.number).columns.drop("Cluster")
    cluster_mean = df_result.groupby("Cluster")[numeric_cols].mean().round(3)
    st.markdown("##### Rata-rata Setiap Klaster")
    st.dataframe(cluster_mean)
    cluster_percentage = cluster_mean.div(cluster_mean.sum(axis=1), axis=0) * 100
    cluster_percentage = cluster_percentage.round(2)
    st.markdown("##### Rata-Rata Persentase Klaster (%)")
    st.dataframe(cluster_percentage)
