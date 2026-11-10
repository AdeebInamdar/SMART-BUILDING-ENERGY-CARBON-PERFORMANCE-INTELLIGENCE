# Smart Building Energy & Carbon Performance Intelligence

## Project Overview

A data analytics and business intelligence project that analyzes building energy consumption, energy efficiency, greenhouse gas emissions, and sustainability performance using NYC building energy disclosure data.

The project transforms raw public API data into an SQL Server database and an interactive three-page Power BI report to support building performance analysis.

## Project Objectives

- Analyze building energy consumption across reporting years.
- Compare energy performance across building types and boroughs.
- Evaluate reported ENERGY STAR scores.
- Examine greenhouse gas emissions and sustainability indicators.
- Present insights through interactive Power BI reports.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | API data extraction and ingestion |
| REST API / JSON | NYC Open Data source |
| SQL Server | Raw data storage |
| SQL | Database queries and data management |
| Power Query (M) | Data cleaning and transformation |
| Power BI | Interactive dashboards and reporting |
| DAX | KPIs and analytical measures |
| Data Modelling | Dimension tables and relationships |

## Data Source

**NYC Building Energy and Water Data Disclosure**

- Source: NYC Open Data
- Dataset ID: `5zyy-y8am`
- API: https://data.cityofnewyork.us/resource/5zyy-y8am.json
- Records imported: 103,259
- Reporting years: 2022–2024

## Project Architecture

```text
NYC Open Data REST API
          |
          v
   Python Data Ingestion
          |
          v
      SQL Server
          |
          v
 Power Query (M)
          |
          v
 Data Model & Relationships
          |
          v
       DAX Measures
          |
          v
   Power BI Dashboard
```

## Power BI Report Pages

### 1. Executive Overview
- Total Buildings
- Total Site Energy
- Average Energy Use Intensity (EUI)
- Total GHG Emissions
- Average ENERGY STAR Score
- Energy consumption by year
- Energy consumption by building type
- GHG emissions by borough

### 2. Energy Performance Analysis
- Energy consumption by year
- Average EUI by building type
- Energy consumption by borough
- Year and building type filters

### 3. Carbon & Sustainability Analysis
- Total GHG emissions
- Average ENERGY STAR score
- GHG emissions by year
- GHG emissions by building type
- ENERGY STAR score by borough
- Data quality note

## Data Modelling

Created dimension tables:

- `DimYear`
- `DimBuildingType`
- `DimBorough`
- `DimProperty`

Main fact table:

- `Fact_BuildingEnergy`

The model uses one-to-many relationships between dimension tables and the fact table.

## Key DAX Measures

- Total Buildings
- Total Site Energy
- Average EUI
- Total GHG Emissions
- Average ENERGY STAR Score
- Energy YoY Change %

## Data Quality Considerations

- Preserved the original imported records in SQL Server.
- Handled missing and invalid measurement values in Power Query.
- Converted relevant columns to appropriate data types.
- Reviewed duplicate property-year records without blindly deleting potentially conflicting records.
- Retained missing geographic coordinates rather than assigning artificial locations.

**Note:** The dataset contains estimated values, missing measurements, and duplicate property-year records. Reported metrics should therefore be interpreted with these limitations in mind.

## Project Outcome

Developed an end-to-end business intelligence workflow connecting public API data ingestion, relational database storage, Power Query transformations, data modelling, DAX calculations, and interactive Power BI reporting.

## Repository Structure

```text
Smart_Building_Energy_Intelligence/
│
├── Dataset/
├── powerbi/
│   └── Smart_Building_Energy_Intelligence.pbix
│
├── python/
│   ├── fetch_data.py
│   ├── inspect_dataset.py
│   ├── inspect_duplicates.py
│   ├── test_sql_connection.py
│   └── load_data_to_sql.py
│
├── sql/
│
└── README.md
```
