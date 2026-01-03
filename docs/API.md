# 📚 API Reference & Code Documentation

Complete reference for all modules, functions, and classes in the Vendor Analytics Platform.

---

## 📦 Module Overview

```
pipeline/
├── pipeline.py      # Data ingestion & transformation
├── analytics.py     # ML & predictive analytics
├── alerts.py        # Alert generation & notifications
├── watcher.py       # File monitoring
├── config.py        # Configuration management
└── run.py           # Command-line interface
```

---

## 🔧 pipeline.py - Data Pipeline

### Functions

#### `load_excel_files()`
Loads all Excel files from the data folder and ingests them into the database.

**Returns:** `bool` - True if successful, False otherwise

**Example:**
```python
from pipeline import load_excel_files

success = load_excel_files()
if success:
    print("Data loaded successfully")
```

---

#### `ingest_raw_data(df, table_name, engine)`
Ingests a DataFrame into a database table.

**Parameters:**
- `df` (DataFrame): Data to ingest
- `table_name` (str): Name of the table
- `engine` (Engine): SQLAlchemy engine

**Returns:** `bool` - Success status

**Example:**
```python
import pandas as pd
from sqlalchemy import create_engine

df = pd.read_excel('data.xlsx')
engine = create_engine('sqlite:///inventory.db')
success = ingest_raw_data(df, 'my_table', engine)
```

---

#### `create_vendor_summary()`
Creates the vendor_sales_summary table by joining sales and purchases data.

**Returns:** `bool` - Success status

**SQL Logic:**
```sql
SELECT 
    s.VendorName,
    s.Description,
    SUM(s.SalesQuantity) AS TotalSalesQuantity,
    SUM(s.SalesDollars) AS TotalSalesDollars,
    SUM(p.Quantity) AS TotalPurchaseQuantity,
    SUM(p.Dollars) AS TotalPurchaseDollars,
    (SUM(s.SalesDollars) - SUM(p.Dollars)) AS GrossProfit,
    -- ... other calculated fields
FROM sales s
LEFT JOIN purchases p 
    ON s.VendorName = p.VendorName 
    AND s.Description = p.Description
GROUP BY s.VendorName, s.Description
```

---

#### `validate_data()`
Validates data quality and integrity.

**Checks:**
- Table existence and row counts
- Negative values
- Data type consistency

**Returns:** `bool` - True if validation passes

---

#### `run_pipeline(archive=False)`
Executes the complete data pipeline.

**Parameters:**
- `archive` (bool): Whether to archive processed files

**Returns:** `bool` - Success status

**Example:**
```python
from pipeline import run_pipeline

# Run without archiving
run_pipeline(archive=False)

# Run with archiving
run_pipeline(archive=True)
```

---

## 🤖 analytics.py - ML Analytics

### Functions

#### `calculate_vendor_scores(vendor_df)`
Calculates AI-powered vendor performance scores (0-100).

**Parameters:**
- `vendor_df` (DataFrame): Vendor data with metrics

**Returns:** `DataFrame` - Data with performance scores added

**Score Calculation:**
```python
PerformanceScore = (
    ProfitMargin_Normalized * 0.35 +      # 35% weight
    StockTurnover_Normalized * 0.25 +     # 25% weight
    TotalSalesDollars_Normalized * 0.25 + # 25% weight
    EfficiencyRatio_Normalized * 0.15     # 15% weight
)
```

**Example:**
```python
from analytics import calculate_vendor_scores
import pandas as pd

df = pd.read_sql("SELECT * FROM vendor_sales_summary", engine)
scored_df = calculate_vendor_scores(df)
print(scored_df[['VendorName', 'PerformanceScore']].head())
```

---

#### `forecast_demand(sales_df, vendor_name=None, days_ahead=30)`
Forecasts future demand using time series analysis.

