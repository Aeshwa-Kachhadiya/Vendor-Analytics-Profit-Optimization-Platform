# Vendor Performance Analysis 📈

## Project Overview

This project focuses on performing an in-depth **Vendor Performance Analysis** to drive strategic business decisions. By analyzing key purchasing and sales metrics, the goal is to evaluate vendor effectiveness and identify opportunities for **Vendor Selection for Profitability** and **Product Pricing Optimization**. The analysis is conducted on a database containing inventory and sales data, culminating in actionable insights on vendor financial performance.

---

## Key Features and Analysis

The repository contains a complete data science workflow, from raw data ingestion to advanced statistical analysis:

1.  **Automated Data Ingestion (`Untitled (1).ipynb`)**:
    * Sets up a robust logging system to monitor the data pipeline.
    * Utilizes **SQLAlchemy** and **Pandas** to ingest raw data files into a central **SQLite database** named `inventory.db`.

2.  **Exploratory Data Analysis (EDA) (`Exploratory Data Analysis.ipynb`)**:
    * Initial exploration of the database structure, data types, and relationships.
    * Focuses on the aggregation strategy to create the core `vendor_sales_summary` table used for performance metrics calculation.

3.  **Core Vendor Performance Metrics (`Vendor Performance Analysis.ipynb`)**:
    * Calculates and analyzes key financial and operational indicators (KPIs) for each vendor, including **Gross Profit**, **Profit Margin**, **Stock Turnover**, and **Sales to Purchase Ratio**.

4.  **Statistical Validation**:
    * Employs a **Two-Sample T-Test** to statistically compare the profit margins between the top-performing and low-performing vendor groups, providing a data-driven basis for vendor selection.

---

## Project Structure

| File Name | Description |
| :--- | :--- |
| `Untitled (1).ipynb` | The primary script for **data ingestion**. Connects to raw data sources and loads them into the `inventory.db` SQLite database using SQLAlchemy. |
| `Exploratory Data Analysis.ipynb` | Initial **EDA** notebook. Focuses on data preparation, cleaning, and creating the necessary aggregate tables for the analysis. |
| `Vendor Performance Analysis.ipynb` | The core analysis notebook. Performs deep dives into vendor metrics, visualizations, and executes the **T-test** for significance testing. |
| `inventory.db` | The resultant **SQLite Database** (not typically committed to Git) containing the necessary sales and inventory data. |

---

## Technologies and Dependencies

The project is built using Python and the following key libraries:

* **Python 3.x**
* **pandas** and **numpy** (for data manipulation)
* **sqlite3** and **sqlalchemy** (for database operations)
* **matplotlib** and **seaborn** (for data visualization)
* **scipy.stats** (specifically for the T-test)

---
