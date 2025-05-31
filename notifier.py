# notifier.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
from config import (
    EMAIL_SENDER,
    EMAIL_RECIPIENT,
    SMTP_SERVER,
    SMTP_PORT,
    EMAIL_PASSWORD
)

def send_email_notification(articles):
    """Send email notification with new articles"""
    if not articles:
        return

    # Create email content with current date and time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    subject = f"Today's News Summary [{current_time}]: {len(articles)} New Articles"
    
    # Create HTML content
    html_content = f"<h2>Latest News Articles - {current_time}</h2>"
    for article in articles:
        # Split the summary into parts if it contains a recommendation
        summary_parts = article.get('summary', '').split('\n')
        main_summary = summary_parts[0] if summary_parts else ''
        recommendation = summary_parts[1] if len(summary_parts) > 1 else ''

        html_content += f"""
        <div style="margin-bottom: 20px; padding: 15px; border: 1px solid #eee; border-radius: 5px;">
            <h3><a href=\"{article['url']}\" style="color: #2c3e50; text-decoration: none;">{article['title']}</a></h3>
            <p style="color: #7f8c8d; margin: 5px 0;">Source: {article['source']}</p>
            {f"<p style='color: #7f8c8d; margin: 5px 0;'>Published: {article['published_date']}</p>" if article.get('published_date') else ""}
            <div style="background-color: #f8f9fa; padding: 10px; border-radius: 3px; margin-top: 10px;">
                <p style="margin: 0;">{main_summary}</p>
                {f'<p style="margin: 5px 0;"><strong>Recommendation:</strong> <span style="color: #27ae60;">{recommendation.replace("Recommendation:", "").strip()}</span></p>' if recommendation else ''}
            </div>
        </div>
        """

    send_with_gmail(subject, html_content)

def send_with_gmail(subject, html_content):
    """Send email using Gmail SMTP"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECIPIENT

        msg.attach(MIMEText(html_content, 'html'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)  # Use App Password here
            server.send_message(msg)
        
        print("Email notification sent successfully via Gmail SMTP")
    except Exception as e:
        print(f"Error sending email via Gmail SMTP: {e}")