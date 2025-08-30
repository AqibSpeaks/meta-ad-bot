# dashboard.py

import os
import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = os.getenv("DB_PATH", "ads.db")

# ---------- DB UTILS ----------
def get_connection():
    return sqlite3.connect(DB_PATH)

def load_ads(country=None, category=None, spend_min=None, spend_max=None, days_min=None, days_max=None):
    query = "SELECT * FROM ads WHERE 1=1"
    params = []

    if country:
        query += " AND country = ?"
        params.append(country)

    if category:
        query += " AND category = ?"
        params.append(category)

    if spend_min is not None:
        query += " AND spend >= ?"
        params.append(spend_min)

    if spend_max is not None:
        query += " AND spend <= ?"
        params.append(spend_max)

    if days_min is not None:
        query += " AND days_active >= ?"
        params.append(days_min)

    if days_max is not None:
        query += " AND days_active <= ?"
        params.append(days_max)

    conn = get_connection()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df


# ---------- STREAMLIT APP ----------
st.set_page_config(page_title="Meta Ad Library AI Dashboard", layout="wide")

st.title("📊 Meta Ad Library AI Dashboard")
st.write("Filter and explore active ads collected from the Meta Ad Library API.")

# Sidebar filters
st.sidebar.header("🔎 Filters")

country = st.sidebar.text_input("Country Code (e.g., US, PK, GB)")
category = st.sidebar.text_input("Category/Industry")
spend_min = st.sidebar.number_input("Min Spend", min_value=0, step=100, value=0)
spend_max = st.sidebar.number_input("Max Spend", min_value=0, step=100, value=100000)
days_min = st.sidebar.number_input("Min Days Active", min_value=0, step=1, value=0)
days_max = st.sidebar.number_input("Max Days Active", min_value=0, step=1, value=365)

df = load_ads(
    country=country if country else None,
    category=category if category else None,
    spend_min=spend_min,
    spend_max=spend_max,
    days_min=days_min,
    days_max=days_max,
)

if df.empty:
    st.warning("No ads found with current filters.")
else:
    # Display summary
    st.subheader(f"Found {len(df)} Ads")

    # Data table
    st.dataframe(
        df[["ad_copy", "country", "category", "spend", "likes", "comments", "shares", "days_active"]],
        use_container_width=True
    )

    # Show previews
    st.subheader("Ad Previews")
    for _, row in df.iterrows():
        with st.container():
            st.markdown(f"**Ad Copy:** {row['ad_copy']}")
            if row.get("creative_url"):
                st.image(row["creative_url"], caption="Ad Creative", use_container_width=False)
            if row.get("landing_page"):
                st.markdown(f"[Landing Page]({row['landing_page']})")
            st.write(
                f"Country: {row['country']} | Category: {row['category']} | Spend: {row['spend']} | "
                f"Likes: {row['likes']} | Comments: {row['comments']} | Shares: {row['shares']} | Days Active: {row['days_active']}"
            )
            st.markdown("---")

    # Export options
    st.subheader("⬇️ Export Data")
    export_csv = st.download_button(
        "Export CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="ads_export.csv",
        mime="text/csv",
    )
    export_xlsx = st.download_button(
        "Export Excel",
        data=df.to_excel("ads_export.xlsx", index=False, engine="openpyxl"),
        file_name="ads_export.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
