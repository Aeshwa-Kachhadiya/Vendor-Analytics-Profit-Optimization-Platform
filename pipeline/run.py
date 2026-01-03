"""
Easy Startup Script for Vendor Analytics Pipeline
Now with Predictive Analytics!
"""

import sys
import subprocess
import time
from pathlib import Path
import os

# Get the absolute paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

BANNER = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║    🤖 AI-POWERED VENDOR ANALYTICS SYSTEM 🤖             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

MENU = """
Select an option:

DATA PIPELINE:
1.  🚀 Run Data Pipeline (load & transform data)
2.  ⏰ Start Scheduled Pipeline (every 24 hours)
3.  👁️  Start File Watcher (auto-trigger on new files)

PREDICTIVE ANALYTICS:
4.  🤖 Run AI Analytics (ML predictions & insights)
5.  🎯 Performance Scoring Only
6.  📈 Demand Forecasting Only

DASHBOARDS:
7.  📊 Launch Basic Dashboard
8.  🤖 Launch AI-Powered Dashboard

COMBINED:
9.  🔄 Full Pipeline + Analytics + Dashboard
10. ⚡ Quick Start (Pipeline → Analytics → AI Dashboard)

UTILITIES:
11. 🔍 Validate Data Only
12. ❌ Exit

Enter your choice (1-12): """

def run_command(cmd, wait=True, cwd=None):
    """Execute a command"""
    try:
        if wait:
            result = subprocess.run(cmd, shell=True, check=True, cwd=cwd)
            return result.returncode == 0
        else:
            subprocess.Popen(cmd, shell=True, cwd=cwd)
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return False

def check_requirements():
    """Check if required folders exist"""
    folders = [
        PROJECT_ROOT / 'data',
        PROJECT_ROOT / 'logs',
        PROJECT_ROOT / 'data' / 'archive'
    ]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
    print("✅ Required folders verified")
    print(f"📂 Working directory: {PROJECT_ROOT}")

def main():
    print(BANNER)
    check_requirements()
    
    # Get script paths
    pipeline_script = SCRIPT_DIR / 'pipeline.py'
    watcher_script = SCRIPT_DIR / 'watcher.py'
    analytics_script = SCRIPT_DIR / 'analytics.py'
    dashboard_script = PROJECT_ROOT / 'dashboard.py'
    dashboard_ai_script = PROJECT_ROOT / 'dashboard_analytics.py'
    
    while True:
        choice = input(MENU).strip()
        
        if choice == '1':
            print("\n🚀 Running data pipeline...")
            run_command(f'python "{pipeline_script}" --archive', cwd=PROJECT_ROOT)
            print("\n✅ Pipeline completed!")
            time.sleep(2)
            
        elif choice == '2':
            print("\n⏰ Starting scheduled pipeline (every 24 hours)...")
            print("Press Ctrl+C to stop\n")
            run_command(f'python "{pipeline_script}" --schedule 24 --archive', cwd=PROJECT_ROOT)
            
        elif choice == '3':
            print("\n👁️  Starting file watcher...")
            print("Add .xlsx files to 'data/' folder to trigger pipeline")
            print("Press Ctrl+C to stop\n")
            run_command(f'python "{watcher_script}"', cwd=PROJECT_ROOT)
            
        elif choice == '4':
            print("\n🤖 Running AI analytics...")
            run_command(f'python "{analytics_script}"', cwd=PROJECT_ROOT)
            print("\n✅ Analytics completed!")
            time.sleep(2)
            
        elif choice == '5':
            print("\n🎯 Calculating performance scores...")
            run_command(f'python "{analytics_script}" --scores-only', cwd=PROJECT_ROOT)
            print("\n✅ Scoring completed!")
            time.sleep(2)
            
        elif choice == '6':
            print("\n📈 Running demand forecasting...")
            run_command(f'python "{analytics_script}" --forecast-only', cwd=PROJECT_ROOT)
            print("\n✅ Forecasting completed!")
            time.sleep(2)
            
        elif choice == '7':
            print("\n📊 Launching basic dashboard...")
            print("Dashboard will open in your browser")
            print("Press Ctrl+C to stop\n")
            run_command(f'streamlit run "{dashboard_script}"', cwd=PROJECT_ROOT)
            
        elif choice == '8':
            print("\n🤖 Launching AI-powered dashboard...")
            print("Dashboard will open in your browser")
            print("Press Ctrl+C to stop\n")
            run_command(f'streamlit run "{dashboard_ai_script}"', cwd=PROJECT_ROOT)
            
        elif choice == '9':
            print("\n🔄 Running full pipeline...")
            print("\nStep 1/3: Data Pipeline")
            if run_command(f'python "{pipeline_script}" --archive', cwd=PROJECT_ROOT):
                print("\nStep 2/3: AI Analytics")
                if run_command(f'python "{analytics_script}"', cwd=PROJECT_ROOT):
                    print("\nStep 3/3: Launching AI Dashboard")
                    time.sleep(2)
                    run_command(f'streamlit run "{dashboard_ai_script}"', cwd=PROJECT_ROOT)
            
        elif choice == '10':
            print("\n⚡ Quick Start Mode...")
            print("\n📥 Loading data...")
            if run_command(f'python "{pipeline_script}" --archive', cwd=PROJECT_ROOT):
                print("\n🤖 Running analytics...")
                if run_command(f'python "{analytics_script}"', cwd=PROJECT_ROOT):
                    print("\n🚀 Launching dashboard...\n")
                    time.sleep(2)
                    run_command(f'streamlit run "{dashboard_ai_script}"', cwd=PROJECT_ROOT)
            
        elif choice == '11':
            print("\n🔍 Validating data...")
            run_command(f'python "{pipeline_script}" --validate-only', cwd=PROJECT_ROOT)
            print("\n✅ Validation completed!")
            time.sleep(2)
            
        elif choice == '12':
            print("\n👋 Goodbye!")
            sys.exit(0)
            
        else:
            print("\n❌ Invalid choice. Please enter 1-12.\n")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped by user. Goodbye!")
        sys.exit(0)
