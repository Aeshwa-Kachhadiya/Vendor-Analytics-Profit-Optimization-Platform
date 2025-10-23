# 📈 Vendor Performance Analysis Project: Driving Profitability

## 🚀 Executive Summary: Strategic Vendor Optimization

| Section | Detail |
| :--- | :--- |
| **Business Problem** | Lack of a data-driven framework to objectively evaluate vendor profitability, leading to sub-optimal purchasing decisions and lower profit margins. |
| **The Solution** | A comprehensive analytical pipeline that calculates key financial KPIs and uses a **Two-Sample T-Test** to statistically validate performance differences. |
| **Key Metrics** | **Gross Profit**, **Profit Margin**, **Stock Turnover**, **Sales-to-Purchase Ratio**. |
| **Number Impact** | **Targeted 5-15% increase in Gross Profit Margin** through strategic vendor consolidation and optimized purchasing terms. |

---

## 🎯 Business Problem

The core challenge is identifying which vendors are true profit drivers versus those that merely contribute to inventory bulk. We need a rigorous, quantitative method for **Vendor Selection for Profitability** and **Product Pricing Optimization**.

This project moves the business beyond anecdotal purchasing to address critical questions:
1.  Which vendors yield the highest **Profit Margin**?
2.  Is the difference in profitability between our best and worst vendors **statistically significant**?
3.  How does operational efficiency (like **Stock Turnover**) correlate with financial success?

---

## 🔬 Methodology: From Ingestion to Statistical Proof

The project follows a robust, three-stage data science workflow:

### 1. Data Ingestion & Setup (`Untitled (1).ipynb`)
* **Purpose:** Establishes a foundation for analysis by loading raw data into a reliable database.
* **Tooling:** **Pandas** and **SQLAlchemy** (using a **SQLite** backend).
* **Process:** Systematically loads all raw data files into the `inventory.db`. A **logging system** is configured to monitor the entire ingestion pipeline for data integrity and traceability.

### 2. Exploratory Data Analysis (EDA) & Aggregation (`Exploratory Data Analysis.ipynb`)
* **Strategy:** Explores database structure, identifies relationships, and plans the aggregation strategy.
* **Output:** Creation of the **`vendor_sales_summary`** master table, which standardizes all purchasing, sales, and inventory data by vendor.

### 3. Core Analysis & Statistical Validation (`Vendor Performance Analysis.ipynb`)
* **KPI Calculation:** Calculates the final vendor performance metrics (Gross Profit, Profit Margin, etc.) using the aggregate table.
* **Statistical Test:** Performs a **Two-Sample T-Test** on the Profit Margin metric. This is the critical step to **statistically prove** the hypothesis that top-tier vendors generate significantly higher margins than low-tier vendors.

---

## 📈 Results & Business Recommendations

### Results Summary
The T-Test is designed to reject the Null Hypothesis (i.e., **P-Value < 0.05**), confirming a **statistically significant difference** in the profit-generating ability between the best and worst vendor groups.

### Business Recommendations
1.  **Vendor Consolidation:** Prioritize purchasing volume toward the top-performing vendors (e.g., top 20%) to maximize volume discounts and profit capture.
2.  **Contract Negotiation:** Use the low **Profit Margin** and **Stock Turnover** metrics from poor performers as leverage to initiate better price terms or explore alternative suppliers.
3.  **Pricing Strategy:** Products sourced from high-margin vendors may allow for more competitive and flexible retail pricing.

---

## 💻 Project Structure

| File Name | Description |
| :--- | :--- |
| `Untitled (1).ipynb` | The primary script for **data ingestion**. Loads raw files into the `inventory.db` SQLite database using SQLAlchemy and sets up logging. |
| `Exploratory Data Analysis.ipynb` | Initial **EDA** notebook. Focuses on data preparation, cleaning, and the creation of the aggregate `vendor_sales_summary` table. |
| `Vendor Performance Analysis.ipynb` | The core analysis notebook. Performs deep dives into vendor metrics, visualizations, and executes the final **Two-Sample T-Test**. |
| `inventory.db` | The resultant **SQLite Database** file containing the prepared data (not typically committed to Git). |

---

## ⚙️ Technologies and Dependencies

| Category | Tools/Skills Used |
| :--- | :--- |
| **Programming** | Python 3.x |
| **Data Manipulation** | **pandas**, **numpy** |
| **Database Management** | **SQLAlchemy**, **sqlite3** |
| **Statistical Modeling** | **scipy.stats** (for T-test) |
| **Visualization** | **matplotlib**, **seaborn** |

---

## ⏭️ Next Steps

1.  **Interactive Dashboard:** Develop a **Tableau/Power BI Dashboard** connected to the final data set to provide real-time, interactive performance monitoring for the purchasing team.
2.  **Predictive Modeling:** Implement a **Time Series Analysis** on sales and inventory to forecast optimal order quantities and proactively manage stock levels for high-impact vendors.
3.  **Granular Analysis:** Extend the analysis to the **Vendor-Product ID** level to identify and capitalize on high-potential SKUs, even from generally underperforming vendors.
