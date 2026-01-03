"""
Predictive Analytics Engine for Vendor Performance
Includes: Forecasting, Scoring, Optimization, Anomaly Detection
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from pathlib import Path
import logging
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Setup
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / 'inventory.db'
engine = create_engine(f"sqlite:///{DB_PATH}")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ================== DATA LOADING ==================
def load_analytics_data():
    """Load data for analytics"""
    try:
        # Load vendor summary
        vendor_df = pd.read_sql("SELECT * FROM vendor_sales_summary", engine)
        
        # Load sales data
        sales_df = pd.read_sql("SELECT * FROM sales", engine)
        
        # Load purchases data
        purchases_df = pd.read_sql("SELECT * FROM purchases", engine)
        
        logging.info(f"✅ Loaded data: {len(vendor_df)} vendors, {len(sales_df)} sales records")
        return vendor_df, sales_df, purchases_df
    except Exception as e:
        logging.error(f"❌ Failed to load data: {str(e)}")
        return None, None, None

# ================== VENDOR PERFORMANCE SCORING ==================
def calculate_vendor_scores(vendor_df):
    """
    Calculate AI-powered vendor performance scores
    Based on: Profitability, Turnover, Sales Volume, Consistency
    """
    try:
        df = vendor_df.copy()
        
        # Feature engineering
        df['ProfitPerUnit'] = df['GrossProfit'] / df['TotalSalesQuantity'].replace(0, 1)
        df['RevenueShare'] = df['TotalSalesDollars'] / df['TotalSalesDollars'].sum()
        df['EfficiencyRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars'].replace(0, 1)
        
        # Normalize features (0-100 scale)
        features = ['ProfitMargin', 'StockTurnover', 'TotalSalesDollars', 'EfficiencyRatio']
        
        for feature in features:
            if feature in df.columns:
                max_val = df[feature].max()
                if max_val > 0:
                    df[f'{feature}_Normalized'] = (df[feature] / max_val) * 100
                else:
                    df[f'{feature}_Normalized'] = 0
        
        # Calculate composite score (weighted average)
        df['PerformanceScore'] = (
            df['ProfitMargin_Normalized'] * 0.35 +  # 35% weight on profit
            df['StockTurnover_Normalized'] * 0.25 +  # 25% weight on turnover
            df['TotalSalesDollars_Normalized'] * 0.25 +  # 25% weight on sales volume
            df['EfficiencyRatio_Normalized'] * 0.15  # 15% weight on efficiency
        )
        
        # Add performance tier
        df['PerformanceTier'] = pd.cut(
            df['PerformanceScore'],
            bins=[0, 25, 50, 75, 100],
            labels=['Poor', 'Fair', 'Good', 'Excellent']
        )
        
        # Save to database
        df.to_sql('vendor_performance_scores', engine, if_exists='replace', index=False)
        
        logging.info(f"✅ Calculated performance scores for {len(df)} vendors")
        return df
        
    except Exception as e:
        logging.error(f"❌ Failed to calculate scores: {str(e)}")
        return None

# ================== DEMAND FORECASTING ==================
def forecast_demand(sales_df, vendor_name=None, days_ahead=30):
    """
    Forecast future demand using time series analysis
    """
    try:
        df = sales_df.copy()
        
        # Filter by vendor if specified
        if vendor_name:
            df = df[df['VendorName'] == vendor_name]
        
        if len(df) < 10:
            logging.warning(f"⚠️ Insufficient data for forecasting")
            return None
        
        # Aggregate by date (if date column exists)
        if 'SalesDate' in df.columns:
            df['SalesDate'] = pd.to_datetime(df['SalesDate'])
            daily_sales = df.groupby('SalesDate').agg({
                'SalesQuantity': 'sum',
                'SalesDollars': 'sum'
            }).reset_index()
        else:
            # Use rolling averages if no date
            daily_sales = df.groupby(df.index // 100).agg({
                'SalesQuantity': 'sum',
                'SalesDollars': 'sum'
            }).reset_index()
        
        # Simple moving average forecast
        window = min(7, len(daily_sales) // 2)
        daily_sales['SalesQuantity_MA'] = daily_sales['SalesQuantity'].rolling(window=window).mean()
        daily_sales['SalesDollars_MA'] = daily_sales['SalesDollars'].rolling(window=window).mean()
        
        # Forecast next period
        last_avg_qty = daily_sales['SalesQuantity_MA'].iloc[-1]
        last_avg_dollars = daily_sales['SalesDollars_MA'].iloc[-1]
        
        forecast = {
            'forecast_quantity': last_avg_qty * days_ahead,
            'forecast_dollars': last_avg_dollars * days_ahead,
            'confidence': 'Medium' if len(daily_sales) > 30 else 'Low'
        }
        
        logging.info(f"✅ Generated {days_ahead}-day forecast")
        return forecast
        
    except Exception as e:
        logging.error(f"❌ Forecasting failed: {str(e)}")
        return None

# ================== INVENTORY OPTIMIZATION ==================
def optimize_inventory(vendor_df, sales_df):
    """
    Recommend optimal inventory levels based on turnover and demand
    """
    try:
        df = vendor_df.copy()
        
        # Calculate optimal stock levels
        df['DemandRate'] = df['TotalSalesQuantity'] / 365  # Daily demand
        df['LeadTime'] = 7  # Assume 7 days lead time
        df['SafetyStock'] = df['DemandRate'] * df['LeadTime'] * 1.5  # 1.5x buffer
        df['ReorderPoint'] = df['DemandRate'] * df['LeadTime'] + df['SafetyStock']
        df['OptimalOrderQuantity'] = df['DemandRate'] * 30  # 30 days supply
        
        # Identify overstocked items (low turnover + high inventory)
        df['IsOverstocked'] = (df['StockTurnover'] < 0.5) & (df['TotalPurchaseQuantity'] > df['OptimalOrderQuantity'])
        
        # Identify understocked items (high turnover + low inventory)
        df['IsUnderstocked'] = (df['StockTurnover'] > 2.0) & (df['TotalPurchaseQuantity'] < df['ReorderPoint'])
        
        # Save recommendations
        recommendations = df[['VendorName', 'Description', 'DemandRate', 'ReorderPoint', 
                             'OptimalOrderQuantity', 'IsOverstocked', 'IsUnderstocked']]
        recommendations.to_sql('inventory_recommendations', engine, if_exists='replace', index=False)
        
        logging.info(f"✅ Generated inventory recommendations for {len(df)} items")
        
        summary = {
            'overstocked_items': int(df['IsOverstocked'].sum()),
            'understocked_items': int(df['IsUnderstocked'].sum()),
            'optimal_items': int((~df['IsOverstocked'] & ~df['IsUnderstocked']).sum())
        }
        
        return recommendations, summary
        
    except Exception as e:
        logging.error(f"❌ Inventory optimization failed: {str(e)}")
        return None, None

# ================== ANOMALY DETECTION ==================
def detect_anomalies(vendor_df):
    """
    Detect unusual vendor behavior using Isolation Forest
    """
    try:
        df = vendor_df.copy()
        
        # Select features for anomaly detection
        features = ['ProfitMargin', 'StockTurnover', 'TotalSalesDollars', 'SalesToPurchaseRatio']
        X = df[features].fillna(0)
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Train Isolation Forest
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        df['IsAnomaly'] = iso_forest.fit_predict(X_scaled)
        df['AnomalyScore'] = iso_forest.score_samples(X_scaled)
        
        # -1 means anomaly, 1 means normal
        df['IsAnomaly'] = df['IsAnomaly'].map({-1: True, 1: False})
        
        anomalies = df[df['IsAnomaly'] == True][['VendorName', 'Description', 'ProfitMargin', 
                                                   'StockTurnover', 'AnomalyScore']]
        
        anomalies.to_sql('vendor_anomalies', engine, if_exists='replace', index=False)
        
        logging.info(f"✅ Detected {len(anomalies)} anomalies out of {len(df)} vendors")
        return anomalies
        
    except Exception as e:
        logging.error(f"❌ Anomaly detection failed: {str(e)}")
        return None

# ================== PRICE OPTIMIZATION ==================
def optimize_pricing(vendor_df):
    """
    Suggest optimal pricing based on demand elasticity and competition
    """
    try:
        df = vendor_df.copy()
        
        # Calculate average price per unit
        df['AvgSalePrice'] = df['TotalSalesDollars'] / df['TotalSalesQuantity'].replace(0, 1)
        df['AvgPurchasePrice'] = df['TotalPurchaseDollars'] / df['TotalPurchaseQuantity'].replace(0, 1)
        
        # Calculate markup
        df['CurrentMarkup'] = ((df['AvgSalePrice'] - df['AvgPurchasePrice']) / df['AvgPurchasePrice'].replace(0, 1)) * 100
        
        # Recommend price adjustments based on performance
        def recommend_price_adjustment(row):
            if row['ProfitMargin'] < 20:
                return 'Increase by 5-10%'
            elif row['ProfitMargin'] > 60 and row['StockTurnover'] < 1.0:
                return 'Decrease by 5% to boost sales'
            else:
                return 'Maintain current price'
        
        df['PriceRecommendation'] = df.apply(recommend_price_adjustment, axis=1)
        
        # Calculate recommended price
        df['RecommendedPrice'] = df.apply(
            lambda row: row['AvgSalePrice'] * 1.075 if 'Increase' in row['PriceRecommendation']
            else row['AvgSalePrice'] * 0.95 if 'Decrease' in row['PriceRecommendation']
            else row['AvgSalePrice'],
            axis=1
        )
        
        pricing = df[['VendorName', 'Description', 'AvgSalePrice', 'CurrentMarkup', 
                     'PriceRecommendation', 'RecommendedPrice']]
        pricing.to_sql('pricing_recommendations', engine, if_exists='replace', index=False)
        
        logging.info(f"✅ Generated pricing recommendations for {len(df)} items")
        return pricing
        
    except Exception as e:
        logging.error(f"❌ Price optimization failed: {str(e)}")
        return None

# ================== MAIN ANALYTICS PIPELINE ==================
def run_analytics():
    """
    Execute complete predictive analytics pipeline
    """
    logging.info("=" * 70)
    logging.info(f"🤖 ANALYTICS PIPELINE STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info("=" * 70)
    
    # Load data
    logging.info("📥 Loading data...")
    vendor_df, sales_df, purchases_df = load_analytics_data()
    
    if vendor_df is None:
        logging.error("❌ Analytics failed: No data available")
        return False
    
    # 1. Vendor Performance Scoring
    logging.info("🎯 Step 1: Calculating vendor performance scores...")
    scores_df = calculate_vendor_scores(vendor_df)
    
    # 2. Inventory Optimization
    logging.info("📦 Step 2: Optimizing inventory levels...")
    recommendations, summary = optimize_inventory(vendor_df, sales_df)
    if summary:
        logging.info(f"   📊 Overstocked: {summary['overstocked_items']}, Understocked: {summary['understocked_items']}")
    
    # 3. Anomaly Detection
    logging.info("🔍 Step 3: Detecting anomalies...")
    anomalies = detect_anomalies(vendor_df)
    
    # 4. Price Optimization
    logging.info("💰 Step 4: Optimizing pricing...")
    pricing = optimize_pricing(vendor_df)
    
    # 5. Demand Forecasting (for top vendors)
    logging.info("📈 Step 5: Forecasting demand...")
    top_vendors = vendor_df.nlargest(5, 'TotalSalesDollars')['VendorName'].tolist()
    forecasts = {}
    for vendor in top_vendors[:3]:  # Forecast for top 3
        forecast = forecast_demand(sales_df, vendor, days_ahead=30)
        if forecast:
            forecasts[vendor] = forecast
    
    logging.info("=" * 70)
    logging.info(f"✅ ANALYTICS COMPLETED")
    logging.info(f"📊 Generated: Scores, Inventory Recs, Anomalies, Pricing, Forecasts")
    logging.info("=" * 70)
    
    return True

# ================== ENTRY POINT ==================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Predictive Analytics Engine')
    parser.add_argument('--scores-only', action='store_true', help='Only calculate vendor scores')
    parser.add_argument('--forecast-only', action='store_true', help='Only run forecasting')
    
    args = parser.parse_args()
    
    if args.scores_only:
        vendor_df, _, _ = load_analytics_data()
        if vendor_df is not None:
            calculate_vendor_scores(vendor_df)
    elif args.forecast_only:
        _, sales_df, _ = load_analytics_data()
        if sales_df is not None:
            forecast_demand(sales_df, days_ahead=30)
    else:
        run_analytics()
