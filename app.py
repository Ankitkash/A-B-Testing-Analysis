# ============================================================
#  A/B Testing — Streamlit Web App
#  Run locally : streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os, warnings
warnings.filterwarnings('ignore')

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="A/B Testing Analyzer",
    page_icon="🧪",
    layout="wide"
)

# ── CACHED FUNCTIONS ─────────────────────────────────────────
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

@st.cache_data
def clean_data(df):
    return df[
        ((df['group'] == 'control')   & (df['landing_page'] == 'old_page')) |
        ((df['group'] == 'treatment') & (df['landing_page'] == 'new_page'))
    ].drop_duplicates(subset='user_id', keep='first')

@st.cache_data
def compute_stats(df_clean):
    control   = df_clean[df_clean['group'] == 'control']
    treatment = df_clean[df_clean['group'] == 'treatment']
    return {
        'control_n'      : len(control),
        'treatment_n'    : len(treatment),
        'conv_control'   : int(control['converted'].sum()),
        'conv_treatment' : int(treatment['converted'].sum()),
        'rate_control'   : control['converted'].mean(),
        'rate_treatment' : treatment['converted'].mean()
    }

# ── TITLE ────────────────────────────────────────────────────
st.title("🧪 A/B Testing Analyzer")
st.markdown("**Statistical analysis of A/B test data — conversion rates, hypothesis testing, and sample size.**")
st.markdown("---")

# ── SIDEBAR ──────────────────────────────────────────────────
st.sidebar.header("⚙️ Test Parameters")
alpha = st.sidebar.slider("Significance Level (α)", 0.01, 0.10, 0.05, 0.01)
power = st.sidebar.slider("Power (1 - β)", 0.70, 0.95, 0.80, 0.05)
mde   = st.sidebar.slider("Minimum Detectable Effect — MDE (%)", 0.5, 5.0, 1.0, 0.1) / 100
tail  = st.sidebar.radio("Test Type", ["Two-tailed", "One-tailed"])
st.sidebar.markdown("---")
st.sidebar.info("📌 **MDE** = Smallest improvement worth detecting. Smaller MDE = larger sample needed.")

# ── LOAD DATA ────────────────────────────────────────────────
st.header("📂 Step 1: Load Dataset")

DEFAULT_FILE = "ab_data.csv"

if os.path.exists(DEFAULT_FILE):
    with st.spinner("Loading default dataset..."):
        df = load_data(DEFAULT_FILE)
    st.success(f"✅ Loaded default dataset ({len(df):,} rows)")

    uploaded = st.file_uploader("Upload your own ab_data.csv (optional)", type=["csv"])
    if uploaded is not None:
        df = load_data(uploaded)
        st.success(f"✅ Using uploaded dataset ({len(df):,} rows)")
else:
    st.markdown("Download from 👉 [Kaggle — zhangluyuan/ab-testing](https://www.kaggle.com/datasets/zhangluyuan/ab-testing)")
    uploaded = st.file_uploader("Upload ab_data.csv", type=["csv"])
    if uploaded is None:
        st.warning("⬆️ Please upload ab_data.csv to begin analysis.")
        st.stop()
    df = load_data(uploaded)

# ── DATA OVERVIEW ────────────────────────────────────────────
st.header("📊 Step 2: Raw Data Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Rows",     f"{len(df):,}")
col2.metric("Columns",        len(df.columns))
col3.metric("Missing Values", df.isnull().sum().sum())
st.dataframe(df.head(10), use_container_width=True)

# ── CLEAN ────────────────────────────────────────────────────
df_clean = clean_data(df)
s = compute_stats(df_clean)

removed = len(df) - len(df_clean)
st.success(f"✅ Cleaned — {removed:,} rows removed. {len(df_clean):,} rows remaining.")

control_n      = s['control_n']
treatment_n    = s['treatment_n']
conv_control   = s['conv_control']
conv_treatment = s['conv_treatment']
rate_control   = s['rate_control']
rate_treatment = s['rate_treatment']
total_n        = control_n + treatment_n

# ── SRM CHECK ────────────────────────────────────────────────
st.markdown("---")
st.header("🔍 Step 3: Sample Ratio Mismatch (SRM) Check")

