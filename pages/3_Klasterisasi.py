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
    page_title="Klasterisasi HDBSCAN dan Bayesian Optimization",
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
.page-title {
    font-size: 3rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.25;
    margin: 0 0 0.6rem 0;
}
.page-sub {
    font-size: 1.1rem;
    color: #bbdefb;
    line-height: 1.7;
    margin: 0;
}

[data-testid="stMarkdownContainer"] h3 {
    background: linear-gradient(135deg, #e3f2fd 0%, #eff8ff 100%);
    border: 1px solid #c2dff5;
    border-radius: 12px;
    padding: 0.75rem 1.2rem;
    margin: 1.4rem 0 0.8rem 0;
    font-size: 1.1rem;
    font-weight: 800;
    color: #1565c0 !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.metric-grid-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 0.8rem 0 1rem 0;
}
.metric-grid-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin: 0.8rem 0 1rem 0;
}
.metric-card {
    background: linear-gradient(135deg, #e8f4fd 0%, #f0f9ff 100%);
    border: 1px solid #c2dff5;
    border-radius: 14px;
    padding: 1.1rem 1.2rem;
    text-align: center;
}
.metric-label {
    font-size: 1rem;
    font-weight: 700;
    color: #7bafd4;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin: 0 0 0.5rem 0;
}
.metric-value {
    font-size: 2rem;
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
[data-testid="stSelectbox"] label {
    font-weight: 700 !important;
    color: #1565c0 !important;
    font-size: 0.88rem !important;
}

.safe-table-wrap {
    overflow-x: auto;
    overflow-y: auto;              
    max-height: 420px;             
    border-radius: 10px;
    border: 1px solid #d4e8f8;
    margin-bottom: 1rem;
}
.safe-table-wrap thead th {
    position: sticky;
    top: 0;
    z-index: 2;
    background: linear-gradient(135deg, #e3f2fd, #eff8ff);
}
.safe-table-wrap table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.82rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #ffffff;
}
.safe-table-wrap thead tr {
    background: linear-gradient(135deg, #e3f2fd, #eff8ff);
}
.safe-table-wrap th {
    padding: 0.6rem 0.9rem;
    text-align: left;
    font-weight: 700;
    color: #1565c0;
    border-bottom: 1px solid #d4e8f8;
    white-space: nowrap;
}
.safe-table-wrap td {
    padding: 0.5rem 0.9rem;
    color: #1a3a5c;
    border-bottom: 1px solid #eaf4fc;
}
.safe-table-wrap tr:last-child td { border-bottom: none; }
.safe-table-wrap tr:hover td { background: #f0f9ff; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #e8f4fd; }
::-webkit-scrollbar-thumb { background: #90caf9; border-radius: 3px; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"], .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# HELPERS
def sec(title):
    st.markdown(f"### {title}")


def step_label(text):
    st.caption(f"🔹 {text.upper()}")


def metric_html(items, cols=4):
    grid_class = f"metric-grid-{cols}"
    cards = "".join(
        f'<div class="metric-card">'
        f'<p class="metric-label">{label}</p>'
        f'<p class="metric-value">{value}</p>'
        f'</div>'
        for label, value in items
    )
    st.markdown(f'<div class="{grid_class}">{cards}</div>', unsafe_allow_html=True)


def safe_table(df_show, max_rows=500, height=420):
    """
    Render DataFrame sebagai HTML table dengan scroll (vertical + horizontal)
    """

    df_render = df_show.head(max_rows).reset_index(drop=True)

    # Header
    headers = "".join(f"<th>{col}</th>" for col in df_render.columns)

    # Rows
    rows = ""
    for _, row in df_render.iterrows():
        cells = "".join(
            f"<td>{round(val, 4) if isinstance(val, float) else val}</td>"
            for val in row.values
        )
        rows += f"<tr>{cells}</tr>"

    html = f"""
    <div class="safe-table-wrap" style="max-height:{height}px;">
        <table>
            <thead><tr>{headers}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

    if len(df_show) > max_rows:
        st.caption(f"⚠️ Menampilkan {max_rows} dari {len(df_show)} baris")

# DCSI HELPERS
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
    return np.where([len(nb) >= min_samples for nb in neighbors])[0]


def compute_connectedness(X_cluster, min_samples, eps_i):
    core_idx = get_core_points(X_cluster, min_samples, eps_i)
    if len(core_idx) < 2:
        return np.inf
    dist_matrix = cdist(X_cluster[core_idx], X_cluster[core_idx])
    return np.max(minimum_spanning_tree(dist_matrix).toarray())


def compute_separation(X_ci, X_cj, min_samples, eps_i, eps_j):
    ci = get_core_points(X_ci, min_samples, eps_i)
    cj = get_core_points(X_cj, min_samples, eps_j)
    if len(ci) == 0 or len(cj) == 0:
        return np.inf
    return np.min(cdist(X_ci[ci], X_cj[cj]))


def dcsi_index(X, labels, min_samples):
    mask = labels != -1
    X_v, lv = X[mask], labels[mask]
    clusters = np.unique(lv)
    if len(clusters) < 2:
        return None
    eps_d  = {c: get_eps_i(X_v[lv == c], min_samples) for c in clusters}
    conn_d = {c: compute_connectedness(X_v[lv == c], min_samples, eps_d[c]) for c in clusters}
    total = weight_sum = 0
    for ci, cj in combinations(clusters, 2):
        sep      = compute_separation(X_v[lv == ci], X_v[lv == cj], min_samples, eps_d[ci], eps_d[cj])
        max_conn = max(conn_d[ci], conn_d[cj])
        if np.isinf(sep) or np.isinf(max_conn) or (sep + max_conn) == 0:
            continue
        w = len(X_v[lv == ci]) + len(X_v[lv == cj])
        total      += sep / (sep + max_conn) * w
        weight_sum += w
    return total / weight_sum if weight_sum > 0 else None


# PREPROCESSING DATA
def run_preprocessing(df):
    data_numeric = df.drop(columns=["Provinsi"])
    scaler = StandardScaler()
    scaled_standard = pd.DataFrame(
        scaler.fit_transform(data_numeric),
        columns=data_numeric.columns
    )

    kmo_all, kmo_model = calculate_kmo(scaled_standard)
    chi_square_value, p_value = calculate_bartlett_sphericity(scaled_standard)

    X_vif = scaled_standard.copy()
    vif_data = pd.DataFrame({
        "Variabel": X_vif.columns,
        "VIF": [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]
    })
    high_vif          = vif_data[vif_data["VIF"] >= 10]
    multikolinieritas = not high_vif.empty
    korelasi_ok       = p_value < 0.05

    lof = LocalOutlierFactor(n_neighbors=20)
    lof.fit_predict(scaled_standard)
    lof_scores = -lof.negative_outlier_factor_
    df_lof = df.copy()
    df_lof["LOF Score"] = lof_scores.round(4)
    threshold = float(lof_scores.std())
    df_lof["Label"] = np.where(df_lof["LOF Score"] > threshold, "Outlier", "Normal")

    pca_result   = None
    pca_df       = None
    n_components = None

    if multikolinieritas and korelasi_ok:
        pca = PCA()
        pca.fit(scaled_standard)
        eigenvalues = pca.explained_variance_
        proporsi    = pca.explained_variance_ratio_ * 100
        kumulatif   = np.cumsum(proporsi)
        pca_df = pd.DataFrame({
            "Komponen": [f"PC{i+1}" for i in range(len(eigenvalues))],
            "Eigenvalue": np.round(eigenvalues, 4),
            "Proporsi Varians (%)": np.round(proporsi, 4),
            "Proporsi Varians Kumulatif (%)": np.round(kumulatif, 4)
        })
        valid_pc     = pca_df[pca_df["Eigenvalue"] > 1]
        n_components = len(valid_pc)
        if kumulatif[n_components - 1] < 80:
            n_components = int(np.argmax(kumulatif >= 80) + 1)

        pca_final  = PCA(n_components=n_components, svd_solver="full")
        pca_result = pd.DataFrame(
            pca_final.fit_transform(scaled_standard),
            columns=[f"PC{i+1}" for i in range(n_components)]
        ).round(6)
        X_clustering = pca_result
        X_plot       = pca_result
    else:
        X_clustering = scaled_standard
        X_plot       = scaled_standard

    return {
        "scaled_standard":   scaled_standard,
        "kmo_model":         float(kmo_model),
        "p_value":           float(p_value),
        "vif_data":          vif_data,
        "high_vif":          high_vif,
        "multikolinieritas": multikolinieritas,
        "korelasi_ok":       korelasi_ok,
        "df_lof":            df_lof,
        "lof_threshold":     threshold,
        "pca_df":            pca_df,
        "n_components":      n_components,
        "pca_result":        pca_result,
        "X_clustering":      X_clustering,
        "X_plot":            X_plot,
    }


# PAGE HEADER
st.markdown("""
<div class="page-header">
    <h1 class="page-title">KLASTERISASI HDBSCAN DAN BAYESIAN OPTIMIZATION</h1>
    <p class="page-sub">
        Pipeline lengkap preprocessing data, pemodelan klasterisasi, dan analisis hasil klasterisasi
        menggunakan algoritma HDBSCAN dan Bayesian Optimization
    </p>
</div>
""", unsafe_allow_html=True)

if "data" not in st.session_state:
    st.warning("Silahkan upload dataset terlebih dahulu di halaman Data!")
    st.stop()

df = st.session_state["data"]
data_hash = joblib.hash(df.values)

# PREPROCESSING
if st.session_state.get("_prep_hash") != data_hash:
    with st.spinner("Memproses data..."):
        prep = run_preprocessing(df)
    st.session_state.update({
        "_prep_hash":         data_hash,
        "_scaled":            prep["scaled_standard"],
        "_kmo":               prep["kmo_model"],
        "_pval":              prep["p_value"],
        "_vif":               prep["vif_data"],
        "_high_vif":          prep["high_vif"],
        "_multikolinieritas": prep["multikolinieritas"],
        "_korelasi_ok":       prep["korelasi_ok"],
        "_df_lof":            prep["df_lof"],
        "_lof_thr":           prep["lof_threshold"],
        "_pca_df":            prep["pca_df"],
        "_n_comp":            prep["n_components"],
        "_pca_result":        prep["pca_result"],
        "X_clustering":       prep["X_clustering"],
        "X_plot":             prep["X_plot"],
    })

scaled_standard   = st.session_state["_scaled"]
kmo_model         = st.session_state["_kmo"]
p_value           = st.session_state["_pval"]
vif_data          = st.session_state["_vif"]
high_vif          = st.session_state["_high_vif"]
multikolinieritas = st.session_state["_multikolinieritas"]
korelasi_ok       = st.session_state["_korelasi_ok"]
df_lof            = st.session_state["_df_lof"]
lof_threshold     = st.session_state["_lof_thr"]
pca_df            = st.session_state["_pca_df"]
n_components      = st.session_state["_n_comp"]
pca_result        = st.session_state["_pca_result"]
X_clustering      = st.session_state["X_clustering"].values

# PEMODELAN KLASTERISASI
if st.session_state.get("_bo_hash") != data_hash:
    with st.spinner("Mencari parameter optimal dengan Bayesian Optimization..."):

        def objective(min_cluster_size, min_samples):
            mcs = int(np.floor(min_cluster_size))
            ms  = int(np.floor(min_samples))
            if mcs < 2 or ms < 1 or ms > mcs:
                return -1.0
            c = hdbscan.HDBSCAN(min_cluster_size=mcs, min_samples=ms,
                                 metric="euclidean", core_dist_n_jobs=1)
            lbl = c.fit_predict(X_clustering)
            if len(set(lbl)) - (1 if -1 in lbl else 0) < 2:
                return -1.0
            try:
                return validity_index(X_clustering, lbl)
            except:
                return -1.0

        optimizer = BayesianOptimization(
            f=objective,
            pbounds={"min_cluster_size": (2, 7), "min_samples": (1, 6)},
            random_state=42, verbose=0
        )
        optimizer.maximize(init_points=8, n_iter=20)

        best_dbcv = optimizer.max["target"]
        final_best_dbcv, final_mcs, final_ms = best_dbcv, None, None

        for mcs in range(2, 8):
            for ms in range(1, 7):
                if ms > mcs:
                    continue
                c   = hdbscan.HDBSCAN(min_cluster_size=mcs, min_samples=ms, metric="euclidean")
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

        best_mcs  = final_mcs
        best_ms   = final_ms
        best_dbcv = final_best_dbcv

        hdbscan_model = hdbscan.HDBSCAN(
            min_cluster_size=best_mcs,
            min_samples=best_ms,
            prediction_data=True
        )
        hdbscan_model.fit(X_clustering)
        cluster_labels = hdbscan_model.labels_
        n_clusters     = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)

        df_result = df.copy()
        df_result["Cluster"] = cluster_labels

        dbcv_score = float(validity_index(X_clustering, cluster_labels))
        _dcsi      = dcsi_index(X_clustering, cluster_labels, best_ms)
        dcsi_score = float(_dcsi) if _dcsi is not None else None

        bo_targets     = [float(v) for v in optimizer.space.target]
        bo_best_so_far = [float(v) for v in np.maximum.accumulate(bo_targets)]
        bo_iterations  = list(range(1, len(bo_targets) + 1))

        st.session_state.update({
            "_bo_hash":        data_hash,
            "_best_mcs":       int(best_mcs),
            "_best_ms":        int(best_ms),
            "_best_dbcv":      float(best_dbcv),
            "_n_clusters":     int(n_clusters),
            "_bo_targets":     bo_targets,
            "_bo_best_so_far": bo_best_so_far,
            "_bo_iterations":  bo_iterations,
            "cluster_labels":  cluster_labels,
            "df_clustered":    df_result,
            "_dbcv_score":     dbcv_score,
            "_dcsi_score":     dcsi_score,
        })

best_mcs       = st.session_state["_best_mcs"]
best_ms        = st.session_state["_best_ms"]
best_dbcv      = st.session_state["_best_dbcv"]
n_clusters     = st.session_state["_n_clusters"]
bo_targets     = st.session_state["_bo_targets"]
bo_best_so_far = st.session_state["_bo_best_so_far"]
bo_iterations  = st.session_state["_bo_iterations"]
cluster_labels = st.session_state["cluster_labels"]
df_result      = st.session_state["df_clustered"]
dbcv_score     = st.session_state["_dbcv_score"]
dcsi_score     = st.session_state["_dcsi_score"]

# TABS — pure render, zero session_state write
menu = st.tabs([
    "PREPROCESSING DATA",
    "PEMODELAN KLASTERISASI",
    "HASIL KLASTERISASI"
])

# TAB PREPROCESSING DATA
with menu[0]:

    sec("1. STANDARISASI DATA")
    safe_table(scaled_standard.round(6))

    sec("2. UJI STATISTIK")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Uji Kaiser-Meyer-Olkin (KMO)", f"{kmo_model:.4f}")
        st.caption("Kriteria Nilai KMO > 0.5")
        if kmo_model > 0.5:
            st.success("Data sudah sesuai untuk dilakukan pemodelan")
        else:
            st.error("Data belum sesuai untuk dilakukan pemodelan")
    with col2:
        st.metric("Uji Bartlett (p-value)", f"{p_value:.6f}")
        st.caption("Kriteria p-value < 0.05")
        if p_value < 0.05:
            st.success("Terdapat korelasi signifikan antarvariabel")
        else:
            st.warning("Tidak terdapat korelasi signifikan antarvariabel")

    step_label("Uji Multikolinieritas (Variance Inflation Factor / VIF)")
    safe_table(vif_data.round(4))
    if not high_vif.empty:
        variabels = ", ".join(high_vif["Variabel"].tolist())
        st.warning(f"Variabel {variabels} memiliki nilai VIF ≥ 10 yang mengindikasikan adanya multikolinieritas tinggi")
    else:
        st.success("Tidak terdapat multikolinieritas tinggi (VIF < 10)")

    sec("3. DETEKSI OUTLIER (LOCAL OUTLIER FACTOR)")
    safe_table(df_lof[["Provinsi", "LOF Score", "Label"]])

    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor('#f7fbff')
    ax.set_facecolor('#f7fbff')
    sns.barplot(data=df_lof, x="Provinsi", y="LOF Score", hue="Label",
                palette={"Normal": "#64b5f6", "Outlier": "#ef9a9a"}, ax=ax)
    plt.xticks(rotation=90, fontsize=8)
    ax.axhline(lof_threshold, linestyle="--", color="#1565c0", alpha=0.7,
               label=f"Threshold = {lof_threshold:.2f}")
    ax.set_title("Visualisasi LOF Score per Provinsi", fontsize=12,
                 fontweight='bold', color='#1565c0')
    ax.set_xlabel("Provinsi", fontsize=9, color='#3d6b8e')
    ax.set_ylabel("LOF Score", fontsize=9, color='#3d6b8e')
    ax.legend(fontsize=8)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    for sp in ax.spines.values():
        sp.set_edgecolor('#d4e8f8')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    sec("4. REDUKSI DATA (PRINCIPAL COMPONENT ANALYSIS)")
    if multikolinieritas and korelasi_ok and pca_df is not None:
        safe_table(pca_df)
        st.success(
            f"Jumlah komponen yang digunakan berdasarkan kriteria nilai eigenvalue > 1 "
            f"dan proporsi variansi kumulatif ≥ 80% adalah {n_components} komponen"
        )
        step_label("HASIL REDUKSI PCA")
        safe_table(pca_result)
    else:
        st.info("PCA tidak diperlukan (tidak memenuhi syarat multikolinieritas atau korelasi)")


# TAB PEMODELAN KLASTERISASI
with menu[1]:

    sec("1. PENCARIAN PARAMETER OPTIMAL (BAYESIAN OPTIMIZATION)")
    st.success("Parameter optimal berhasil ditemukan!")
    metric_html([
        ("min cluster size", best_mcs),
        ("min samples",      best_ms),
        ("Best DBCV Score",  f"{best_dbcv:.4f}"),
        ("Jumlah Klaster",   n_clusters),
    ], cols=4)

    col1, col2 = st.columns(2)
    plot_specs = [
        (col1, bo_best_so_far, "Best DBCV Over Time",              "Best DBCV Score", False),
        (col2, bo_targets,     "Bayesian Optimization Convergence", "DBCV Score",      True),
    ]
    for fig_col, y_data, title, ylabel, show_hline in plot_specs:
        with fig_col:
            fig_, ax_ = plt.subplots(figsize=(7, 4))
            fig_.patch.set_facecolor('#f7fbff')
            ax_.set_facecolor('#f7fbff')
            ax_.plot(bo_iterations, y_data, marker='o', color='#1976d2',
                     linewidth=2, markersize=5)
            if show_hline:
                ax_.axhline(best_dbcv, color='#ef5350', linestyle="--",
                            linewidth=1.5, label=f"Best = {best_dbcv:.4f}")
                ax_.legend(fontsize=8)
            ax_.set_title(title, fontsize=11, fontweight='bold', color='#1565c0')
            ax_.set_xlabel("Iterasi", fontsize=9, color='#3d6b8e')
            ax_.set_ylabel(ylabel, fontsize=9, color='#3d6b8e')
            ax_.grid(True, linestyle='--', alpha=0.3)
            for sp in ax_.spines.values():
                sp.set_edgecolor('#d4e8f8')
            plt.tight_layout()
            st.pyplot(fig_)
            plt.close(fig_)

    sec("2. VISUALISASI SCATTER PLOT")
    X_plot        = st.session_state["X_plot"]
    xcol, ycol    = X_plot.columns[0], X_plot.columns[1]
    unique_labels = sorted(set(cluster_labels))
    palette       = sns.color_palette("Set2", sum(1 for l in unique_labels if l != -1))
    color_map, pi = {}, 0
    for lbl in unique_labels:
        if lbl == -1:
            color_map[lbl] = "#b0bec5"
        else:
            color_map[lbl] = palette[pi]; pi += 1

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#f7fbff')
    ax.set_facecolor('#f7fbff')
    for lbl in unique_labels:
        idx   = cluster_labels == lbl
        pts   = X_plot[idx].reset_index(drop=True)
        color = color_map[lbl]
        ax.scatter(pts[xcol], pts[ycol], s=70,
                   c='#b0bec5' if lbl == -1 else [color],
                   label='Noise' if lbl == -1 else f'Klaster {lbl}',
                   edgecolor='white', linewidth=0.8,
                   alpha=0.55 if lbl == -1 else 0.92)
        if lbl != -1 and len(pts) >= 3:
            try:
                hull = ConvexHull(pts[[xcol, ycol]])
                ax.add_patch(Polygon(pts.iloc[hull.vertices][[xcol, ycol]].values,
                                     closed=True, facecolor=color, alpha=0.15,
                                     edgecolor=color, linewidth=2))
            except:
                pass

    ax.set_title("Distribusi Klaster HDBSCAN + Bayesian Optimization",
                 fontsize=13, fontweight='bold', color='#1565c0', pad=12)
    ax.set_xlabel(xcol, fontsize=9, color='#3d6b8e')
    ax.set_ylabel(ycol, fontsize=9, color='#3d6b8e')
    ax.set_xticks([]); ax.set_yticks([])
    ax.legend(title="Klaster", fontsize=9, title_fontsize=9)
    ax.grid(True, linestyle='--', alpha=0.3)
    for sp in ax.spines.values():
        sp.set_edgecolor('#d4e8f8')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    sec("3. EVALUASI MODEL")
    metric_html([
        ("DBCV Score", f"{dbcv_score:.4f}"),
        ("DCSI Score", "N/A" if dcsi_score is None else f"{dcsi_score:.4f}"),
    ], cols=2)
    st.caption("Kriteria: DBCV Score > 0.5 dan DCSI Score > 0.5")

    if dcsi_score is not None:
        if dbcv_score > 0.5 and dcsi_score > 0.5:
            st.success("Kualitas klaster sudah baik dengan stabilitas dan pemisahan yang jelas antarklaster")
        elif dbcv_score > 0.5:
            st.warning("Kualitas klaster cukup baik berdasarkan DBCV, namun kurang optimal berdasarkan DCSI")
        elif dcsi_score > 0.5:
            st.warning("Kualitas klaster cukup baik berdasarkan DCSI, namun kurang optimal berdasarkan DBCV")
        else:
            st.error("Kualitas klaster yang buruk berdasarkan DBCV dan DCSI")
    else:
        st.warning("DCSI tidak dapat dihitung")
        if dbcv_score > 0.5:
            st.success("Kualitas klaster sudah baik berdasarkan DBCV")
        else:
            st.error("Kualitas klaster kurang optimal berdasarkan DBCV")


# TAB HASIL KLASTERISASI
with menu[2]:

    numeric_cols = df_result.select_dtypes(include=np.number).columns.drop("Cluster")

    sec("1. HASIL KLASTERISASI")
    safe_table(df_result)

    step_label("Nilai Rata-rata per Klaster")
    cluster_mean = df_result.groupby("Cluster")[numeric_cols].mean().round(3)
    safe_table(cluster_mean.reset_index())

    step_label("Rata-Rata Persentase per Klaster (%)")
    cluster_pct = cluster_mean.div(cluster_mean.sum(axis=0), axis=1).mul(100).round(2)
    safe_table(cluster_pct.reset_index())

    sec("2. KARAKTERISTIK KLASTER")
    all_clusters     = sorted(df_result["Cluster"].unique())
    selected_cluster = st.selectbox(
        "Pilih Klaster",
        all_clusters,
        format_func=lambda x: "Noise (-1)" if x == -1 else f"Klaster {x}"
    )
    df_cluster = df_result[df_result["Cluster"] == selected_cluster].reset_index(drop=True)
    label_text = "Noise" if selected_cluster == -1 else f"Klaster {selected_cluster}"
    step_label(f"{label_text} ({len(df_cluster)} Provinsi)")
    safe_table(df_cluster)

    cluster_mean_all = (df_result[df_result["Cluster"] != -1]
                        .groupby("Cluster")[numeric_cols].mean().round(3))
    cluster_pct_all  = cluster_mean_all.div(cluster_mean_all.sum(axis=0), axis=1).mul(100).round(2)

    step_label("Karakteristik")
    if selected_cluster == -1:
        st.warning("Klaster -1 merupakan noise (tidak tergabung dalam klaster utama manapun)")
        mean_noise = df_cluster[numeric_cols].mean().round(3).to_frame("Nilai Rata-rata").T
        if not cluster_mean_all.empty:
            pct_noise = (df_cluster[numeric_cols].mean()
                         .div(cluster_mean_all.sum(axis=0)) * 100).round(2).to_frame("Rata-Rata Persentase (%)").T
            combined  = pd.concat([mean_noise, pct_noise])
            combined.index = ["Nilai Rata-rata", "Rata-Rata Persentase (%)"]
        else:
            combined = mean_noise
            combined.index = ["Nilai Rata-rata"]
        safe_table(combined.reset_index())
    else:
        combined = pd.concat([
            cluster_mean_all.loc[selected_cluster].to_frame("Nilai Rata-rata").T,
            cluster_pct_all.loc[selected_cluster].to_frame("Rata-Rata Persentase (%)").T
        ])
        combined.index = ["Nilai Rata-rata", "Rata-Rata Persentase (%)"]
        safe_table(combined.reset_index())
