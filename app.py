# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Meta Ad Bot (Demo)")
st.title("Meta Ad Bot — Streamlit Demo")

st.markdown("Upload a CSV of ads to preview (demo).")

uploaded = st.file_uploader("Upload CSV", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
    st.dataframe(df.head(100))
else:
    st.info("No file uploaded yet — try uploading a small CSV.")
