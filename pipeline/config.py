"""
Pipeline Configuration Settings
"""

from pathlib import Path

# Paths - adjusted for pipeline subfolder
BASE_DIR = Path(__file__).parent.parent  # Go up one level from pipeline/
DATA_FOLDER = BASE_DIR / 'data'
ARCHIVE_FOLDER = DATA_FOLDER / 'archive'
LOG_FOLDER = BASE_DIR / 'logs'
DB_PATH = BASE_DIR / 'inventory.db'

# Database
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Pipeline Settings
PIPELINE_SCHEDULE_HOURS = 24  # Run every 24 hours
FILE_WATCH_COOLDOWN = 30  # Seconds to wait before re-triggering

# Data Validation
MIN_RECORDS_THRESHOLD = 10  # Minimum records per table
ALLOWED_FILE_EXTENSIONS = ['.xlsx', '.xls']

# Email Notifications (optional - configure if needed)
ENABLE_EMAIL_ALERTS = False
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your-email@gmail.com'
SENDER_PASSWORD = 'your-app-password'
RECIPIENT_EMAIL = 'recipient@example.com'

# Create required directories
DATA_FOLDER.mkdir(exist_ok=True)
ARCHIVE_FOLDER.mkdir(exist_ok=True)
LOG_FOLDER.mkdir(exist_ok=True)
