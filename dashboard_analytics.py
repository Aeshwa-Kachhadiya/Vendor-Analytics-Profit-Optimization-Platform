"""
Enhanced Vendor Analytics Dashboard with Predictive Analytics
Includes: ML Insights, Forecasts, Recommendations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
from datetime import datetime

# ================== PAGE CONFIGURATION ==================
st.set_page_config(
    page_title="🤖 AI-Powered Vendor Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== CUSTOM CSS ==================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1f77b4, #2ca02c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px 0;
    }
    .insight-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ================== DATABASE CONNECTION ==================
@st.cache_resource
def get_database_connection():
    try:
        conn = sqlite3.connect('inventory.db', check_same_thread=False)
        return conn
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return None

# ================== DATA LOADING ==================
@st.cache_data(ttl=300)
def load_vendor_scores():
    conn = get_database_connection()
    if conn:
        try:
            df = pd.read_sql_query("SELECT * FROM vendor_performance_scores", conn)
            return df
        except:
            return pd.DataFrame()
    return pd.DataFrame()

@st.cache_data(ttl=300)
def load_inventory_recs():
    conn = get_database_connection()
    if conn:
        try:
            df = pd.read_sql_query("SELECT * FROM inventory_recommendations", conn)
            return df
        except:
            return pd.DataFrame()
    return pd.DataFrame()

@st.cache_data(ttl=300)
def load_anomalies():
    conn = get_database_connection()
    if conn:
        try:
            df = pd.read_sql_query("SELECT * FROM vendor_anomalies", conn)
            return df
        except:
            return pd.DataFrame()
    return pd.DataFrame()

@st.cache_data(ttl=300)
def load_pricing_recs():
    conn = get_database_connection()
    if conn:
        try:
            df = pd.read_sql_query("SELECT * FROM pricing_recommendations", conn)
            return df
        except:
            return pd.DataFrame()
    return pd.DataFrame()

# ================== MAIN DASHBOARD ==================
def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 AI-Powered Vendor Analytics Dashboard</h1>', 
                unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Performance Scores",
        "📦 Inventory Optimization", 
        "🔍 Anomaly Detection",
        "💰 Price Optimization",
        "📈 Insights & Recommendations"
    ])
    
    # ================== TAB 1: PERFORMANCE SCORES ==================
    with tab1:
        st.header("🎯 Vendor Performance Scoring")
        
        scores_df = load_vendor_scores()
        
        if not scores_df.empty:
            # KPIs
            col1, col2, col3, col4 = st.columns(4)
            
            excellent = len(scores_df[scores_df['PerformanceTier'] == 'Excellent'])
            good = len(scores_df[scores_df['PerformanceTier'] == 'Good'])
            fair = len(scores_df[scores_df['PerformanceTier'] == 'Fair'])
            poor = len(scores_df[scores_df['PerformanceTier'] == 'Poor'])
            
            col1.metric("⭐ Excellent", excellent, f"{(excellent/len(scores_df)*100):.1f}%")
            col2.metric("✅ Good", good, f"{(good/len(scores_df)*100):.1f}%")
            col3.metric("⚠️ Fair", fair, f"{(fair/len(scores_df)*100):.1f}%")
            col4.metric("❌ Poor", poor, f"{(poor/len(scores_df)*100):.1f}%")
            
            st.markdown("---")
            
            # Top Performers
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🏆 Top 10 Performers")
                top10 = scores_df.nlargest(10, 'PerformanceScore')[
                    ['VendorName', 'PerformanceScore', 'PerformanceTier']
                ]
                fig = px.bar(
                    top10,
                    x='PerformanceScore',
                    y='VendorName',
                    orientation='h',
                    color='PerformanceTier',
                    color_discrete_map={
                        'Excellent': '#2ca02c',
                        'Good': '#1f77b4',
                        'Fair': '#ff7f0e',
                        'Poor': '#d62728'
                    },
                    title="Highest Performance Scores"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("📊 Performance Distribution")
                tier_counts = scores_df['PerformanceTier'].value_counts()
                fig = px.pie(
                    values=tier_counts.values,
                    names=tier_counts.index,
                    title="Vendors by Performance Tier",
                    color=tier_counts.index,
                    color_discrete_map={
                        'Excellent': '#2ca02c',
                        'Good': '#1f77b4',
                        'Fair': '#ff7f0e',
                        'Poor': '#d62728'
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed Table
            st.subheader("📋 Detailed Performance Scores")
            display_cols = ['VendorName', 'Description', 'PerformanceScore', 'PerformanceTier',
                          'ProfitMargin', 'StockTurnover', 'TotalSalesDollars']
            st.dataframe(
                scores_df[display_cols].sort_values('PerformanceScore', ascending=False),
                use_container_width=True,
                height=400
            )
        else:
            st.warning("⚠️ No performance scores available. Run analytics first!")
    
    # ================== TAB 2: INVENTORY OPTIMIZATION ==================
    with tab2:
        st.header("📦 Inventory Optimization Recommendations")
        
        inv_df = load_inventory_recs()
        
        if not inv_df.empty:
            # Summary
            col1, col2, col3 = st.columns(3)
            
            overstocked = inv_df['IsOverstocked'].sum()
            understocked = inv_df['IsUnderstocked'].sum()
            optimal = len(inv_df) - overstocked - understocked
            
            col1.metric("🔴 Overstocked Items", overstocked)
            col2.metric("🟡 Understocked Items", understocked)
            col3.metric("🟢 Optimal Items", optimal)
            
            st.markdown("---")
            
            # Alerts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🚨 Overstocked Items")
                if overstocked > 0:
                    overstocked_items = inv_df[inv_df['IsOverstocked'] == True][
                        ['VendorName', 'Description', 'OptimalOrderQuantity']
                    ].head(10)
                    st.dataframe(overstocked_items, use_container_width=True)
                else:
                    st.success("✅ No overstocked items!")
            
            with col2:
                st.subheader("⚠️ Understocked Items")
                if understocked > 0:
                    understocked_items = inv_df[inv_df['IsUnderstocked'] == True][
                        ['VendorName', 'Description', 'ReorderPoint']
                    ].head(10)
                    st.dataframe(understocked_items, use_container_width=True)
                else:
                    st.success("✅ No understocked items!")
            
            # Reorder recommendations
            st.subheader("📊 Reorder Point Analysis")
            top_reorder = inv_df.nlargest(15, 'ReorderPoint')[
                ['VendorName', 'Description', 'DemandRate', 'ReorderPoint', 'OptimalOrderQuantity']
            ]
            fig = px.bar(
                top_reorder,
                x='VendorName',
                y=['ReorderPoint', 'OptimalOrderQuantity'],
                title="Top Items by Reorder Point",
                barmode='group'
            )
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("⚠️ No inventory recommendations available. Run analytics first!")
    
    # ================== TAB 3: ANOMALY DETECTION ==================
    with tab3:
        st.header("🔍 Anomaly Detection")
        
        anomalies_df = load_anomalies()
        
        if not anomalies_df.empty:
            st.warning(f"⚠️ Detected {len(anomalies_df)} unusual vendor behaviors")
            
            # Anomaly details
            st.subheader("🚨 Detected Anomalies")
            st.dataframe(
                anomalies_df[['VendorName', 'Description', 'ProfitMargin', 
                             'StockTurnover', 'AnomalyScore']].sort_values('AnomalyScore'),
                use_container_width=True
            )
            
            # Visualization
            fig = px.scatter(
                anomalies_df,
                x='ProfitMargin',
                y='StockTurnover',
                size=abs(anomalies_df['AnomalyScore']) * 100,
                color='AnomalyScore',
                hover_data=['VendorName', 'Description'],
                title="Anomalous Vendors - Profit vs Turnover",
                color_continuous_scale='RdYlGn_r'
            )
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.success("✅ No anomalies detected! All vendors performing normally.")
    
    # ================== TAB 4: PRICE OPTIMIZATION ==================
    with tab4:
        st.header("💰 Price Optimization Recommendations")
        
        pricing_df = load_pricing_recs()
        
        if not pricing_df.empty:
            # Count recommendations
            increase = len(pricing_df[pricing_df['PriceRecommendation'].str.contains('Increase', na=False)])
            decrease = len(pricing_df[pricing_df['PriceRecommendation'].str.contains('Decrease', na=False)])
            maintain = len(pricing_df[pricing_df['PriceRecommendation'].str.contains('Maintain', na=False)])
            
            col1, col2, col3 = st.columns(3)
            col1.metric("📈 Increase Price", increase)
            col2.metric("📉 Decrease Price", decrease)
            col3.metric("➡️ Maintain Price", maintain)
            
            st.markdown("---")
            
            # Price adjustment recommendations
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Items to Increase Price")
                increase_items = pricing_df[
                    pricing_df['PriceRecommendation'].str.contains('Increase', na=False)
                ].head(10)
                st.dataframe(
                    increase_items[['VendorName', 'Description', 'AvgSalePrice', 
                                  'CurrentMarkup', 'RecommendedPrice']],
                    use_container_width=True
                )
            
            with col2:
                st.subheader("📉 Items to Decrease Price")
                decrease_items = pricing_df[
                    pricing_df['PriceRecommendation'].str.contains('Decrease', na=False)
                ].head(10)
                st.dataframe(
                    decrease_items[['VendorName', 'Description', 'AvgSalePrice', 
                                  'CurrentMarkup', 'RecommendedPrice']],
                    use_container_width=True
                )
            
        else:
            st.warning("⚠️ No pricing recommendations available. Run analytics first!")
    
    # ================== TAB 5: INSIGHTS ==================
    with tab5:
        st.header("💡 AI-Powered Insights & Recommendations")
        
        scores_df = load_vendor_scores()
        inv_df = load_inventory_recs()
        anomalies_df = load_anomalies()
        pricing_df = load_pricing_recs()
        
        # Generate insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="insight-card">
                <h3>🎯 Performance Insights</h3>
                <p>Based on ML analysis of your vendor data</p>
            </div>
            """, unsafe_allow_html=True)
            
            if not scores_df.empty:
                top_vendor = scores_df.nlargest(1, 'PerformanceScore').iloc[0]
                st.info(f"""
                **Top Performer:** {top_vendor['VendorName']}  
                **Score:** {top_vendor['PerformanceScore']:.1f}/100  
                **Profit Margin:** {top_vendor['ProfitMargin']:.1f}%
                """)
        
        with col2:
            st.markdown("""
            <div class="insight-card">
                <h3>📦 Inventory Actions</h3>
                <p>Recommended actions for inventory optimization</p>
            </div>
            """, unsafe_allow_html=True)
            
            if not inv_df.empty:
                overstocked = inv_df['IsOverstocked'].sum()
                understocked = inv_df['IsUnderstocked'].sum()
                
                if overstocked > 0:
                    st.warning(f"⚠️ {overstocked} items are overstocked - consider promotions")
                if understocked > 0:
                    st.error(f"🚨 {understocked} items need reordering immediately")
        
        # Action items
        st.subheader("✅ Recommended Actions")
        
        actions = []
        if not anomalies_df.empty:
            actions.append(f"🔍 Investigate {len(anomalies_df)} vendors with unusual patterns")
        if not pricing_df.empty:
            increase_count = len(pricing_df[pricing_df['PriceRecommendation'].str.contains('Increase', na=False)])
            if increase_count > 0:
                actions.append(f"💰 Consider price increases for {increase_count} low-margin items")
        if not inv_df.empty:
            overstocked = inv_df['IsOverstocked'].sum()
            if overstocked > 0:
                actions.append(f"📦 Run clearance sale for {overstocked} overstocked items")
        
        for i, action in enumerate(actions, 1):
            st.markdown(f"{i}. {action}")
    
    # Footer
    st.markdown("---")
    st.caption(f"🤖 AI Analytics | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