**Parameters:**
- `sales_df` (DataFrame): Historical sales data
- `vendor_name` (str, optional): Filter by vendor
- `days_ahead` (int): Forecast horizon in days

**Returns:** `dict` - Forecast results
```python
{
    'forecast_quantity': 1000,
    'forecast_dollars': 15000,
    'confidence': 'Medium'
}
```

**Example:**
```python
from analytics import forecast_demand

forecast = forecast_demand(sales_df, vendor_name='Vendor A', days_ahead=30)
print(f"Expected sales: ${forecast['forecast_dollars']:,.2f}")
```

---

#### `optimize_inventory(vendor_df, sales_df)`
Recommends optimal inventory levels.

**Parameters:**
- `vendor_df` (DataFrame): Vendor summary data
- `sales_df` (DataFrame): Sales history

**Returns:** `tuple` - (recommendations DataFrame, summary dict)

**Calculations:**
- `DemandRate` = TotalSalesQuantity / 365
- `SafetyStock` = DemandRate × LeadTime × 1.5
- `ReorderPoint` = DemandRate × LeadTime + SafetyStock
- `OptimalOrderQuantity` = DemandRate × 30

**Example:**
```python
from analytics import optimize_inventory

recommendations, summary = optimize_inventory(vendor_df, sales_df)
print(f"Overstocked items: {summary['overstocked_items']}")
print(f"Understocked items: {summary['understocked_items']}")
```

---

#### `detect_anomalies(vendor_df)`
Detects unusual vendor behavior using Isolation Forest.

**Parameters:**
- `vendor_df` (DataFrame): Vendor data

**Returns:** `DataFrame` - Vendors flagged as anomalies

**Algorithm:** Isolation Forest with 10% contamination

**Example:**
```python
from analytics import detect_anomalies

anomalies = detect_anomalies(vendor_df)
print(f"Found {len(anomalies)} anomalous vendors")
```

---

#### `optimize_pricing(vendor_df)`
Suggests optimal pricing based on performance.

**Parameters:**
- `vendor_df` (DataFrame): Vendor data

**Returns:** `DataFrame` - Pricing recommendations

**Logic:**
- If ProfitMargin < 20%: Increase price by 5-10%
- If ProfitMargin > 60% and Turnover < 1.0: Decrease by 5%
- Otherwise: Maintain current price

---

## 🔔 alerts.py - Alert System

### Classes

#### `AlertConfig`
Configuration class for alert thresholds and settings.

**Attributes:**
```python
# Email Settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-app-password"
RECIPIENT_EMAILS = ["recipient@example.com"]

# Alert Thresholds
LOW_PROFIT_MARGIN = 15.0
LOW_STOCK_TURNOVER = 0.3
HIGH_INVENTORY_VALUE = 50000
POOR_PERFORMANCE_SCORE = 30

# Priority Levels
PRIORITY_CRITICAL = "🔴 CRITICAL"
PRIORITY_HIGH = "🟠 HIGH"
PRIORITY_MEDIUM = "🟡 MEDIUM"
PRIORITY_LOW = "🟢 LOW"
```

---

#### `AlertType`
Enumeration of alert types.

**Types:**
- `LOW_PROFIT` - Profit margin below threshold
- `NEGATIVE_PROFIT` - Selling at a loss
- `LOW_TURNOVER` - Slow-moving inventory
- `OVERSTOCKED` - Excess inventory
- `UNDERSTOCKED` - Stock below reorder point
- `ANOMALY` - Unusual behavior detected
- `POOR_PERFORMANCE` - Low performance score
- `HIGH_INVENTORY` - High inventory value

---

### Functions

#### `generate_all_alerts()`
Generates all alerts based on current data.

**Returns:** `list` - List of alert dictionaries

