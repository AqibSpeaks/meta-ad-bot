# insights.py

import os
import sqlite3
import pandas as pd
from collections import Counter

# Optional: Use GPT to summarize patterns (set OPENAI_API_KEY in env if needed)
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    USE_GPT = True
except Exception:
    USE_GPT = False

DB_PATH = os.getenv("DB_PATH", "ads.db")


# ---------- DB UTILS ----------
def get_connection():
    return sqlite3.connect(DB_PATH)

def load_ads():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM ads", conn)
    conn.close()
    return df


# ---------- INSIGHTS ----------
def compute_insights(df: pd.DataFrame, country=None, category=None):
    if df.empty:
        return {"message": "No ads available for insights."}

    insights = {}

    # Filter if needed
    if country:
        df = df[df["country"] == country]
    if category:
        df = df[df["category"] == category]

    if df.empty:
        return {"message": f"No ads found for {country or ''} {category or ''}."}

    # Top ads by engagement
    df["engagement"] = df["likes"] + df["comments"] + df["shares"]
    top_ads = df.sort_values(by="engagement", ascending=False).head(5)

    insights["top_ads"] = top_ads[
        ["ad_copy", "country", "category", "spend", "likes", "comments", "shares", "days_active", "creative_url"]
    ].to_dict(orient="records")

    # Engagement trends
    avg_engagement = df["engagement"].mean()
    max_engagement = df["engagement"].max()
    insights["engagement_summary"] = {
        "avg_engagement": avg_engagement,
        "max_engagement": max_engagement,
        "most_engaging_category": df.groupby("category")["engagement"].mean().idxmax(),
    }

    # Spend trends
    insights["spending_summary"] = {
        "avg_spend": df["spend"].mean() if "spend" in df else None,
        "top_spending_category": df.groupby("category")["spend"].sum().idxmax() if "spend" in df else None,
        "top_country_by_spend": df.groupby("country")["spend"].sum().idxmax() if "spend" in df else None,
    }

    # Creative patterns (most common words in ad copy)
    words = " ".join(df["ad_copy"].astype(str).tolist()).lower().split()
    common_words = Counter(words).most_common(10)
    insights["creative_patterns"] = {"common_words": common_words}

    # GPT summary if available
    if USE_GPT:
        try:
            prompt = f"""
            You are analyzing advertising performance data.
            Summarize insights for these ads:
            - Country: {country or 'All'}
            - Category: {category or 'All'}
            - Top engagement ads: {insights['top_ads']}
            - Engagement summary: {insights['engagement_summary']}
            - Spending summary: {insights['spending_summary']}
            - Creative patterns: {insights['creative_patterns']}
            Provide 5 key insights in plain English.
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
            )
            insights["ai_summary"] = response.choices[0].message.content
        except Exception as e:
            insights["ai_summary"] = f"GPT summary failed: {e}"

    return insights


# ---------- CLI USAGE ----------
if __name__ == "__main__":
    df = load_ads()
    results = compute_insights(df, country="US", category=None)
    print(results)
