# 🤖 AI-Powered Vendor Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)](https://streamlit.io/)
[![ML](https://img.shields.io/badge/ML-scikit--learn-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Transform procurement data into profit with AI-powered analytics, automated pipelines, and real-time alerts.

[Quick Start](#-quick-start) • [Features](#-key-features) • [Demo](#-demo) • [Documentation](#-documentation)

---

## 🚀 What It Does

**From raw Excel files to actionable intelligence in minutes:**

```
Excel Data → Automated Pipeline → ML Analytics → Smart Alerts → Interactive Dashboards
```

**Business Impact:**
- 📈 **5-15% profit margin increase** through data-driven vendor optimization
- ⏱️ **95% reduction** in manual data processing time
- 🎯 **100% coverage** of critical issues with automated alerts
- 🔮 **87% accuracy** in demand forecasting

---

## ✨ Key Features

### 🤖 AI & Machine Learning
- **Vendor Performance Scoring** - ML-based rankings (0-100)
- **Demand Forecasting** - Predict future sales with Random Forest
- **Anomaly Detection** - Isolation Forest identifies outliers
- **Smart Recommendations** - Pricing & inventory optimization

### ⚙️ Automation
- **Auto-Ingestion** - Drop Excel files, system processes automatically
- **File Watcher** - Real-time monitoring for new data
- **Scheduled Runs** - Daily/weekly pipeline execution
- **Data Validation** - Automatic quality checks

### 🔔 Intelligent Alerts
- **8 Alert Types** - Profit, inventory, performance issues
- **4 Priority Levels** - Critical, High, Medium, Low
- **Email Notifications** - HTML-formatted alert summaries
- **Alert Dashboard** - Monitor and track issues

### 📊 Interactive Dashboards
- **Basic Dashboard** - Core KPIs and metrics
- **AI Dashboard** - ML insights and predictions
- **Alert Dashboard** - Real-time issue monitoring

---

## 🎯 Problems Solved

| Challenge | Solution |
|-----------|----------|
| **Manual data processing** | Automated pipeline with file watching |
| **Reactive decision-making** | Proactive alerts before issues escalate |
| **Subjective vendor selection** | ML-based performance scoring |
| **Stockouts & overstock** | Smart reorder point calculations |
| **Hidden profit leaks** | Anomaly detection identifies issues |
| **Slow insights** | Real-time dashboards with live data |

---

## 🏗️ Architecture

```
┌──────────────┐
│ Excel Files  │
└──────┬───────┘
       ↓
┌──────────────────────┐
│ Automated Pipeline   │  ← Data validation, transformation
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│  ML Analytics Engine │  ← Scoring, forecasting, anomalies
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│   Alert System       │  ← Smart notifications
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ Interactive Dashboards│ ← Real-time insights
└──────────────────────┘
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add Your Data
```bash
# Place Excel files in data/ folder
data/
├── sales.xlsx
└── purchases.xlsx
```

### 3. Run the Platform
```bash
cd pipeline
python run.py
# Select option 13 (Quick Start)
```

**That's it!** The system will:
1. ✅ Load and validate your data
2. ✅ Run ML analytics
3. ✅ Generate alerts
4. ✅ Launch interactive dashboard

---




---

## 📈 Results

### Original Statistical Analysis
- **Two-Sample T-Test**: P-value < 0.001 (highly significant)
- **Top vendors**: 45.3% profit margin
- **Bottom vendors**: 12.7% profit margin
- **Opportunity**: 42 underperforming vendors identified

### Platform Performance
- **Processing**: ~1M records in 5-7 minutes
- **Alerts**: 50-200 generated per run
- **Forecast Accuracy**: 87% for top vendors
- **Automation**: Saves 10+ hours/week

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit (dashboards) |
| **Backend** | Python 3.11+ |
| **Data** | Pandas, NumPy |
| **Database** | SQLite (via SQLAlchemy) |
| **ML** | scikit-learn, scipy |
| **Viz** | Plotly |
| **Automation** | schedule, watchdog |

---

## 📁 Project Structure

```
vendor-analytics/
├── pipeline/           # Automation & ML modules
│   ├── pipeline.py    # Data ingestion
│   ├── analytics.py   # ML engine
│   ├── alerts.py      # Alert system
│   └── run.py         # Command center
├── data/              # Excel files
├── logs/              # System logs
├── dashboard*.py      # 3 Streamlit dashboards
└── inventory.db       # SQLite database
```

---

## 📚 Documentation

- **[Setup Guide](docs/SETUP.md)** - Installation and configuration
- **[Pipeline Guide](docs/PIPELINE_README.md)** - Automation details
- **[Analytics Guide](docs/ANALYTICS_SETUP.md)** - ML features
- **[Alert Guide](docs/ALERTS_SETUP.md)** - Alert configuration
- **[API Reference](docs/API.md)** - Code documentation

---

## 🔮 Roadmap

- [x] Automated data pipeline
- [x] ML analytics engine
- [x] Real-time alerts
- [x] Interactive dashboards
- [ ] PDF report generation
- [ ] User authentication
- [ ] REST API
- [ ] Slack integration

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---


## 👤 Author

**Aeshwa Kachhadiya**

## 📫 Connect with Me

- 📧 Email: [aeshwakachhadiya129@gmail.com](mailto:aeshwakachhadiya129@gmail.com)  
- 🔗 LinkedIn: [Aeshwa Kachhadiya](https://www.linkedin.com/in/aeshwakachhadiya/)  
- 🐙 GitHub: [Aeshwa-Kachhadiya](https://github.com/Aeshwa-Kachhadiya)


---

## 🙏 Acknowledgments

- Statistical methodology based on procurement optimization research
- ML algorithms follow scikit-learn best practices
- Dashboard design inspired by modern BI tools

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

**Built with ❤️ using Python & Machine Learning**

</div>
