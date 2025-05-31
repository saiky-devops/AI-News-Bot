# scraper.py
import requests
from bs4 import BeautifulSoup
import datetime
from urllib.parse import urljoin
import time
import random
from config import NEWS_SOURCES

def scrape_source(source):
    """Scrape a single news source"""
    print(f"\n=== Scraping {source['name']} from {source['url']} ===")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
       # print(f"Making request to {source['url']}...")
        response = requests.get(source['url'], headers=headers, timeout=10)
        response.raise_for_status()
       # print(f"Response status: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        
        # Site-specific selectors
        selectors = {
            'DevOps.com': {
                'articles': '.post, .article, .post-item, .pt-cv-title',  # Added .pt-cv-title for card articles
                'title': '.entry-title, .article-title, .post-title, a',  # For .pt-cv-title, the <a> is the title
                'link': '.entry-title a, .article-title a, .post-title a, a',  # For .pt-cv-title, the <a> is the link
                'date': '.entry-date, .article-date, .post-date'  # Date is still in .entry-date
            },
            'The New Stack': {
                'articles': 'a[data-context][data-url]',  # Articles are links with data-context and data-url
                'title': '',  # Title is in aria-label attribute
                'link': '',  # URL is in data-url attribute
                'date': ''  # No date available on the homepage
            },
            'AI News': {
                'articles': 'article',
                'title': 'h2.entry-title',
                'link': 'h2.entry-title a',
                'date': '.entry-date'
            }
        }
        
        # Get site-specific selectors or use defaults
        site_selectors = selectors.get(source['name'], {
            'articles': 'article, .post, .article, .entry',
            'title': 'h1, h2, h3, .title, .heading',
            'link': 'a',
            'date': '.date, time, .published, .post-date'
        })
        
        # Extract articles using site-specific selectors
        article_elements = soup.select(site_selectors['articles'])
        print(f"Found {len(article_elements)} potential article elements")
        
        
        for i, article in enumerate(article_elements[:10], 1):  # Limit to first 10 articles
           # print(f"\nProcessing article {i}:")
            
            # Extract title and link using site-specific selectors
            if source['name'] == 'The New Stack':
                title = article.get('aria-label', '').strip()
                url = article.get('data-url', '')
            elif source['name'] == 'DevOps.com':
                title = ''
                url = ''
                if site_selectors['title']:
                    title_element = article.select_one(site_selectors['title'])
                    title = title_element.get_text().strip() if title_element else ''
                if site_selectors['link']:
                    link_element = article.select_one(site_selectors['link'])
                    url = link_element.get('href') if link_element else ''
                else:
                    url = article.get('href', '')
                if not title:
                    print("[DevOps.com] Could not find title element")
                if not url:
                    print("[DevOps.com] Could not find link element")
                # For .pt-cv-title, the date is not a child, so look for the closest .entry-date in the parent or next siblings
                published_date = None
                if 'pt-cv-title' in article.get('class', []):
                    # Try to find .entry-date in parent or next siblings
                    parent = article.parent
                    date_element = parent.select_one('.entry-date') if parent else None
                    if not date_element:
                        # Try next siblings
                        next_sibling = article.find_next_sibling()
                        while next_sibling and not date_element:
                            date_element = next_sibling.select_one('.entry-date') if next_sibling else None
                            next_sibling = next_sibling.find_next_sibling() if next_sibling else None
                    if date_element:
                        published_date = date_element.get_text().strip()
                       # print(f"Published date: {published_date}")
                else:
                    if site_selectors['date']:
                        date_element = article.select_one(site_selectors['date'])
                        if date_element:
                            published_date = date_element.get_text().strip()
                          #  print(f"Published date: {published_date}")
            else:
                title_element = article.select_one(site_selectors['title']) if site_selectors['title'] else None
                link_element = article.select_one(site_selectors['link']) if site_selectors['link'] else article
                title = title_element.get_text().strip() if title_element else ''
                url = link_element.get('href') if link_element else ''
            
          #  print(f"Title: {title}")
          #  print(f"URL: {url}")
            
            # Handle relative URLs
            if url and not url.startswith(('http://', 'https://')):
                url = urljoin(source['url'], url)
                print(f"Converted to absolute URL: {url}")
            
            if title and url:
                articles.append({
                    'title': title,
                    'url': url,
                    'source': source['name'],
                    'published_date': published_date if 'published_date' in locals() else None
                })
            else:
                print("Could not find title or link elements")
        
        print(f"\n=== Completed scraping {source['name']} ===")
      #  print(f"Found {len(articles)} articles")
        return articles
        
    except Exception as e:
        print(f"Error scraping {source['name']}: {str(e)}")
        return []

def run_scraper():
    """Run the scraper for all configured sources"""
    print("\n=== Starting scraper ===")
    all_articles = []
    
    for source in NEWS_SOURCES:
        articles = scrape_source(source)
        all_articles.extend(articles)
        
        # Be nice to servers with a random delay
        delay = random.uniform(2, 5)
        print(f"Waiting {delay:.1f} seconds before next source...")
        time.sleep(delay)
    
    print(f"\n=== Scraping completed ===")
    print(f"Total new articles found: {len(all_articles)}")
    return all_articles