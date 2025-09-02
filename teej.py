# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Finance Data Boxplot", layout="wide")
st.title("Age Distribution by Fixed Deposits")

# 1) Load data directly from GitHub raw URL
CSV_URL = (
    "https://raw.githubusercontent.com/"
    "teejputeh/norhartijah/refs/heads/main/Finance_data.csv"
)

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

try:
    df = load_data(CSV_URL)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

st.subheader("Raw Data Preview")
st.dataframe(df.head())

# 2) Validate presence of required columns
required_cols = {"Fixed_Deposits", "age"}
missing = required_cols - set(df.columns)
if missing:
    st.error(f"Missing required columns: {', '.join(missing)}")
    st.stop()

# Clean: ensure numeric age and non-null Fixed_Deposits
df_clean = df.copy()
df_clean['age'] = pd.to_numeric(df_clean['age'], errors='coerce')
df_clean = df_clean.dropna(subset=['Fixed_Deposits', 'age'])

if df_clean.empty:
    st.error("No valid data after cleaning. Check your data.")
    st.stop()

# 3) Plot: Seaborn boxplot
st.subheader("Boxplot: Age by Fixed Deposits")

with st.expander("Plot Options"):
    fig_w = st.slider("Figure width", 6.0, 16.0, 10.0)
    fig_h = st.slider("Figure height", 4.0, 12.0, 6.0)
    jitter_points = st.checkbox("Overlay jittered points", False)

fig, ax = plt.subplots(figsize=(fig_w, fig_h))
sns.boxplot(x='Fixed_Deposits', y='age', data=df_clean, ax=ax)

if jitter_points:
    import numpy as np
    for i, grp in enumerate(df_clean.groupby('Fixed_Deposits')['age']):
        cat_val, ages = grp
        x = np.random.normal(loc=i, scale=0.08, size=len(ages))
        ax.plot(x, ages, 'r.', alpha=0.4)

ax.set_title("Age Distribution by Fixed Deposits")
ax.set_xlabel("Fixed Deposits")
ax.set_ylabel("Age")
plt.tight_layout()

st.pyplot(fig)

# 4) Summary statistics
st.subheader("Summary Statistics by Fixed Deposits")

def summarize(grp):
    return {
        "Count": grp.count(),
        "Median": grp.median(),
        "Q1": grp.quantile(0.25),
        "Q3": grp.quantile(0.75),
        "IQR": grp.quantile(0.75) - grp.quantile(0.25),
    }

summary_df = df_clean.groupby('Fixed_Deposits')['age'].apply(lambda grp: pd.Series(summarize(grp)))
summary_df = summary_df.reset_index()

st.dataframe(summary_df)

# 5) Download summary
csv_bytes = summary_df.to_csv(index=False).encode('utf-8')
st.download_button(
    "Download summary as CSV",
    data=csv_bytes,
    file_name="age_fixed_deposits_summary.csv",
    mime="text/csv"
)