**Alert Structure:**
```python
{
    'type': 'Low Profit Margin',
    'priority': '🔴 CRITICAL',
    'vendor': 'Vendor A',
    'description': 'Product 1',
    'metric_value': '12.5%',
    'threshold': '15.0%',
    'message': 'Profit margin below threshold',
    'recommendation': 'Review pricing strategy',
    'timestamp': '2024-01-15 10:30:00',
    'alert_id': 'ALT_20240115103000_1'
}
```

**Example:**
```python
from alerts import generate_all_alerts

alerts = generate_all_alerts()
critical = [a for a in alerts if a['priority'] == '🔴 CRITICAL']
print(f"Found {len(critical)} critical alerts")
```

---

#### `send_email_alert(alerts, recipient=None)`
Sends email notification with alerts.

**Parameters:**
- `alerts` (list): List of alert dictionaries
- `recipient` (str, optional): Override default recipient

**Returns:** `bool` - Success status

**Example:**
```python
from alerts import generate_all_alerts, send_email_alert

alerts = generate_all_alerts()
if alerts:
    send_email_alert(alerts, recipient='manager@company.com')
```

---

#### `run_alert_system(send_email=False)`
Runs the complete alert system.

**Parameters:**
- `send_email` (bool): Whether to send email notifications

**Returns:** `list` - Generated alerts

**Example:**
```python
from alerts import run_alert_system

# Generate and display alerts
alerts = run_alert_system(send_email=False)

# Generate and email alerts
alerts = run_alert_system(send_email=True)
```

---

## 👁️ watcher.py - File Monitor

### Classes

#### `DataFolderHandler(FileSystemEventHandler)`
Handles file system events in the data folder.

**Methods:**

##### `__init__(cooldown=30)`
Initialize handler with cooldown period.

**Parameters:**
- `cooldown` (int): Seconds to wait before re-triggering

---

##### `on_created(event)`
Triggered when a new file is created.

**Parameters:**
- `event` (FileSystemEvent): Event object

**Behavior:**
- Only processes .xlsx files
- Respects cooldown period
- Triggers pipeline automatically

---

### Functions

#### `start_watcher(folder_path='data', cooldown=30)`
Starts watching the data folder for new files.

**Parameters:**
- `folder_path` (str): Path to watch
- `cooldown` (int): Seconds between triggers

**Example:**
```python
from watcher import start_watcher

# Start watching with 30 second cooldown
start_watcher(folder_path='data', cooldown=30)
```

---

## ⚙️ config.py - Configuration

### Variables

```python
# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_FOLDER = BASE_DIR / 'data'
ARCHIVE_FOLDER = DATA_FOLDER / 'archive'
LOG_FOLDER = BASE_DIR / 'logs'
DB_PATH = BASE_DIR / 'inventory.db'

# Database
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Pipeline Settings
PIPELINE_SCHEDULE_HOURS = 24
FILE_WATCH_COOLDOWN = 30

# Data Validation
MIN_RECORDS_THRESHOLD = 10
ALLOWED_FILE_EXTENSIONS = ['.xlsx', '.xls']
```

---

## 🖥️ run.py - CLI Interface

### Main Menu Options

```
1-3:   Data Pipeline (load, schedule, watch)
4-6:   Analytics (ML, scoring, forecasting)
7-9:   Alerts (generate, email, dashboard)
10-11: Dashboards (basic, AI-powered)
12-13: Combined workflows
14:    Validate data
15:    Exit
```

### Usage

```bash
cd pipeline
python run.py
# Select option from menu
```

---

## 📊 Database Schema

### Tables

#### `sales`
Raw sales data from Excel.

**Columns:**
- `VendorName` (TEXT)
- `Description` (TEXT)
- `SalesQuantity` (REAL)
- `SalesDollars` (REAL)
- ... other columns from Excel

---

#### `purchases`
Raw purchase data from Excel.

**Columns:**
- `VendorName` (TEXT)
- `Description` (TEXT)
- `Quantity` (REAL)
- `Dollars` (REAL)
- ... other columns from Excel

---

#### `vendor_sales_summary`
Aggregated vendor performance data.

