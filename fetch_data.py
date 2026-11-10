
import requests
import pandas as pd

url = "https://data.cityofnewyork.us/resource/5zyy-y8am.json"

params = {
    "$limit": 100
}

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()

data = response.json()
df = pd.DataFrame(data)

# Important columns for our project
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
    "total_location_based_ghg_1",
    "borough",
    "latitude",
    "longitude",
    "estimated_data_flag"
]

# Check which columns actually exist
available_columns = [
    col for col in selected_columns if col in df.columns
]

df_selected = df[available_columns].copy()

print("\n========== DATASET OVERVIEW ==========")
print("Total records:", len(df))
print("Total available columns:", len(df.columns))

print("\n========== SELECTED DATA ==========")
print(df_selected.head(10).to_string(index=False))

print("\n========== DATA TYPES ==========")
print(df_selected.dtypes)

print("\n========== MISSING VALUES ==========")
print(df_selected.isnull().sum())

print("\n========== MISSING VALUE PERCENTAGE ==========")
print((df_selected.isnull().mean() * 100).round(2))
