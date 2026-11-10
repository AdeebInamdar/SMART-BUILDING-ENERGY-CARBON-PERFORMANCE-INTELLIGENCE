
import requests
import pandas as pd

URL = "https://data.cityofnewyork.us/resource/5zyy-y8am.json"

# Fetch records in batches to avoid one oversized request
all_records = []
limit = 5000
offset = 0

while True:
    params = {
        "$limit": limit,
        "$offset": offset,
        "$order": "property_id ASC"
    }

    response = requests.get(URL, params=params, timeout=60)
    response.raise_for_status()

    batch = response.json()

    if not batch:
        break

    all_records.extend(batch)
    print(f"Fetched {len(all_records)} records...")

    offset += len(batch)

    if len(batch) < limit:
        break

df = pd.DataFrame(all_records)

print("\n========== DATASET PROFILE ==========")
print("Total records:", len(df))
print("Total columns:", len(df.columns))

print("\n========== REPORTING YEARS ==========")
print(df["report_year"].value_counts(dropna=False).sort_index())

print("\n========== UNIQUE BUILDINGS ==========")
print("Unique property IDs:", df["property_id"].nunique())

print("\n========== DUPLICATE CHECK ==========")
duplicates = df.duplicated(
    subset=["property_id", "report_year"]
).sum()

print("Duplicate building-year records:", duplicates)

print("\n========== IMPORTANT FIELD COMPLETENESS ==========")

fields = [
    "property_id",
    "report_year",
    "site_energy_use_kbtu",
    "site_eui_kbtu_ft",
    "energy_star_score",
    "total_location_based_ghg",
    "borough",
    "latitude",
    "longitude"
]

for field in fields:
    if field in df.columns:
        missing = df[field].isna().sum()
        unavailable = df[field].astype(str).str.strip().isin(
            ["Not Available", "Not Applicable", ""]
        ).sum()

        print(
            f"{field}: "
            f"Missing={missing}, "
            f"Unavailable={unavailable}"
        )

print("\n========== INSPECTION COMPLETED ==========")
