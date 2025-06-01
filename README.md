# AI News Bot

An automated news aggregator and summarizer that collects articles from various tech news sources, generates AI-powered summaries, and delivers them via email notifications.

## Features

- 🔍 Automated web scraping from multiple tech news sources
- 🤖 AI-powered article summarization using OpenAI's GPT-3.5
- 📧 Email notifications with formatted article summaries
- ⏰ Configurable update frequency
- 📊 Article recommendations (Worth Exploring/FYI)

## Supported News Sources

- DevOps.com
- The New Stack
- VentureBeat AI

## Prerequisites

- Python 3.7+
- OpenAI API key
- Gmail account (for sending notifications)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI-News-Bot.git
cd AI-News-Bot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the following variables:
```env
OPENAI_API_KEY=your_openai_api_key
EMAIL_SENDER=your_gmail_address
EMAIL_RECIPIENT=recipient_email_address
EMAIL_PASSWORD=your_gmail_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

Note: For Gmail, you'll need to use an App Password. You can generate one in your Google Account settings under Security > 2-Step Verification > App passwords.

## Usage

Run the news bot:
```bash
python app.py
```

The bot will:
1. Scrape articles from configured news sources
2. Generate AI summaries for each article
3. Send an email notification with the formatted summaries


## Project Structure

- `app.py`: Main application entry point
- `config.py`: Configuration settings
- `scraper.py`: Web scraping functionality
- `processor.py`: Article processing and summarization
- `notifier.py`: Email notification system
