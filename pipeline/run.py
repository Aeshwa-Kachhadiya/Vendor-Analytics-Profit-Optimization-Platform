"""
Easy Startup Script for Vendor Analytics Pipeline
"""

import sys
import subprocess
import time
from pathlib import Path

BANNER = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        📊 VENDOR ANALYTICS AUTOMATION SYSTEM 📊          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

MENU = """
Select an option:

1. 🚀 Run Pipeline Once (with archiving)
2. ⏰ Start Scheduled Pipeline (every 24 hours)
3. 👁️  Start File Watcher (auto-trigger on new files)
4. 📊 Launch Dashboard
5. 🔍 Validate Data Only
6. 📈 Run Pipeline + Launch Dashboard
7. 🔄 Full Auto Mode (Watcher + Dashboard)
8. ❌ Exit

Enter your choice (1-8): """

def run_command(cmd, wait=True):
    """Execute a command"""
    try:
        if wait:
            result = subprocess.run(cmd, shell=True, check=True)
            return result.returncode == 0
        else:
            subprocess.Popen(cmd, shell=True)
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return False

def check_requirements():
    """Check if required folders exist"""
    folders = ['data', 'logs', 'data/archive']
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
    print("✅ Required folders verified")

def main():
    print(BANNER)
    check_requirements()
    
    while True:
        choice = input(MENU).strip()
        
        if choice == '1':
            print("\n🚀 Running pipeline with archiving...")
            run_command("python pipeline.py --archive")
            print("\n✅ Pipeline completed!")
            time.sleep(2)
            
        elif choice == '2':
            print("\n⏰ Starting scheduled pipeline (every 24 hours)...")
            print("Press Ctrl+C to stop\n")
            run_command("python pipeline.py --schedule 24 --archive")
            
        elif choice == '3':
            print("\n👁️  Starting file watcher...")
            print("Add .xlsx files to 'data/' folder to trigger pipeline")
            print("Press Ctrl+C to stop\n")
            run_command("python watcher.py")
            
        elif choice == '4':
            print("\n📊 Launching dashboard...")
            print("Dashboard will open in your browser")
            print("Press Ctrl+C to stop\n")
            run_command("streamlit run dashboard.py")
            
        elif choice == '5':
            print("\n🔍 Validating data...")
            run_command("python pipeline.py --validate-only")
            print("\n✅ Validation completed!")
            time.sleep(2)
            
        elif choice == '6':
            print("\n📈 Running pipeline and launching dashboard...")
            if run_command("python pipeline.py --archive"):
                print("\n✅ Pipeline completed! Launching dashboard...\n")
                time.sleep(2)
                run_command("streamlit run dashboard.py")
            
        elif choice == '7':
            print("\n🔄 Starting Full Auto Mode...")
            print("File watcher and dashboard will run simultaneously")
            print("Press Ctrl+C to stop\n")
            
            # Start watcher in background
            run_command("python watcher.py", wait=False)
            time.sleep(2)
            
            # Start dashboard (blocking)
            run_command("streamlit run dashboard.py")
            
        elif choice == '8':
            print("\n👋 Goodbye!")
            sys.exit(0)
            
        else:
            print("\n❌ Invalid choice. Please enter 1-8.\n")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped by user. Goodbye!")
        sys.exit(0)
