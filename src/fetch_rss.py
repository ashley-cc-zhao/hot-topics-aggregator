"""
Fetch articles from RSS feeds
"""
import feedparser
from datetime import datetime, timedelta
from dateutil import parser as date_parser

def fetch_rss_feeds(feed_urls=None, hours_back=24):
    """
    Fetch articles from RSS feeds

    Args:
        feed_urls: Dictionary of feed names and URLs
        hours_back: How many hours back to fetch articles

    Returns:
        List of article dictionaries
    """
    if feed_urls is None:
        feed_urls = {
            'The Verge AI': 'https://www.theverge.com/rss/ai-artificial-intelligence/index.xml',
            'TechCrunch AI': 'https://techcrunch.com/category/artificial-intelligence/feed/',
            'MIT Technology Review': 'https://www.technologyreview.com/feed/',
            'Ars Technica': 'https://feeds.arstechnica.com/arstechnica/technology-lab',
            'Wired AI': 'https://www.wired.com/feed/tag/ai/latest/rss'
        }

    articles = []
    cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)

    for feed_name, feed_url in feed_urls.items():
        try:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries:
                try:
                    # Parse published date
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published_date = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'published'):
                        published_date = date_parser.parse(entry.published)
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        published_date = datetime(*entry.updated_parsed[:6])
                    else:
                        # Skip if no date available
                        continue

                    # Filter by time
                    if published_date < cutoff_time:
                        continue

                    # Extract summary/description
                    summary = ''
                    if hasattr(entry, 'summary'):
                        summary = entry.summary
                    elif hasattr(entry, 'description'):
                        summary = entry.description

                    # Clean HTML from summary
                    from bs4 import BeautifulSoup
                    if summary:
                        summary = BeautifulSoup(summary, 'html.parser').get_text()[:500]

                    articles.append({
                        'source': 'RSS Feed',
                        'feed_name': feed_name,
                        'title': entry.get('title', ''),
                        'url': entry.get('link', ''),
                        'published_at': published_date.isoformat(),
                        'summary': summary,
                        'author': entry.get('author', '')
                    })

                except Exception as e:
                    print(f"Error parsing entry from {feed_name}: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error fetching RSS feed {feed_name}: {str(e)}")
            continue

    # Sort by published date descending
    articles.sort(key=lambda x: x['published_at'], reverse=True)
    return articles

if __name__ == '__main__':
    articles = fetch_rss_feeds()
    print(f"Fetched {len(articles)} RSS articles")
    for article in articles[:3]:
        print(f"  - [{article['feed_name']}] {article['title']}")
