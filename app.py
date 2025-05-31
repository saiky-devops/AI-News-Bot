# app.py
import datetime
from scraper import run_scraper
from processor import summarize_articles
from notifier import send_email_notification

def run_news_update():
    print(f"\n--- Starting news update: {datetime.datetime.now().isoformat()} ---")
    
    # Step 1: Scrape news sources
    print("Step 1: Scraping news sources...")
    articles = run_scraper()
    
    # Step 2: Summarize articles
    print("\nStep 2: Summarizing articles...")
    summarized_articles = summarize_articles(articles)
    
    # Step 3: Send notifications
    if summarized_articles:
        print(f"\nStep 3: Sending notification with {len(summarized_articles)} articles...")
        send_email_notification(summarized_articles)
    else:
        print("\nNo articles to send notification for.")
    
    print(f"--- News update completed: {datetime.datetime.now().isoformat()} ---\n")

if __name__ == "__main__":
    run_news_update()