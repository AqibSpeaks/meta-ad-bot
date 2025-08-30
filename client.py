# app/client.py

import os
import argparse
import requests

# Default backend URL (FastAPI service)
BASE = os.getenv("BASE_URL", "http://localhost:8000")


def sync_ads(country: str, search_terms: str | None = None):
    """
    Call FastAPI backend /sync endpoint to pull active ads
    from Meta Ad Library API for a specific country.
    """
    params = {"country": country}
    if search_terms:
        params["search_terms"] = search_terms

    r = requests.get(f"{BASE}/sync", params=params)

    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        print("❌ Error from backend:", e, r.text)
        return

    data = r.json()
    print("✅ Sync complete")
    print("Count:", data.get("count", 0))
    if "error" in data:
        print("Error:", data["error"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CLI tool to sync Meta Ad Library active ads via FastAPI backend"
    )
    parser.add_argument("country", help="ISO country code, e.g., US, GB, PK")
    parser.add_argument("--search", help="Optional search term (e.g., skincare)", default=None)
    args = parser.parse_args()

    sync_ads(args.country, args.search)
