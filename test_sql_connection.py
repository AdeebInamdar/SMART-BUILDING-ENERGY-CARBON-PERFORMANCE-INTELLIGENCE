
import pyodbc

server = r"ADEEB\SQLEXPRESS"
database = "SmartBuildingEnergyDB"

# Find an installed SQL Server ODBC driver
drivers = [
    driver for driver in pyodbc.drivers()
    if "SQL Server" in driver
]

if not drivers:
    raise RuntimeError(
        "No SQL Server ODBC driver found. "
        "Please share the installed ODBC drivers."
    )

driver = drivers[-1]

connection_string = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

try:
    connection = pyodbc.connect(
        connection_string,
        timeout=10
    )

    cursor = connection.cursor()
    cursor.execute("SELECT DB_NAME()")

    result = cursor.fetchone()

    print("SQL SERVER CONNECTION SUCCESSFUL")
    print("Connected Database:", result[0])
    print("ODBC Driver:", driver)

    cursor.close()
    connection.close()

except pyodbc.Error as error:
    print("SQL SERVER CONNECTION FAILED")
    print(error)
