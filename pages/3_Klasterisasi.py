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
import joblib

st.set_page_config(
    page_title="Klasterisasi HDBSCAN",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #f0f6ff !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #1a3a5c;
}
[data-testid="stMain"] { background: #f0f6ff !important; }
.main .block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1080px !important;
}
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #d0e4f7 !important;
}
[data-testid="stSidebar"] * { color: #1a5fa8 !important; }

.page-header {
    background: linear-gradient(135deg, #1565c0 0%, #1976d2 55%, #0288d1 100%);
    border-radius: 20px;
    padding: 2.2rem 2.8rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute;
    top: -50px; right: -50px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
}
.page-header::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 40%;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
}
.page-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.25;
    margin: 0 0 0.6rem 0;
}
.page-sub {
    font-size: 0.92rem;
    color: #bbdefb;
    line-height: 1.7;
    margin: 0 0 1.4rem 0;
}
.badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.7rem;
    position: relative;
    z-index: 1;
}
.badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.28);
    border-radius: 999px;
    padding: 0.45rem 1.1rem 0.45rem 0.7rem;
    color: #ffffff;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    cursor: default;
    user-select: none;
}
.badge-icon {
    width: 26px; height: 26px;
    border-radius: 50%;
    background: rgba(255,255,255,0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
}

/* CARD WRAPPERS — hanya dekorasi, tidak membungkus widget */
.card-wrap {
    background: #ffffff;
    border: 1px solid #d4e8f8;
    border-radius: 18px;
    margin-bottom: 1.4rem;
    overflow: hidden;
}
.card-head {
    background: linear-gradient(135deg, #e3f2fd 0%, #eff8ff 100%);
    border-bottom: 1px solid #d4e8f8;
    padding: 1rem 1.6rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.card-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, #1565c0, #0288d1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.card-title {
    font-size: 1rem;
    font-weight: 800;
    color: #1565c0;
    margin: 0;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
/* Padding wrapper untuk konten di bawah card-head */
.card-body-pad {
    padding: 1.2rem 1.6rem 1.4rem 1.6rem;
}
/* Penutup bawah card setelah widget */
.card-bottom {
    padding: 0 1.6rem 1.4rem 1.6rem;
}
.card-close {
    border-radius: 0 0 18px 18px;
}

.step-label {
    font-size: 0.78rem;
    font-weight: 700;
    color: #1976d2;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 1.1rem 0 0.6rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.step-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #d4e8f8;
}

.metric-grid-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 0.8rem 0 0.4rem 0;
}
.metric-grid-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin: 0.8rem 0 0.4rem 0;
}
.metric-card {
    background: linear-gradient(135deg, #e8f4fd 0%, #f0f9ff 100%);
    border: 1px solid #c2dff5;
    border-radius: 14px;
    padding: 1.1rem 1.2rem;
    text-align: center;
}
.metric-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: #7bafd4;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin: 0 0 0.5rem 0;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #1565c0;
    line-height: 1;
    margin: 0;
}

[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #e3f2fd !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid #c2dff5 !important;
    margin-bottom: 1.2rem !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 9px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.05em !important;
    color: #7bafd4 !important;
    padding: 0.5rem 1.2rem !important;
    border: none !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(135deg, #1565c0, #0288d1) !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(21,101,192,0.25) !important;
}

[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-size: 0.9rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #d4e8f8 !important;
}
[data-testid="stSelectbox"] label {
    font-weight: 700 !important;
    color: #1565c0 !important;
    font-size: 0.88rem !important;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #e8f4fd; }
::-webkit-scrollbar-thumb { background: #90caf9; border-radius: 3px; }

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"], .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ── PAGE HEADER ───────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1 class="page-title">KLASTERISASI HDBSCAN<br>&amp; BAYESIAN OPTIMIZATION</h1>
    <p class="page-sub">
        Pipeline lengkap preprocessing data, pemodelan klasterisasi, dan analisis hasil
        menggunakan algoritma HDBSCAN dengan optimasi hyperparameter Bayesian.
    </p>
    <div class="badge-row">
        <div class="badge-pill"><span class="badge-icon">⚙️</span> Preprocessing</div>
        <div class="badge-pill"><span class="badge-icon">🔵</span> Pemodelan</div>
        <div class="badge-pill"><span class="badge-icon">📊</span> Hasil Klasterisasi</div>
    </div>
</div>
""", unsafe_allow_html=True)

if "data" not in st.session_state:
    st.warning("⚠️ Silakan upload dataset terlebih dahulu di halaman Data!")
    st.stop()

df = st.session_state["data"]

menu = st.tabs([
    "⚙️  PREPROCESSING DATA",
    "🔵  PEMODELAN KLASTERISASI",
    "📊  HASIL KLASTERISASI"
])

# ════════════════════════════════════════════════════════════════
# TAB 1 — PREPROCESSING DATA
# ════════════════════════════════════════════════════════════════
with menu[0]:

    # ── 1. STANDARISASI ──────────────────────────────────────
    st.markdown("""
    <div class="card-wrap">
        <div class="card-head">
            <div class="card-icon">📐</div>
            <h2 class="card-title">1. Standarisasi Data</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    data_numeric = df.drop(columns=["Provinsi"])
    scaler = StandardScaler()
    scaled_standard = pd.DataFrame(
        scaler.fit_transform(data_numeric),
        columns=data_numeric.columns
    )
    st.dataframe(scaled_standard, use_container_width=True)

    # ── 2. UJI STATISTIK ─────────────────────────────────────
    st.markdown("""
    <div class="card-wrap">
        <div class="card-head">
            <div class="card-icon">🧪</div>
            <h2 class="card-title">2. Uji Statistik</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    kmo_all, kmo_model = calculate_kmo(scaled_standard)
    chi_square_value, p_value = calculate_bartlett_sphericity(scaled_standard)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Uji Kaiser-Meyer-Olkin (KMO)", f"{kmo_model:.4f}")
        st.caption("Kriteria Nilai KMO > 0.5")
        if kmo_model > 0.5:
            st.success("✅ Data sudah sesuai untuk dilakukan pemodelan")
        else:
            st.error("❌ Data belum sesuai untuk dilakukan pemodelan")
    with col2:
        st.metric("Uji Bartlett (p-value)", f"{p_value:.6f}")
        st.caption("Kriteria p-value < 0.05")
        if p_value < 0.05:
            st.success("✅ Terdapat korelasi signifikan antarvariabel")
            korelasi_ok = True
        else:
            st.warning("⚠️ Tidak terdapat korelasi signifikan antarvariabel")
            korelasi_ok = False

    st.markdown('<div class="step-label">Uji Multikolinieritas — Variance Inflation Factor (VIF)</div>', unsafe_allow_html=True)

    X_vif = scaled_standard.copy()
    vif_data = pd.DataFrame()
    vif_data["Variabel"] = X_vif.columns
    vif_data["VIF"] = [
        variance_inflation_factor(X_vif.values, i)
        for i in range(X_vif.shape[1])
    ]
    st.dataframe(vif_data, use_container_width=True, hide_index=True)

    high_vif = vif_data[vif_data["VIF"] >= 10]
    if not high_vif.empty:
        variabels = ", ".join(high_vif["Variabel"].tolist())
        st.warning(f"⚠️ Variabel {variabels} memiliki nilai VIF ≥ 10 yang mengindikasikan adanya multikolinieritas yang tinggi.")
        multikolinieritas = True
    else:
        st.success("✅ Tidak terdapat multikolinieritas tinggi (VIF < 10)")
        multikolinieritas = False

    # ── 3. DETEKSI OUTLIER ───────────────────────────────────
    st.markdown("""
    <div class="card-wrap">
        <div class="card-head">
            <div class="card-icon">🔎</div>
            <h2 class="card-title">3. Deteksi Outlier — Local Outlier Factor</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    lof = LocalOutlierFactor(n_neighbors=20)
    lof.fit_predict(scaled_standard)
    lof_scores = -lof.negative_outlier_factor_
    df_lof = df.copy()
    df_lof["LOF Score"] = lof_scores
    threshold = lof_scores.std()
    df_lof["Label"] = np.where(df_lof["LOF Score"] > threshold, "Outlier", "Normal")
    st.dataframe(df_lof[["Provinsi", "LOF Score", "Label"]], use_container_width=True, hide_index=True)

    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor('#f7fbff')
    ax.set_facecolor('#f7fbff')
    sns.barplot(
        data=df_lof, x="Provinsi", y="LOF Score", hue="Label",
        palette={"Normal": "#64b5f6", "Outlier": "#ef9a9a"}, ax=ax
    )
    plt.xticks(rotation=90, fontsize=8)
    plt.axhline(threshold, linestyle="--", color="#1565c0", alpha=0.6, label=f"Threshold = {threshold:.2f}")
    ax.set_title("Visualisasi LOF Score per Provinsi", fontsize=12, fontweight='bold', color='#1565c0')
    ax.set_xlabel("Provinsi", fontsize=9, color='#3d6b8e')
    ax.set_ylabel("LOF Score", fontsize=9, color='#3d6b8e')
    ax.legend(fontsize=8)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    for spine in ax.spines.values():
        spine.set_edgecolor('#d4e8f8')
    plt.tight_layout()
    st.pyplot(fig)

    # ── 4. REDUKSI DATA ──────────────────────────────────────
    st.markdown("""
    <div class="card-wrap">
        <div class="card-head">
            <div class="card-icon">📉</div>
            <h2 class="card-title">4. Reduksi Data — Principal Component Analysis</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
        st.dataframe(pca_df, use_container_width=True, hide_index=True)

        valid_pc = pca_df[pca_df["Eigenvalue"] > 1]
        n_components = len(valid_pc)
        if kumulatif[n_components - 1] < 80:
            n_components = np.argmax(kumulatif >= 80) + 1

        st.success(f"✅ Jumlah komponen yang digunakan berdasarkan kriteria eigenvalue > 1 dan proporsi variansi kumulatif ≥ 80% adalah **{n_components} komponen**")

        if ("X_clustering" not in st.session_state or
            st.session_state.get("pca_n_components") != n_components or
            st.session_state.get("pca_input_hash") != joblib.hash(scaled_standard.values)):

            pca_final = PCA(n_components=n_components, svd_solver="full")
            pca_result = pd.DataFrame(
                pca_final.fit_transform(scaled_standard),
                columns=[f"PC{i+1}" for i in range(n_components)]
            )
            st.session_state["X_clustering"] = pca_result
            st.session_state["X_plot"] = pca_result
            st.session_state["pca_n_components"] = n_components
            st.session_state["pca_input_hash"] = joblib.hash(scaled_standard.values)
        else:
            pca_result = st.session_state["X_clustering"]

        st.markdown('<div class="step-label">Hasil Reduksi Data dengan PCA</div>', unsafe_allow_html=True)
        st.dataframe(pca_result, use_container_width=True)
    else:
        st.info("ℹ️ PCA tidak diperlukan karena tidak memenuhi syarat multikolinieritas atau korelasi antarvariabel.")
        st.session_state["X_clustering"] = scaled_standard
        st.session_state["X_plot"] = scaled_standard

# ════════════════════════════════════════════════════════════════
# DCSI HELPERS
# ════════════════════════════════════════════════════════════════
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
    dist = cdist(X_ci[core_i], X_cj[core_j])
    return np.min(dist)

def dcsi_index(X, labels, min_samples):
    mask = labels != -1
    X_valid = X[mask]
    labels_valid = labels[mask]
    clusters = np.unique(labels_valid)
    if len(clusters) < 2:
        return None
    eps_dict, conn_dict = {}, {}
    for c in clusters:
        X_c = X_valid[labels_valid == c]
        eps = get_eps_i(X_c, min_samples)
        eps_dict[c] = eps
        conn_dict[c] = compute_connectedness(X_c, min_samples, eps)
    total, weight_sum = 0, 0
    for ci, cj in combinations(clusters, 2):
        X_ci = X_valid[labels_valid == ci]
        X_cj = X_valid[labels_valid == cj]
        sep = compute_separation(X_ci, X_cj, min_samples, eps_dict[ci], eps_dict[cj])
        max_conn = max(conn_dict[ci], conn_dict[cj])
        if np.isinf(sep) or np.isinf(max_conn) or (sep + max_conn) == 0:
            continue
        score = sep / (sep + max_conn)
        weight = len(X_ci) + len(X_cj)
        total += score * weight
        weight_sum += weight
    return total / weight_sum if weight_sum > 0 else None

if "X_clustering" not in st.session_state:
    with menu[1]:
        st.warning("⚠️ Silakan lakukan preprocessing data terlebih dahulu!")
    st.stop()

X_clustering = st.session_state["X_clustering"].values

# ════════════════════════════════════════════════════════════════
# TAB 2 — PEMODELAN KLASTERISASI
# ════════════════════════════════════════════════════════════════
with menu[1]:

    # ── 1. BAYESIAN OPTIMIZATION ─────────────────────────────
    st.markdown("""
    <div class="card-wrap">
        <div class="card-head">
            <div class="card-icon">🎯</div>
            <h2 class="card-title">1. Pencarian Parameter Optimal — Bayesian Optimization</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Mencari parameter optimal..."):
        def objective(min_cluster_size, min_samples):
            mcs = int(np.floor(min_cluster_size))
            ms  = int(np.floor(min_samples))
            if mcs < 2 or ms < 1 or ms > mcs:
                return -1.0
            clusterer = hdbscan.HDBSCAN(min_cluster_size=mcs, min_samples=ms,
                                         metric="euclidean", core_dist_n_jobs=1)
            labels = clusterer.fit_predict(X_clustering)
            if len(set(labels)) - (1 if -1 in labels else 0) < 2:
                return -1.0
            try:
                return validity_index(X_clustering, labels)
            except:
                return -1.0

        pbounds = {"min_cluster_size": (2, 7), "min_samples": (1, 6)}
        optimizer = BayesianOptimization(f=objective, pbounds=pbounds, random_state=42, verbose=0)
        optimizer.maximize(init_points=8, n_iter=20)

        best_dbcv = optimizer.max["target"]
        final_best_dbcv, final_mcs, final_ms = best_dbcv, None, None

        for mcs in range(2, 8):
            for ms in range(1, 7):
                if ms > mcs:
                    continue
                c = hdbscan.HDBSCAN(min_cluster_size=mcs, min_samples=ms, metric="euclidean")
                lbl = c.fit_predict(X_clustering)
                if len(set(lbl)) - (1 if -1 in lbl else 0) < 2:
                    continue
                try:
                    dbcv = validity_index(X_clustering, lbl)
                    if (dbcv > final_best_dbcv + 1e-9) or (
                        abs(dbcv - final_best_dbcv) < 1e-9 and
                        (final_mcs is None or (mcs, ms) < (final_mcs, final_ms))
                    ):
                        final_best_dbcv, final_mcs, final_ms = dbcv, mcs, ms
                except:
                    continue

        if final_mcs is None:
            bp = min(
                [r for r in optimizer.res if abs(r["target"] - best_dbcv) < 1e-9],
                key=lambda x: (int(np.floor(x["params"]["min_cluster_size"])),
                               int(np.floor(x["params"]["min_samples"])))
            )["params"]
            final_mcs = int(np.floor(bp["min_cluster_size"]))
            final_ms  = int(np.floor(bp["min_samples"]))

        best_min_cluster_size = final_mcs
        best_min_samples      = final_ms
        best_dbcv             = final_best_dbcv

        best_clusterer = hdbscan.HDBSCAN(min_cluster_size=best_min_cluster_size,
                                          min_samples=best_min_samples, metric="euclidean")
        best_labels = best_clusterer.fit_predict(X_clustering)
        n_clusters  = len(set(best_labels)) - (1 if -1 in best_labels else 0)

    st.success("✅ Parameter optimal berhasil ditemukan!")
    st.markdown(f"""
    <div class="metric-grid-4">
        <div class="metric-card">
            <p class="metric-label">min_cluster_size</p>
            <p class="metric-value">{best_min_cluster_size}</p>
        </div>
        <div class="metric-card">
            <p class="metric-label">min_samples</p>
            <p class="metric-value">{best_min_samples}</p>
        </div>
        <div class="metric-card">
            <p class="metric-label">Best DBCV Score</p>
            <p class="metric-value">{best_dbcv:.4f}</p>
        </div>
        <div class="metric-card">
            <p class="metric-label">Jumlah Klaster</p>
            <p class="metric-value">{n_clusters}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    targets      = optimizer.space.target
    iterations   = np.arange(1, len(targets) + 1)
    best_so_far  = np.maximum.accumulate(targets)

    col1, col2 = st.columns(2)
    for fig_col, y_data, title, ylabel, show_hline in [
        (col1, best_so_far, "Best DBCV Over Time",            "Best DBCV Score", False),
        (col2, targets,     "Bayesian Optimization Convergence", "DBCV Score",    True),
    ]:
        with fig_col:
            fig_, ax_ = plt.subplots(figsize=(7, 4))
            fig_.patch.set_facecolor('#f7fbff')
            ax_.set_facecolor('#f7fbff')
            ax_.plot(iterations, y_data, marker='o', color='#1976d2', linewidth=2, markersize=5)
            if show_hline:
                ax_.axhline(best_dbcv, color='#ef5350', linestyle="--",
                            linewidth=1.5, label=f"Best = {best_dbcv:.4f}")
                ax_.legend(fontsize=8)
            ax_.set_title(title, fontsize=11, fontweight='bold', color='#1565c0')
            ax_.set_xlabel("Iterasi", fontsize=9, color='#3d6b8e')
            ax_.set_ylabel(ylabel, fontsize=9, color='#3d6b8e')
            ax_.grid(True, linestyle='--', alpha=0.3)
            for spine in ax_.spines.values():
                spine.set_edgecolor('#d4e8f8')
            plt.tight_layout()
            st.pyplot(fig_)

    # ── 2. SCATTER PLOT ──────────────────────────────────────
    st.markdown("""
    <div class="card-wrap">
        <div class="card-head">
            <div class="card-icon">🗺️</div>
            <h2 class="card-title">2. Visualisasi Scatter Plot Klaster</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    hdbscan_model = hdbscan.HDBSCAN(min_cluster_size=best_min_cluster_size,
                                     min_samples=best_min_samples, prediction_data=True)
    hdbscan_model.fit(X_clustering)
    cluster_labels = hdbscan_model.labels_
    st.session_state["cluster_labels"] = cluster_labels
    df_result = df.copy()
    df_result["Cluster"] = cluster_labels
    st.session_state["df_clustered"] = df_result

    X_plot = st.session_state.get("X_plot", pd.DataFrame(X_clustering))
    xcol, ycol = X_plot.columns[0], X_plot.columns[1]

    unique_labels = sorted(set(cluster_labels))
    n_c = len([l for l in unique_labels if l != -1])
    palette   = sns.color_palette("Set2", n_c)
    color_map = {}
    pi = 0
    for label in unique_labels:
        color_map[label] = "#b0bec5" if label == -1 else palette[pi]; pi += (label != -1)

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#f7fbff')
    ax.set_facecolor('#f7fbff')
    for label in unique_labels:
        idx    = cluster_labels == label
        points = X_plot[idx].reset_index(drop=True)
        color  = color_map[label]
        ax.scatter(points[xcol], points[ycol], s=70,
                   c='#b0bec5' if label == -1 else [color],
                   label='Noise' if label == -1 else f'Klaster {label}',
                   edgecolor='white', linewidth=0.8,
                   alpha=0.55 if label == -1 else 0.92)
        if label != -1 and len(points) >= 3:
            try:
                hull = ConvexHull(points[[xcol, ycol]])
                hull_pts = points.iloc[hull.vertices][[xcol, ycol]]
                ax.add_patch(Polygon(hull_pts.values, closed=True,
                                     facecolor=color, alpha=0.15,
                                     edgecolor=color, linewidth=2))
            except Exception:
                pass

    ax.set_title("Distribusi Klaster HDBSCAN + Bayesian Optimization",
                 fontsize=13, fontweight='bold', color='#1565c0', pad=12)
    ax.set_xlabel(xcol, fontsize=9, color='#3d6b8e')
    ax.set_ylabel(ycol, fontsize=9, color='#3d6b8e')
    ax.set_xticks([]); ax.set_yticks([])
    ax.legend(title="Klaster", fontsize=9, title_fontsize=9)
    ax.grid(True, linestyle='--', alpha=0.3)
    for spine in ax.spines.values():
        spine.set_edgecolor('#d4e8f8')
    plt.tight_layout()
    st.pyplot(fig)

    # ── 3. EVALUASI MODEL ────────────────────────────────────
    st.markdown("""
    <div class="card-wrap">
        <div class="card-head">
            <div class="card-icon">📋</div>
            <h2 class="card-title">3. Evaluasi Model HDBSCAN</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    dbcv_score = validity_index(X_clustering, cluster_labels)
    dcsi_score = dcsi_index(X_clustering, cluster_labels, best_min_samples)

    st.markdown(f"""
    <div class="metric-grid-2">
        <div class="metric-card">
            <p class="metric-label">DBCV Score</p>
            <p class="metric-value">{dbcv_score:.4f}</p>
        </div>
        <div class="metric-card">
            <p class="metric-label">DCSI Score</p>
            <p class="metric-value">{"N/A" if dcsi_score is None else f"{dcsi_score:.4f}"}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Kriteria: DBCV Score > 0.5 dan DCSI Score > 0.5")

    if dcsi_score is not None:
        if dbcv_score > 0.5 and dcsi_score > 0.5:
            st.success("✅ Kualitas klaster sudah baik dengan stabilitas dan pemisahan yang jelas antarklaster.")
        elif dbcv_score > 0.5:
            st.warning("⚠️ Kualitas klaster cukup baik berdasarkan DBCV, namun kurang optimal berdasarkan DCSI.")
        elif dcsi_score > 0.5:
            st.warning("⚠️ Kualitas klaster cukup baik berdasarkan DCSI, namun kurang optimal berdasarkan DBCV.")
        else:
            st.error("❌ Kualitas klaster yang buruk berdasarkan DBCV dan DCSI.")
    else:
        st.warning("⚠️ DCSI tidak dapat dihitung (kurang dari 2 klaster valid).")
        if dbcv_score > 0.5:
            st.success("✅ Kualitas klaster sudah baik berdasarkan DBCV.")
        else:
            st.error("❌ Kualitas klaster kurang optimal berdasarkan DBCV.")

# ════════════════════════════════════════════════════════════════
# TAB 3 — HASIL KLASTERISASI
# ════════════════════════════════════════════════════════════════
with menu[2]:
    if "cluster_labels" not in st.session_state:
        st.warning("⚠️ Silakan jalankan proses klasterisasi terlebih dahulu!")
        st.stop()

    cluster_labels = st.session_state["cluster_labels"]
    df_result      = df.copy()
    df_result["Cluster"] = cluster_labels
    numeric_cols   = df_result.select_dtypes(include=np.number).columns.drop("Cluster")

    # ── 1. HASIL KLASTERISASI ────────────────────────────────
    st.markdown("""
    <div class="card-wrap">
        <div class="card-head">
            <div class="card-icon">📄</div>
            <h2 class="card-title">1. Hasil Klasterisasi</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(df_result, use_container_width=True)

    st.markdown('<div class="step-label">Nilai Rata-rata per Klaster</div>', unsafe_allow_html=True)
    cluster_mean = df_result.groupby("Cluster")[numeric_cols].mean().round(3)
    st.dataframe(cluster_mean, use_container_width=True)

    st.markdown('<div class="step-label">Rata-Rata Persentase per Klaster (%)</div>', unsafe_allow_html=True)
    cluster_percentage = cluster_mean.div(cluster_mean.sum(axis=0), axis=1).mul(100).round(2)
    st.dataframe(cluster_percentage, use_container_width=True)

    # ── 2. KARAKTERISTIK KLASTER ─────────────────────────────
    st.markdown("""
    <div class="card-wrap">
        <div class="card-head">
            <div class="card-icon">🏷️</div>
            <h2 class="card-title">2. Karakteristik Setiap Klaster</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    all_clusters     = sorted(df_result["Cluster"].unique())
    selected_cluster = st.selectbox(
        "Pilih Klaster",
        all_clusters,
        format_func=lambda x: "Noise (-1)" if x == -1 else f"Klaster {x}"
    )

    df_cluster = df_result[df_result["Cluster"] == selected_cluster].reset_index(drop=True)

    st.markdown(
        f'<div class="step-label">{"Noise" if selected_cluster == -1 else f"Klaster {selected_cluster}"}'
        f' — {len(df_cluster)} Provinsi</div>',
        unsafe_allow_html=True
    )
    st.dataframe(df_cluster, use_container_width=True, hide_index=True)

    cluster_mean_all = (
        df_result[df_result["Cluster"] != -1]
        .groupby("Cluster")[numeric_cols].mean().round(3)
    )
    cluster_pct_all = cluster_mean_all.div(cluster_mean_all.sum(axis=0), axis=1).mul(100).round(2)

    st.markdown('<div class="step-label">Karakteristik</div>', unsafe_allow_html=True)

    if selected_cluster == -1:
        st.warning("⚠️ Klaster -1 merupakan noise (tidak tergabung dalam klaster utama manapun).")
        mean_noise = df_cluster[numeric_cols].mean().round(3).to_frame(name="Nilai Rata-rata").T
        if not cluster_mean_all.empty:
            pct_noise = (
                df_cluster[numeric_cols].mean()
                .div(cluster_mean_all.sum(axis=0)) * 100
            ).round(2).to_frame(name="Rata-Rata Persentase (%)").T
            combined_noise = pd.concat([mean_noise, pct_noise])
            combined_noise.index = ["Nilai Rata-rata", "Rata-Rata Persentase (%)"]
        else:
            combined_noise = mean_noise
            combined_noise.index = ["Nilai Rata-rata"]
        st.dataframe(combined_noise, use_container_width=True)
    else:
        mean_row = cluster_mean_all.loc[selected_cluster].to_frame(name="Nilai Rata-rata").T
        pct_row  = cluster_pct_all.loc[selected_cluster].to_frame(name="Rata-Rata Persentase (%)").T
        combined = pd.concat([mean_row, pct_row])
        combined.index = ["Nilai Rata-rata", "Rata-Rata Persentase (%)"]
        st.dataframe(combined, use_container_width=True)