chi2_srm, p_srm = stats.chisquare(
    f_obs=[control_n, treatment_n],
    f_exp=[total_n/2, total_n/2]
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Control (n)",   f"{control_n:,}")
col2.metric("Treatment (n)", f"{treatment_n:,}")
col3.metric("χ² statistic",  f"{chi2_srm:.4f}")
col4.metric("SRM p-value",   f"{p_srm:.4f}")

if p_srm < 0.05:
    st.error("⚠️ SRM DETECTED — Investigate randomization.")
else:
    st.success("✅ No SRM — Split looks good.")

# ── EDA ──────────────────────────────────────────────────────
st.markdown("---")
st.header("📈 Step 4: Exploratory Data Analysis")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Control Conv Rate",   f"{rate_control*100:.2f}%")
col2.metric("Treatment Conv Rate", f"{rate_treatment*100:.2f}%")
col3.metric("Absolute Lift", f"{(rate_treatment-rate_control)*100:.4f}%",
            delta=f"{(rate_treatment-rate_control)*100:.4f}%")
col4.metric("Relative Lift", f"{((rate_treatment-rate_control)/rate_control)*100:.2f}%")

fig, axes = plt.subplots(1, 3, figsize=(16, 4))
sns.set_palette("Set2")

axes[0].bar(['Control','Treatment'], [control_n, treatment_n], color=['#4C72B0','#DD8452'])
axes[0].set_title('Group Sizes'); axes[0].set_ylabel('Users')
for i, v in enumerate([control_n, treatment_n]):
    axes[0].text(i, v+100, f'{v:,}', ha='center', fontweight='bold')

axes[1].bar(['Control','Treatment'], [rate_control, rate_treatment], color=['#4C72B0','#DD8452'])
axes[1].set_title('Conversion Rates'); axes[1].set_ylabel('Rate')
axes[1].set_ylim(0, max(rate_control, rate_treatment)*1.3)
for i, v in enumerate([rate_control, rate_treatment]):
    axes[1].text(i, v+0.001, f'{v*100:.2f}%', ha='center', fontweight='bold')

axes[2].bar(['Control','Treatment'], [conv_control, conv_treatment], label='Converted', color='#2ca02c')
axes[2].bar(['Control','Treatment'],
            [control_n-conv_control, treatment_n-conv_treatment],
            bottom=[conv_control, conv_treatment],
            label='Not Converted', color='#d62728')
axes[2].set_title('Converted vs Not Converted'); axes[2].legend()

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# ── HYPOTHESIS TEST ──────────────────────────────────────────
st.markdown("---")
st.header("🧮 Step 5: Two Proportion Z-Test")

st.markdown("""
| Hypothesis | Statement |
|---|---|
| H₀ | p_control = p_treatment |
| H₁ | p_control ≠ p_treatment |
""")

p_pool = (conv_control + conv_treatment) / (control_n + treatment_n)
se     = np.sqrt(p_pool * (1-p_pool) * (1/control_n + 1/treatment_n))
z_stat = (rate_treatment - rate_control) / se
z_crit = stats.norm.ppf(1 - alpha/2) if tail == "Two-tailed" else stats.norm.ppf(1 - alpha)
p_val  = (2 * (1 - stats.norm.cdf(abs(z_stat)))) if tail == "Two-tailed" else (1 - stats.norm.cdf(z_stat))

col1, col2, col3, col4 = st.columns(4)
col1.metric("Pooled p̂",   f"{p_pool:.6f}")
col2.metric("Std Error",   f"{se:.6f}")
col3.metric("Z-statistic", f"{z_stat:.4f}")
col4.metric("p-value",     f"{p_val:.6f}")

if p_val < alpha:
    st.success(f"✅ p-value ({p_val:.4f}) < α ({alpha}) → REJECT H₀ — Statistically Significant!")
else:
    st.error(f"❌ p-value ({p_val:.4f}) ≥ α ({alpha}) → FAIL TO REJECT H₀ — No Significant Difference.")

fig2, ax = plt.subplots(figsize=(10, 3))
x = np.linspace(-4, 4, 400)
ax.plot(x, stats.norm.pdf(x), 'b-', linewidth=2)
ax.axvline(z_stat,  color='red',   linestyle='--', linewidth=2,   label=f'Z = {z_stat:.3f}')
ax.axvline(z_crit,  color='green', linestyle='--', linewidth=1.5, label=f'+z_crit = {z_crit:.3f}')
ax.axvline(-z_crit, color='green', linestyle='--', linewidth=1.5, label=f'-z_crit = {-z_crit:.3f}')
ax.fill_between(np.linspace(z_crit,4,100),  stats.norm.pdf(np.linspace(z_crit,4,100)),  alpha=0.3, color='red', label='Rejection region')
ax.fill_between(np.linspace(-4,-z_crit,100),stats.norm.pdf(np.linspace(-4,-z_crit,100)),alpha=0.3, color='red')
ax.set_title('Standard Normal Distribution — Z-Test')
ax.set_xlabel('Z value'); ax.legend(loc='upper right'); ax.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig2)
plt.close(fig2)

