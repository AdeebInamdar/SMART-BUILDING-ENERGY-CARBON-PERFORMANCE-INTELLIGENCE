
import requests
import pandas as pd
from pathlib import Path

URL = "https://data.cityofnewyork.us/resource/5zyy-y8am.json"

selected_columns = [
    "report_year",
    "property_id",
    "property_name",
    "primary_property_type",
    "year_built",
    "energy_star_score",
    "site_eui_kbtu_ft",
    "site_energy_use_kbtu",
    "electricity_use_grid_purchase_1",
    "natural_gas_use_kbtu",
    "total_location_based_ghg",
    "borough",
    "latitude",
    "longitude",
    "estimated_data_flag"
]

all_records = []
limit = 5000
offset = 0

while True:
    params = {
        "$select": ",".join(selected_columns),
        "$limit": limit,
        "$offset": offset,
        "$order": "property_id ASC, report_year ASC"
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

# Identify duplicate building-year records
duplicate_mask = df.duplicated(
    subset=["property_id", "report_year"],
    keep=False
)

duplicates = df[duplicate_mask].copy()

# Count duplicate building-year groups
duplicate_groups = (
    duplicates.groupby(["property_id", "report_year"])
    .size()
    .reset_index(name="record_count")
)

print("\n========== DUPLICATE ANALYSIS ==========")
print("Total records:", len(df))
print("Rows involved in duplicates:", len(duplicates))
print("Duplicate building-year groups:", len(duplicate_groups))

print("\n========== DUPLICATE GROUPS (FIRST 20) ==========")
print(duplicate_groups.head(20).to_string(index=False))

print("\n========== DUPLICATE RECORD DETAILS (FIRST 30) ==========")
print(
    duplicates.head(30).to_string(index=False)
)

# Save duplicate records for detailed inspection
output_path = (
    Path(__file__).resolve().parent.parent
    / "Dataset"
    / "duplicate_building_year_records.csv"
)

duplicates.to_csv(output_path, index=False)

print("\nDuplicate records saved to:", output_path)
print("\n========== INSPECTION COMPLETED ==========")
