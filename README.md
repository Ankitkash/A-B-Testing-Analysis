# 🧪 A/B Testing Analysis — Landing Page Conversion

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-username-ab-testing.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)

A complete end-to-end A/B testing project using Python — from data cleaning and EDA to hypothesis testing, confidence intervals, and sample size calculation. Deployed as a live interactive web app using Streamlit.

---

## 🌐 Live Demo

👉 **[Open Streamlit App](https://share.streamlit.io/-/build/assets/support_tickets-BE90L2li.jpg)**

> Replace the link above with your actual Streamlit Cloud URL after deployment.

---

## 📌 Problem Statement

An e-commerce company wants to know whether a **new landing page** (treatment) leads to a **higher conversion rate** than the **existing landing page** (control). We run a controlled A/B experiment and analyze the results statistically.

---

## 📂 Dataset

* **Source:** [Kaggle — A/B Testing by zhangluyuan](https://www.kaggle.com/datasets/zhangluyuan/ab-testing)
* **File:** `ab_data.csv`
* **Size:** ~300,000 rows

| Column         | Description                        |
| -------------- | ---------------------------------- |
| `user_id`      | Unique user identifier             |
| `timestamp`    | Time of visit                      |
| `group`        | control / treatment                |
| `landing_page` | old_page / new_page                |
| `converted`    | 1 = converted, 0 = did not convert |

---

## 📁 What's Inside

| File                        | Purpose                                                         |
| --------------------------- | --------------------------------------------------------------- |
| `app.py`                    | Interactive Streamlit web app                                   |
| `ab_testing_analysis.ipynb` | Detailed Jupyter notebook with step-by-step analysis & formulas |
| `requirements.txt`          | Python dependencies                                             |
| `.gitignore`                | Files excluded from Git                                         |

---

## 🔬 Methodology

| Step | What's Done                                  |
| ---- | -------------------------------------------- |
| 1    | Load & explore raw data                      |
| 2    | Clean mismatches & duplicates                |
| 3    | Sample Ratio Mismatch (SRM) check            |
| 4    | EDA — conversion rates, group sizes          |
| 5    | Two Proportion Z-Test (manual + statsmodels) |
| 6    | 95% Confidence Interval                      |
| 7    | Sample size & power analysis                 |

---

## 📊 Results

| Metric                    | Value           |
| ------------------------- | --------------- |
| Control Conversion Rate   | ~12.04%         |
| Treatment Conversion Rate | ~11.88%         |
| Absolute Lift             | -0.16%          |
| Z-statistic               | -1.31           |
| p-value                   | ~0.19           |
| 95% CI                    | (-0.39%, 0.08%) |
| Statistically Significant | ❌ No            |

**Decision:** No significant difference found. Keep the control page.

---

## 🚀 Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/ab-testing-project.git
cd ab-testing-project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download dataset

Get `ab_data.csv` from [Kaggle](https://www.kaggle.com/datasets/zhangluyuan/ab-testing) and place it in the project folder.

### 4. Run the Streamlit app

```bash
streamlit run app.py
```

Or open the notebook:

```bash
jupyter notebook ab_testing_analysis.ipynb
```

---

## 🌍 Deploy on Streamlit Cloud

1. Push this repo to GitHub (must be **public**)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"Create app"**
4. Set:

   * Repository: `<your-username>/ab-testing-project`
   * Branch: `main`
   * Main file: `app.py`
5. Click **Deploy** → live in 2 minutes ✨

---

## 🧠 Key Concepts Covered

* Null & Alternative Hypothesis (H₀ vs H₁)
* Type I & Type II Error
* Two Proportion Z-Test
* Pooled vs Unpooled Standard Error
* Confidence Interval interpretation
* Sample Size & Power Analysis
* Sample Ratio Mismatch (SRM) detection
* Statistical vs Practical Significance

---

## 🛠️ Tech Stack

| Tool                 | Purpose               |
| -------------------- | --------------------- |
| Python 3.10+         | Core language         |
| Pandas               | Data manipulation     |
| NumPy                | Numerical computation |
| SciPy                | Statistical tests     |
| Statsmodels          | Z-test verification   |
| Matplotlib / Seaborn | Visualisation         |
| Streamlit            | Web app deployment    |

---