**Columns:**
- `VendorName` (TEXT)
- `Description` (TEXT)
- `TotalSalesQuantity` (REAL)
- `TotalSalesDollars` (REAL)
- `TotalPurchaseQuantity` (REAL)
- `TotalPurchaseDollars` (REAL)
- `GrossProfit` (REAL)
- `ProfitMargin` (REAL)
- `StockTurnover` (REAL)
- `SalesToPurchaseRatio` (REAL)

---

#### `vendor_performance_scores`
ML-generated performance scores.

**Columns:**
- All columns from vendor_sales_summary
- `PerformanceScore` (REAL) - 0-100 score
- `PerformanceTier` (TEXT) - Excellent/Good/Fair/Poor

---

#### `inventory_recommendations`
Inventory optimization suggestions.

**Columns:**
- `VendorName` (TEXT)
- `Description` (TEXT)
- `DemandRate` (REAL)
- `ReorderPoint` (REAL)
- `OptimalOrderQuantity` (REAL)
- `IsOverstocked` (BOOLEAN)
- `IsUnderstocked` (BOOLEAN)

---

#### `vendor_anomalies`
Detected anomalous vendors.

**Columns:**
- `VendorName` (TEXT)
- `Description` (TEXT)
- `ProfitMargin` (REAL)
- `StockTurnover` (REAL)
- `AnomalyScore` (REAL)

---

#### `pricing_recommendations`
Price optimization suggestions.

**Columns:**
- `VendorName` (TEXT)
- `Description` (TEXT)
- `AvgSalePrice` (REAL)
- `CurrentMarkup` (REAL)
- `PriceRecommendation` (TEXT)
- `RecommendedPrice` (REAL)

---

#### `active_alerts`
Currently active alerts.

**Columns:**
- `alert_id` (TEXT)
- `type` (TEXT)
- `priority` (TEXT)
- `vendor` (TEXT)
- `description` (TEXT)
- `metric_value` (TEXT)
- `threshold` (TEXT)
- `message` (TEXT)
- `recommendation` (TEXT)
- `timestamp` (TEXT)

---

#### `alert_history`
Historical alert records.

**Same columns as active_alerts**

---

## 🔗 Usage Examples

### Complete Workflow Example

```python
from pipeline import run_pipeline
from analytics import run_analytics
from alerts import run_alert_system

# Step 1: Load data
success = run_pipeline(archive=True)

if success:
    # Step 2: Run ML analytics
    run_analytics()
    
    # Step 3: Generate and email alerts
    alerts = run_alert_system(send_email=True)
    
    print(f"✅ Workflow complete! Generated {len(alerts)} alerts")
```

---

### Custom Alert Threshold Example

```python
from alerts import AlertConfig, generate_all_alerts

# Customize thresholds
AlertConfig.LOW_PROFIT_MARGIN = 20.0  # More strict
AlertConfig.LOW_STOCK_TURNOVER = 0.5  # Higher threshold

# Generate alerts with new thresholds
alerts = generate_all_alerts()
```

---

### Query Database Example

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///inventory.db')

# Get top performers
query = """
SELECT VendorName, PerformanceScore, ProfitMargin
FROM vendor_performance_scores
ORDER BY PerformanceScore DESC
LIMIT 10
"""

top_vendors = pd.read_sql(query, engine)
print(top_vendors)
```

---

## 📝 Notes

- All functions include error handling and logging
- Database operations use SQLAlchemy for portability
- ML models use default parameters (can be customized)
- Alert thresholds are configurable in AlertConfig class
- All timestamps are in local system time

---

## 🔄 Version History

- **v1.0** - Initial release with basic pipeline
- **v2.0** - Added ML analytics
- **v3.0** - Added alert system
- **v4.0** - Added interactive dashboards

---

## 🆘 Support

For API questions:
- Check inline code docstrings
- Review example usage above
- Open GitHub issue for bugs
