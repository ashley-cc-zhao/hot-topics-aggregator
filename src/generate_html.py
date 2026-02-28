"""
Generate HTML report from collected data
"""
from datetime import datetime
import json

def generate_html_report(all_data, analysis, output_file='index.html'):
    """
    Generate a beautiful HTML report

    Args:
        all_data: Dictionary with data from all sources
        analysis: Analysis results from Gemini
        output_file: Output HTML file path
    """
    # Get current timestamp
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tech Hot Topics - {timestamp}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .timestamp {{
            opacity: 0.9;
            font-size: 0.9em;
        }}

        .summary-section {{
            background: #f8f9fa;
            padding: 30px;
            border-bottom: 3px solid #667eea;
        }}

        .summary-section h2 {{
            color: #667eea;
            margin-bottom: 15px;
        }}

        .trends {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}

        .trend-tag {{
            background: white;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}

        .content-section {{
            padding: 30px;
        }}

        .source-group {{
            margin-bottom: 40px;
        }}

        .source-header {{
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e9ecef;
        }}

        .source-icon {{
            width: 40px;
            height: 40px;
            margin-right: 15px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
        }}

        .reddit-icon {{ background: #FF4500; }}
        .hn-icon {{ background: #FF6600; }}
        .youtube-icon {{ background: #FF0000; }}
        .rss-icon {{ background: #FFA500; }}

        .source-header h3 {{
            color: #333;
            font-size: 1.5em;
        }}

        .items-grid {{
            display: grid;
            gap: 15px;
        }}

        .item-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .item-card:hover {{
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}

        .item-title {{
            font-size: 1.2em;
            font-weight: 600;
            margin-bottom: 10px;
        }}

        .item-title a {{
            color: #333;
            text-decoration: none;
        }}

        .item-title a:hover {{
            color: #667eea;
        }}

        .item-meta {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            font-size: 0.9em;
            color: #666;
            margin-top: 10px;
        }}

        .meta-badge {{
            background: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: 500;
        }}

        .score {{ color: #FF4500; }}
        .views {{ color: #FF0000; }}
        .comments {{ color: #4CAF50; }}

        footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}

        .stat-box {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}

        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}

        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔥 Tech Hot Topics Aggregator</h1>
            <p class="timestamp">Last Updated: {timestamp}</p>
        </header>

        <div class="summary-section">
            <h2>📊 AI Analysis Summary</h2>
            <p>{analysis.get('summary', 'No analysis available')}</p>

            <h3 style="margin-top: 25px; color: #667eea;">🎯 Top Trending Topics</h3>
            <div class="trends">
"""

    # Add trending topics
    for trend in analysis.get('top_trends', [])[:5]:
        html_content += f'                <div class="trend-tag">🔹 {trend}</div>\n'

    html_content += """            </div>
        </div>

        <div class="summary-section">
            <div class="stats">
"""

    # Add statistics
    stats = [
        ('Reddit Posts', len(all_data.get('reddit', []))),
        ('HN Stories', len(all_data.get('hackernews', []))),
        ('YouTube Videos', len(all_data.get('youtube', []))),
        ('RSS Articles', len(all_data.get('rss', [])))
    ]

    for label, count in stats:
        html_content += f"""                <div class="stat-box">
                    <div class="stat-number">{count}</div>
                    <div class="stat-label">{label}</div>
                </div>
"""

    html_content += """            </div>
        </div>

        <div class="content-section">
"""

    # Add Reddit posts
    reddit_posts = all_data.get('reddit', [])
    if reddit_posts:
        html_content += generate_reddit_section(reddit_posts)

    # Add Hacker News stories
    hn_stories = all_data.get('hackernews', [])
    if hn_stories:
        html_content += generate_hn_section(hn_stories)

    # Add YouTube videos
    youtube_videos = all_data.get('youtube', [])
    if youtube_videos:
        html_content += generate_youtube_section(youtube_videos)

    # Add RSS articles
    rss_articles = all_data.get('rss', [])
    if rss_articles:
        html_content += generate_rss_section(rss_articles)

    html_content += """        </div>

        <footer>
            <p>🤖 Powered by GitHub Actions + Google Gemini AI</p>
            <p>Auto-updated every 12 hours</p>
        </footer>
    </div>
</body>
</html>
"""

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML report generated: {output_file}")

def generate_reddit_section(posts):
    """Generate HTML for Reddit section"""
    html = """            <div class="source-group">
                <div class="source-header">
                    <div class="source-icon reddit-icon">🔴</div>
                    <h3>Reddit Hot Posts</h3>
                </div>
                <div class="items-grid">
"""
    for post in posts[:20]:  # Top 20
        html += f"""                    <div class="item-card">
                        <div class="item-title">
                            <a href="{post['url']}" target="_blank">{post['title']}</a>
                        </div>
                        <div class="item-meta">
                            <span class="meta-badge">r/{post['subreddit']}</span>
                            <span class="meta-badge score">⬆ {post['score']} upvotes</span>
                            <span class="meta-badge comments">💬 {post['num_comments']} comments</span>
                        </div>
                    </div>
"""
    html += """                </div>
            </div>
"""
    return html

def generate_hn_section(stories):
    """Generate HTML for Hacker News section"""
    html = """            <div class="source-group">
                <div class="source-header">
                    <div class="source-icon hn-icon">Y</div>
                    <h3>Hacker News Top Stories</h3>
                </div>
                <div class="items-grid">
"""
    for story in stories[:20]:
        html += f"""                    <div class="item-card">
                        <div class="item-title">
                            <a href="{story['url']}" target="_blank">{story['title']}</a>
                        </div>
                        <div class="item-meta">
                            <span class="meta-badge score">▲ {story['score']} points</span>
                            <span class="meta-badge comments">💬 {story['num_comments']} comments</span>
                            <span class="meta-badge"><a href="{story['hn_url']}" target="_blank">HN Discussion</a></span>
                        </div>
                    </div>
"""
    html += """                </div>
            </div>
"""
    return html

def generate_youtube_section(videos):
    """Generate HTML for YouTube section"""
    html = """            <div class="source-group">
                <div class="source-header">
                    <div class="source-icon youtube-icon">▶</div>
                    <h3>YouTube Trending Videos</h3>
                </div>
                <div class="items-grid">
"""
    for video in videos[:15]:
        html += f"""                    <div class="item-card">
                        <div class="item-title">
                            <a href="{video['url']}" target="_blank">{video['title']}</a>
                        </div>
                        <div class="item-meta">
                            <span class="meta-badge">{video['channel']}</span>
                            <span class="meta-badge views">👁 {video['views']:,} views</span>
                            <span class="meta-badge score">👍 {video['likes']:,} likes</span>
                        </div>
                    </div>
"""
    html += """                </div>
            </div>
"""
    return html

def generate_rss_section(articles):
    """Generate HTML for RSS section"""
    html = """            <div class="source-group">
                <div class="source-header">
                    <div class="source-icon rss-icon">📰</div>
                    <h3>Tech News from RSS Feeds</h3>
                </div>
                <div class="items-grid">
"""
    for article in articles[:25]:
        html += f"""                    <div class="item-card">
                        <div class="item-title">
                            <a href="{article['url']}" target="_blank">{article['title']}</a>
                        </div>
                        <div class="item-meta">
                            <span class="meta-badge">{article['feed_name']}</span>
"""
        if article.get('author'):
            html += f"""                            <span class="meta-badge">✍ {article['author']}</span>
"""
        html += """                        </div>
                    </div>
"""
    html += """                </div>
            </div>
"""
    return html

if __name__ == '__main__':
    # Test with sample data
    sample_data = {
        'reddit': [],
        'hackernews': [],
        'youtube': [],
        'rss': []
    }
    sample_analysis = {
        'summary': 'Test summary',
        'top_trends': ['AI', 'ML', 'Cloud'],
        'categories': {}
    }
    generate_html_report(sample_data, sample_analysis, 'test_report.html')
