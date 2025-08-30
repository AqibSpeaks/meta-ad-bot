from fastapi import FastAPI, Query
spend REAL,
currency TEXT,
impressions_lower INTEGER,
impressions_upper INTEGER,
comments TEXT,
likes TEXT,
shares TEXT,
days_active INTEGER,
ad_creation_time TEXT,
ad_delivery_start_time TEXT,
ad_delivery_stop_time TEXT,
publisher_platforms TEXT,
ad_type TEXT,
raw_json TEXT
);
""")
CONN.commit()




def upsert(ad):
# Compute derived fields
start = ad.get("ad_delivery_start_time") or ad.get("ad_creation_time")
stop = ad.get("ad_delivery_stop_time")
start_dt = dt.datetime.fromisoformat(start.replace("Z", "+00:00")) if start else None
stop_dt = dt.datetime.fromisoformat(stop.replace("Z", "+00:00")) if stop else None
days_active = None
if start_dt:
days_active = ((stop_dt or dt.datetime.utcnow()) - start_dt).days
if days_active < 0: days_active = 0


impressions = ad.get("impressions") or {}
imp_low = impressions.get("lower_bound") if isinstance(impressions, dict) else None
imp_high = impressions.get("upper_bound") if isinstance(impressions, dict) else None


CONN.execute(
"""
INSERT INTO ads (
ad_archive_id, page_id, page_name, countries, category, ad_copy,
creative_preview, landing_page_url, spend, currency, impressions_lower,
impressions_upper, comments, likes, shares, days_active,
ad_creation_time, ad_delivery_start_time, ad_delivery_stop_time,
publisher_platforms, ad_type, raw_json
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(ad_archive_id) DO UPDATE SET
page_id=excluded.page_id,
page_name=excluded.page_name,
countries=excluded.countries,
category=excluded.category,
ad_copy=excluded.ad_copy,
creative_preview=excluded.creative_preview,
landing_page_url=excluded.landing_page_url,
spend=excluded.spend,
currency=excluded.currency,
impressions_lower=excluded.impressions_lower,
impressions_upper=excluded.impressions_upper,
comments=excluded.comments,
likes=excluded.likes,
shares=excluded.shares,
days_active=excluded.days_active,
ad_creation_time=excluded.ad_creation_time,
ad_delivery_start_time=excluded.ad_delivery_start_time,
ad_delivery_stop_time=excluded.ad_delivery_stop_time,
publisher_platforms=excluded.publisher_platforms,
ad_type=excluded.ad_type,
raw_json=excluded.raw_json
;
""",
(
ad.get("ad_archive_id"),
ad.get("page_id"),
ad.get("page_name"),
json.dumps(ad.g
