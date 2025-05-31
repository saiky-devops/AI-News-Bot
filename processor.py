# processor.py
import requests
from bs4 import BeautifulSoup
import openai
from config import OPENAI_API_KEY
import time

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

def fetch_article_content(url):
    """Fetch the content of an article from its URL"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup.select('script, style, nav, footer, header, aside, .ads, .comments, .sidebar'):
            element.decompose()
        
        # Get the main content
        content = ''
        paragraphs = soup.select('p')
        if not paragraphs:
            print(f"Warning: No paragraph content found in article at {url}")
            # Try alternative content extraction
            content = soup.get_text().strip()
            if not content:
                print(f"Error: No content found in article at {url}")
                return None
        
        for p in paragraphs:
            content += p.get_text().strip() + ' '
        
        if not content.strip():
            print(f"Error: Empty content extracted from article at {url}")
            return None
            
      #  print(f"Successfully extracted {len(content)} characters of content")
        return content[:5000]  # Limit to first 5000 chars to save on API costs
        
    except requests.exceptions.RequestException as e:
        print(f"Network error fetching article content from {url}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error fetching article content from {url}: {e}")
        return None

def summarize_article(title, content):
    """Summarize article using OpenAI API"""
    if not content:
        print(f"Error: Cannot summarize article '{title}' - no content provided")
        return "Error: No content available for summarization"
        
    try:
       # print(f"Generating summary for article: {title}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": """You are a helpful assistant that summarizes technical articles about DevOps and AI. 
                    For each article, provide the output in exactly this format:
                    
                    [Main summary in 1-2 sentences]
                    Recommendation: [Either 'Worth Exploring' if the article contains actionable insights, new technologies, or important trends; or 'FYI' if it's general information or updates]"""
                },
                {
                    "role": "user", 
                    "content": f"""Please analyze this article and provide a summary with recommendation:
                    Title: {title}
                    
                    Content: {content}"""
                }
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        summary = response.choices[0].message.content.strip()
        if not summary:
            print(f"Warning: Empty summary generated for article: {title}")
            return "Error: Empty summary generated"
            
        print(f"Successfully generated summary for article: {title}")
        return summary
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error summarizing article '{title}': {e}")
        return f"Error: OpenAI API error - {str(e)}"
    except Exception as e:
        print(f"Unexpected error summarizing article '{title}': {e}")
        return f"Error: Unexpected error - {str(e)}"

def process_new_articles(articles, limit=10):
    """Process and return new articles"""
    # Sort articles by published date if available
    sorted_articles = sorted(
        articles,
        key=lambda x: x.get('published_date', ''),
        reverse=True
    )
    return sorted_articles[:limit]

def summarize_articles(articles):
    """Summarize articles using AI"""
    summarized = []
    total_articles = len(articles)
    print(f"\nStarting to process {total_articles} articles...")
    
    for i, article in enumerate(articles, 1):
       # print(f"\nProcessing article {i}/{total_articles}: {article.get('title', '')} - URL: {article.get('url', '')}")
        
        try:
            # Fetch article content
            content = fetch_article_content(article.get('url', ''))
            if not content:
                print(f"❌ Skipped: Could not fetch content for article: {article.get('title', '')}")
                continue
            
            # Generate AI summary
            summary = summarize_article(article.get('title', ''), content)
            
            # Robust summary extraction
            summary_lines = [line.strip() for line in summary.split('\n') if line.strip()]
            rec_idx = -1
            for idx, line in enumerate(summary_lines):
                if 'recommendation:' in line.lower():
                    rec_idx = idx
                    break
            if rec_idx == -1:
                print(f"❌ Skipped: No recommendation found for article: {article.get('title', '')}")
                print(f"Summary received: {summary}")
                continue
            
            # Main summary: join all lines before the recommendation
            main_summary = ' '.join(summary_lines[:rec_idx]).strip()
            
            # Clean up main summary - remove various prefixes and brackets
            prefixes_to_remove = [
                '[Main summary in 1-2 sentences]',
                '[Main summary:]',
                '[Summary]',
                'Main summary in 1-2 sentences',
                'Main summary:',
                'Summary:'
            ]
            for prefix in prefixes_to_remove:
                if main_summary.lower().startswith(prefix.lower()):
                    main_summary = main_summary[len(prefix):].strip()
            
            # Remove any remaining brackets and their contents
            main_summary = main_summary.replace('[', '').replace(']', '').strip()
            
            # Recommendation: first line containing 'Recommendation:'
            recommendation = summary_lines[rec_idx]
            # Clean up recommendation
            recommendation = recommendation[recommendation.lower().find('recommendation:'):].strip()
            recommendation = recommendation.replace('[Recommendation:', 'Recommendation:').replace('[', '').replace(']', '').strip()
            
            if not main_summary or not recommendation.lower().startswith('recommendation:'):
                print(f"❌ Skipped: Missing main summary or recommendation for article: {article.get('title', '')}")
               # print(f"Summary received: {summary}")
                continue
            
            summarized.append({
                'title': article.get('title', ''),
                'url': article.get('url', ''),
                'source': article.get('source', ''),
                'published_date': article.get('published_date', ''),
                'summary': f"{main_summary}\n{recommendation}"
            })
            
            print(f"✅ Successfully processed article: {article.get('title', '')}")
          #  print(f"Summary: {main_summary}\n{recommendation}")
            print("---")
            
        except Exception as e:
            print(f"❌ Error processing article {article.get('title', '')}: {str(e)}")
            continue
    
    print(f"\nProcessing complete. Successfully processed {len(summarized)} out of {total_articles} articles.")
    return summarized