# ── CONFIDENCE INTERVAL ──────────────────────────────────────
st.markdown("---")
st.header("📏 Step 6: Confidence Interval")

se_un   = np.sqrt((rate_control*(1-rate_control)/control_n) +
                  (rate_treatment*(1-rate_treatment)/treatment_n))
diff    = rate_treatment - rate_control
ci_low  = diff - z_crit * se_un
ci_high = diff + z_crit * se_un

col1, col2, col3 = st.columns(3)
col1.metric("Difference", f"{diff*100:.4f}%")
col2.metric("CI Lower",   f"{ci_low*100:.4f}%")
col3.metric("CI Upper",   f"{ci_high*100:.4f}%")

fig3, ax = plt.subplots(figsize=(9, 2.5))
ax.errorbar(x=diff, y=0, xerr=[[diff-ci_low],[ci_high-diff]],
            fmt='o', color='#2ca02c', markersize=10, capsize=12, linewidth=2)
ax.axvline(0, color='red', linestyle='--', linewidth=2, label='No effect (0)')
ax.set_title(f'{int((1-alpha)*100)}% CI for Difference in Conversion Rates')
ax.set_xlabel('Difference (Treatment − Control)'); ax.set_yticks([]); ax.legend()
ax.grid(True, axis='x', alpha=0.3)
plt.tight_layout()
st.pyplot(fig3)
plt.close(fig3)

if ci_low > 0 or ci_high < 0:
    st.success("✅ CI excludes 0 — Statistically Significant")
else:
    st.warning("❌ CI contains 0 — Not Statistically Significant")

# ── SAMPLE SIZE ──────────────────────────────────────────────
st.markdown("---")
st.header("📐 Step 7: Sample Size & Power Analysis")

p_avg   = (rate_control + rate_control + mde) / 2
z_alpha = stats.norm.ppf(1 - alpha/2)
z_beta  = stats.norm.ppf(power)
n_req   = int(np.ceil(((z_alpha+z_beta)**2 * 2 * p_avg * (1-p_avg)) / mde**2))

col1, col2, col3 = st.columns(3)
col1.metric("Required n (per group)", f"{n_req:,}")
col2.metric("Total Required",         f"{n_req*2:,}")
col3.metric("Actual n Used",          f"{control_n:,}")

if control_n >= n_req:
    st.success(f"✅ Sample ({control_n:,}) ≥ required ({n_req:,}) — Adequately powered!")
else:
    st.error(f"⚠️ Sample ({control_n:,}) < required ({n_req:,}) — Underpowered.")

mde_range = np.linspace(0.001, 0.05, 100)
n_range   = [int(np.ceil(((z_alpha+z_beta)**2 * 2 * ((rate_control*2+m)/2) *
             (1-(rate_control*2+m)/2)) / m**2)) for m in mde_range]

fig4, ax = plt.subplots(figsize=(10, 3.5))
ax.plot(mde_range*100, n_range, color='#4C72B0', linewidth=2.5)
ax.axvline(mde*100, color='red',   linestyle='--', linewidth=1.5, label=f'MDE = {mde*100:.1f}%')
ax.axhline(n_req,   color='green', linestyle='--', linewidth=1.5, label=f'Required n = {n_req:,}')
ax.fill_between(mde_range*100, n_range, alpha=0.08, color='#4C72B0')
ax.set_title('Power Curve — Sample Size vs MDE')
ax.set_xlabel('MDE (%)'); ax.set_ylabel('Required n per Group')
ax.legend(); ax.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig4)
plt.close(fig4)

# ── FINAL SUMMARY ────────────────────────────────────────────
st.markdown("---")
st.header("📋 Final Summary & Decision")

summary_df = pd.DataFrame({
    'Metric': ['Control Conv Rate','Treatment Conv Rate','Absolute Lift',
               'Relative Lift','Z-statistic','p-value',
               f'{int((1-alpha)*100)}% CI','Significant?'],
    'Value' : [f"{rate_control*100:.2f}%", f"{rate_treatment*100:.2f}%",
               f"{diff*100:.4f}%", f"{(diff/rate_control)*100:.2f}%",
               f"{z_stat:.4f}", f"{p_val:.6f}",
               f"({ci_low*100:.4f}%, {ci_high*100:.4f}%)",
               "YES ✅" if p_val < alpha else "NO ❌"]
})
st.table(summary_df)

if p_val < alpha:
    st.success("🚀 Decision: Significant difference found. Evaluate practical significance before shipping.")
else:
    st.info("🔁 Decision: No significant difference. Keep control page and iterate on design.")

st.markdown("---")
st.caption("Built with ❤️ using Python & Streamlit | Dataset: Kaggle (zhangluyuan)")