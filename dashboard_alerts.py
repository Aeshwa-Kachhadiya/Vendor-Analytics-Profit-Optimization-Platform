"""
Real-Time Alerts Dashboard
Monitor and manage system alerts
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from datetime import datetime, timedelta

# ================== PAGE CONFIGURATION ==================
st.set_page_config(
    page_title="🔔 Alert Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== CUSTOM CSS ==================
st.markdown("""
<style>
    .alert-critical {
        background: linear-gradient(135deg, #c62828, #ef5350);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .alert-high {
        background: linear-gradient(135deg, #ef6c00, #ff9800);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .alert-medium {
        background: linear-gradient(135deg, #f9a825, #fbc02d);
        padding: 20px;
        border-radius: 10px;
        color: #333;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .alert-low {
        background: linear-gradient(135deg, #43a047, #66bb6a);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(90deg, #c62828, #ef6c00, #f9a825);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# ================== DATABASE CONNECTION ==================
@st.cache_resource
def get_db():
    return sqlite3.connect('inventory.db', check_same_thread=False)

# ================== DATA LOADING ==================
@st.cache_data(ttl=60)  # Refresh every minute
def load_active_alerts():
    try:
        return pd.read_sql("SELECT * FROM active_alerts", get_db())
    except:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_alert_history():
    try:
        df = pd.read_sql("SELECT * FROM alert_history", get_db())
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except:
        return pd.DataFrame()

# ================== MAIN DASHBOARD ==================
def main():
    st.markdown('<h1 class="main-header">🔔 Real-Time Alert Dashboard</h1>', 
                unsafe_allow_html=True)
    
    # Refresh button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Refresh Alerts", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    # Load data
    alerts_df = load_active_alerts()
    history_df = load_alert_history()
    
    if alerts_df.empty:
        st.success("✅ **No Active Alerts** - All systems operating normally!")
        st.balloons()
        
        # Show history if available
        if not history_df.empty:
            st.markdown("---")
            st.subheader("📊 Recent Alert History")
            recent = history_df.tail(10)
            st.dataframe(recent[['timestamp', 'priority', 'type', 'vendor', 'message']], 
                        use_container_width=True)
        return
    
    # ================== ALERT SUMMARY ==================
    st.markdown("---")
    st.header("📊 Alert Summary")
    
    # Count by priority
    critical = len(alerts_df[alerts_df['priority'] == '🔴 CRITICAL'])
    high = len(alerts_df[alerts_df['priority'] == '🟠 HIGH'])
    medium = len(alerts_df[alerts_df['priority'] == '🟡 MEDIUM'])
    low = len(alerts_df[alerts_df['priority'] == '🟢 LOW'])
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📋 Total Alerts", len(alerts_df))
    with col2:
        st.metric("🔴 Critical", critical, delta=None if critical == 0 else "Action Required")
    with col3:
        st.metric("🟠 High", high)
    with col4:
        st.metric("🟡 Medium", medium)
    with col5:
        st.metric("🟢 Low", low)
    
    # ================== TABS ==================
    tabs = st.tabs([
        "🔴 Critical Alerts",
        "🟠 High Priority",
        "📊 All Alerts",
        "📈 Analytics",
        "📜 History"
    ])
    
    # ================== TAB 1: CRITICAL ALERTS ==================
    with tabs[0]:
        st.header("🔴 Critical Alerts - Immediate Action Required")
        
        critical_alerts = alerts_df[alerts_df['priority'] == '🔴 CRITICAL']
        
        if critical_alerts.empty:
            st.success("✅ No critical alerts!")
        else:
            st.error(f"⚠️ {len(critical_alerts)} critical alerts require immediate attention!")
            
            for idx, alert in critical_alerts.iterrows():
                st.markdown(f"""
                <div class="alert-critical">
                    <h3>🚨 {alert['type']}</h3>
                    <p><strong>Vendor:</strong> {alert['vendor']}</p>
                    <p><strong>Item:</strong> {alert['description']}</p>
                    <p><strong>Issue:</strong> {alert['message']}</p>
                    <p><strong>📊 Current Value:</strong> {alert['metric_value']} (Threshold: {alert['threshold']})</p>
                    <p><strong>✅ Recommended Action:</strong> {alert['recommendation']}</p>
                    <p><small>⏰ Detected: {alert['timestamp']}</small></p>
                </div>
                """, unsafe_allow_html=True)
    
    # ================== TAB 2: HIGH PRIORITY ==================
    with tabs[1]:
        st.header("🟠 High Priority Alerts")
        
        high_alerts = alerts_df[alerts_df['priority'] == '🟠 HIGH']
        
        if high_alerts.empty:
            st.success("✅ No high priority alerts!")
        else:
            st.warning(f"⚠️ {len(high_alerts)} high priority alerts need attention")
            
            for idx, alert in high_alerts.iterrows():
                st.markdown(f"""
                <div class="alert-high">
                    <h3>⚠️ {alert['type']}</h3>
                    <p><strong>Vendor:</strong> {alert['vendor']}</p>
                    <p><strong>Item:</strong> {alert['description']}</p>
                    <p><strong>Issue:</strong> {alert['message']}</p>
                    <p><strong>📊 Current Value:</strong> {alert['metric_value']} (Threshold: {alert['threshold']})</p>
                    <p><strong>✅ Recommended Action:</strong> {alert['recommendation']}</p>
                    <p><small>⏰ Detected: {alert['timestamp']}</small></p>
                </div>
                """, unsafe_allow_html=True)
    
    # ================== TAB 3: ALL ALERTS ==================
    with tabs[2]:
        st.header("📊 All Active Alerts")
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            priority_filter = st.multiselect(
                "Filter by Priority",
                options=alerts_df['priority'].unique(),
                default=alerts_df['priority'].unique()
            )
        
        with col2:
            type_filter = st.multiselect(
                "Filter by Type",
                options=alerts_df['type'].unique(),
                default=alerts_df['type'].unique()
            )
        
        # Apply filters
        filtered_alerts = alerts_df[
            (alerts_df['priority'].isin(priority_filter)) &
            (alerts_df['type'].isin(type_filter))
        ]
        
        # Display table
        st.dataframe(
            filtered_alerts[[
                'priority', 'type', 'vendor', 'description', 
                'message', 'metric_value', 'recommendation', 'timestamp'
            ]].sort_values('priority'),
            use_container_width=True,
            height=500
        )
        
        # Download button
        csv = filtered_alerts.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Alert Report",
            data=csv,
            file_name=f"alerts_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    # ================== TAB 4: ANALYTICS ==================
    with tabs[3]:
        st.header("📈 Alert Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Alerts by priority
            st.subheader("Alerts by Priority")
            priority_counts = alerts_df['priority'].value_counts()
            fig = px.pie(
                values=priority_counts.values,
                names=priority_counts.index,
                title="Alert Distribution by Priority",
                color=priority_counts.index,
                color_discrete_map={
                    '🔴 CRITICAL': '#c62828',
                    '🟠 HIGH': '#ef6c00',
                    '🟡 MEDIUM': '#f9a825',
                    '🟢 LOW': '#43a047'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Alerts by type
            st.subheader("Alerts by Type")
            type_counts = alerts_df['type'].value_counts()
            fig = px.bar(
                x=type_counts.index,
                y=type_counts.values,
                title="Alert Distribution by Type",
                labels={'x': 'Alert Type', 'y': 'Count'},
                color=type_counts.values,
                color_continuous_scale='Reds'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Top vendors with alerts
        st.subheader("🏢 Vendors with Most Alerts")
        vendor_counts = alerts_df['vendor'].value_counts().head(10)
        fig = px.bar(
            x=vendor_counts.values,
            y=vendor_counts.index,
            orientation='h',
            title="Top 10 Vendors by Alert Count",
            labels={'x': 'Number of Alerts', 'y': 'Vendor'},
            color=vendor_counts.values,
            color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # ================== TAB 5: HISTORY ==================
    with tabs[4]:
        st.header("📜 Alert History")
        
        if history_df.empty:
            st.info("No alert history available yet")
        else:
            # Time range filter
            col1, col2 = st.columns(2)
            
            with col1:
                days_back = st.selectbox(
                    "Time Range",
                    options=[1, 7, 30, 90],
                    index=1,
                    format_func=lambda x: f"Last {x} days"
                )
            
            # Filter by time range
            cutoff_date = datetime.now() - timedelta(days=days_back)
            recent_history = history_df[history_df['timestamp'] >= cutoff_date]
            
            # Alert trends
            st.subheader("📈 Alert Trends Over Time")
            
            # Group by date and priority
            recent_history['date'] = recent_history['timestamp'].dt.date
            daily_alerts = recent_history.groupby(['date', 'priority']).size().reset_index(name='count')
            
            fig = px.line(
                daily_alerts,
                x='date',
                y='count',
                color='priority',
                title=f"Alert Trends - Last {days_back} Days",
                labels={'date': 'Date', 'count': 'Number of Alerts'},
                color_discrete_map={
                    '🔴 CRITICAL': '#c62828',
                    '🟠 HIGH': '#ef6c00',
                    '🟡 MEDIUM': '#f9a825',
                    '🟢 LOW': '#43a047'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # History table
            st.subheader("📋 Recent Alerts")
            st.dataframe(
                recent_history[[
                    'timestamp', 'priority', 'type', 'vendor', 'message'
                ]].sort_values('timestamp', ascending=False).head(50),
                use_container_width=True,
                height=400
            )
    
    # Footer
    st.markdown("---")
    st.caption(f"🔔 Alert System | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption("💡 Tip: Run alerts regularly to stay on top of issues!")

if __name__ == "__main__":
    main()
