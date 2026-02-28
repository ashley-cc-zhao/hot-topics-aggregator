"""
Analyze content using Google Gemini API
"""
import os
import google.generativeai as genai
import json

def analyze_topics_with_gemini(all_data, api_key=None):
    """
    Use Gemini to analyze and summarize hot topics

    Args:
        all_data: Dictionary with lists of items from different sources
        api_key: Gemini API key

    Returns:
        Dictionary with analysis results
    """
    if api_key is None:
        api_key = os.environ.get('GEMINI_API_KEY')

    if not api_key:
        print("Warning: No Gemini API key provided. Skipping AI analysis.")
        return {
            'summary': 'AI analysis not available - no API key provided',
            'top_trends': [],
            'categories': {}
        }

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        # Prepare data summary for analysis
        data_summary = prepare_data_summary(all_data)

        prompt = f"""
You are a tech news analyst. Analyze the following hot topics from various sources and provide:

1. A brief executive summary (2-3 sentences) of the main trends
2. Top 5 trending topics/themes
3. Categorize topics into: AI/ML, Software Development, Hardware, Business/Industry, Other

Here's the data:

{data_summary}

Respond in JSON format:
{{
  "summary": "Executive summary here...",
  "top_trends": ["Trend 1", "Trend 2", "Trend 3", "Trend 4", "Trend 5"],
  "categories": {{
    "AI/ML": ["topic1", "topic2"],
    "Software Development": ["topic1"],
    "Hardware": ["topic1"],
    "Business/Industry": ["topic1"],
    "Other": ["topic1"]
  }}
}}
"""

        response = model.generate_content(prompt)

        # Parse the JSON response
        response_text = response.text.strip()

        # Remove markdown code blocks if present
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '').replace('```', '').strip()
        elif response_text.startswith('```'):
            response_text = response_text.replace('```', '').strip()

        analysis = json.loads(response_text)
        return analysis

    except Exception as e:
        print(f"Error in Gemini analysis: {str(e)}")
        return {
            'summary': 'Analysis temporarily unavailable',
            'top_trends': [],
            'categories': {}
        }

def prepare_data_summary(all_data):
    """
    Prepare a concise summary of all data for the AI prompt
    """
    summary_parts = []

    # Reddit posts
    reddit_posts = all_data.get('reddit', [])
    if reddit_posts:
        summary_parts.append(f"\n### Reddit Hot Posts ({len(reddit_posts)} posts):")
        for post in reddit_posts[:10]:  # Top 10
            summary_parts.append(f"- [{post['subreddit']}] {post['title']} ({post['score']} upvotes)")

    # Hacker News
    hn_stories = all_data.get('hackernews', [])
    if hn_stories:
        summary_parts.append(f"\n### Hacker News ({len(hn_stories)} stories):")
        for story in hn_stories[:10]:
            summary_parts.append(f"- {story['title']} ({story['score']} points)")

    # YouTube
    youtube_videos = all_data.get('youtube', [])
    if youtube_videos:
        summary_parts.append(f"\n### YouTube Trending ({len(youtube_videos)} videos):")
        for video in youtube_videos[:10]:
            summary_parts.append(f"- {video['title']} ({video['views']:,} views)")

    # RSS Feeds
    rss_articles = all_data.get('rss', [])
    if rss_articles:
        summary_parts.append(f"\n### RSS News ({len(rss_articles)} articles):")
        for article in rss_articles[:15]:
            summary_parts.append(f"- [{article['feed_name']}] {article['title']}")

    return '\n'.join(summary_parts)

if __name__ == '__main__':
    # Test with sample data
    sample_data = {
        'reddit': [{'title': 'AI breakthrough', 'score': 1000, 'subreddit': 'artificial'}],
        'hackernews': [{'title': 'New ML framework', 'score': 500}]
    }
    analysis = analyze_topics_with_gemini(sample_data)
    print("Analysis:", json.dumps(analysis, indent=2))
