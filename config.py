# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# API Credentials
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Email Configuration
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")


# Gmail Configuration (only needed if USE_SENDGRID is False)
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Use App Password for Gmail
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

# SendGrid Configuration (only needed if USE_SENDGRID is True)
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

# Sources to scrape
NEWS_SOURCES = [
    {"name": "DevOps.com", "url": "https://devops.com/category/blogs/"},
    {"name": "The New Stack", "url": "https://thenewstack.io/"},
    {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/"},
]


# Update frequency (in hours)
UPDATE_FREQUENCY = 12