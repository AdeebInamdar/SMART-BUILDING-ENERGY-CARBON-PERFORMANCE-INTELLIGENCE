
import requests
import pyodbc

# -------------------------------
# 1. API CONFIGURATION
# -------------------------------

API_URL = "https://data.cityofnewyork.us/resource/5zyy-y8am.json"

# -------------------------------
# 2. SQL SERVER CONFIGURATION
# -------------------------------

SERVER = r"ADEEB\SQLEXPRESS"
DATABASE = "SmartBuildingEnergyDB"

DRIVER = "ODBC Driver 17 for SQL Server"

connection_string = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

# -------------------------------
# 3. SELECT SOURCE COLUMNS
# -------------------------------

columns = [
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

# -------------------------------
# 4. FETCH API DATA
# -------------------------------

all_records = []

limit = 5000
offset = 0

print("Starting API data extraction...")

while True:

    params = {
        "$select": ",".join(columns),
        "$limit": limit,
        "$offset": offset,
        "$order": "property_id ASC, report_year ASC"
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    batch = response.json()

    if not batch:
        break

    all_records.extend(batch)

    offset += len(batch)

    print(f"Fetched {len(all_records)} records...")

    if len(batch) < limit:
        break

print("\nTotal records fetched:", len(all_records))

# -------------------------------
# 5. CONNECT TO SQL SERVER
# -------------------------------

print("\nConnecting to SQL Server...")

connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

# -------------------------------
# 6. INSERT SOURCE DATA
# -------------------------------

insert_query = """
INSERT INTO dbo.BuildingEnergy_Raw (
    report_year,
    property_id,
    property_name,
    primary_property_type,
    year_built,
    energy_star_score,
    site_eui_kbtu_ft,
    site_energy_use_kbtu,
    electricity_use_grid_purchase_1,
    natural_gas_use_kbtu,
    total_location_based_ghg,
    borough,
    latitude,
    longitude,
    estimated_data_flag
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

values = [
    tuple(record.get(column) for column in columns)
    for record in all_records
]

print("\nInserting records into SQL Server...")

try:
    cursor.fast_executemany = True

    batch_size = 1000

    for start in range(0, len(values), batch_size):
        batch_values = values[start:start + batch_size]

        cursor.executemany(insert_query, batch_values)
        connection.commit()

        print(
            f"Inserted {min(start + batch_size, len(values))}"
            f" / {len(values)} records..."
        )

    print("\nDATA IMPORT COMPLETED SUCCESSFULLY!")

except Exception:
    connection.rollback()
    raise

finally:
    cursor.close()
    connection.close()

print("\nSQL Server connection closed.")
