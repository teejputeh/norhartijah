# app.py
import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Age vs Fixed Deposits", layout="wide")
st.title("Age Distribution by Fixed Deposits (Boxplot)")

# --- 1) Load data ---
uploaded = st.file_uploader("Upload a CSV that includes columns: 'Fixed_Deposits' and 'age'", type=["csv"])

@st.cache_data
def load_csv(file):
    return pd.read_csv(file)

if uploaded is not None:
    df = load_csv(uploaded)
elif "df" in st.session_state:  # optional: preloaded df
    df = st.session_state["df"]
else:
    st.info("Please upload a CSV to continue.")
    st.stop()

# --- 2) Validate columns ---
required = {"Fixed_Deposits", "age"}
missing = required - set(df.columns)
if missing:
    st.error(f"Missing required columns: {', '.join(missing)}")
    st.stop()

# Coerce types safely
df = df.copy()
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df = df.dropna(subset=["age", "Fixed_Deposits"])
if df.empty:
    st.error("No valid rows after cleaning. Check your data types/values.")
    st.stop()

# --- 3) Sidebar options ---
with st.sidebar:
    st.header("Plot Options")
    fig_w = st.slider("Figure width", 6, 16, 10)
    fig_h = st.slider("Figure height", 4, 12, 6)
    order_opt = st.selectbox(
        "Category order",
        ["Data order", "Alphabetical", "By median age (asc)", "By median age (desc)"],
        index=0
    )
    show_points = st.checkbox("Overlay data points", value=False)
    show_summary = st.checkbox("Show summary table", value=True)

# Determine category order
cats = df["Fixed_Deposits"].astype(str)
if order_opt == "Alphabetical":
    labels = sorted(cats.unique())
elif order_opt.startswith("By median"):
    med = df.groupby(cats)["age"].median().sort_values()
    labels = med.index.tolist()
    if order_opt.endswith("(desc)"):
        labels = labels[::-1]
else:
    # Data order = preserve first-seen order
    labels = list(dict.fromkeys(cats.tolist()))

# Build groups in chosen order
groups = [df.loc[cats == lab, "age"].dropna().values for lab in labels]

# --- 4) Plot (pure Matplotlib, one chart) ---
fig, ax = plt.subplots(figsize=(fig_w, fig_h))
# Boxplot
bp = ax.boxplot(groups, labels=labels, vert=True, patch_artist=False, whis=1.5, showmeans=False)

# Optional: overlay minimal jittered points
if show_points:
    for i, vals in enumerate(groups, start=1):
        if len(vals) == 0:
            continue
        x = np.random.normal(loc=i, scale=0.05, size=len(vals))
        ax.plot(x, vals, linestyle="None", marker="o", markersize=3, alpha=0.6)

ax.set_title("Age Distribution by Fixed Deposits")
ax.set_xlabel("Fixed Deposits")
ax.set_ylabel("Age")
plt.tight_layout()
st.pyplot(fig
