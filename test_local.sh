#!/bin/bash
# Quick test script to verify the setup locally

echo "🔍 Testing Hot Topics Aggregator locally..."
echo "============================================"

# Check Python version
echo ""
echo "1️⃣  Checking Python version..."
python3 --version

# Check if required modules can be imported
echo ""
echo "2️⃣  Checking dependencies..."
python3 -c "
import sys
try:
    import requests
    import feedparser
    import google.generativeai
    from bs4 import BeautifulSoup
    print('✅ All dependencies installed!')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    print('Run: pip install -r requirements.txt')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "3️⃣  Running a quick fetch test..."
    echo ""

    cd src

    # Test Reddit fetch
    echo "Testing Reddit..."
    python3 -c "from fetch_reddit import fetch_reddit_hot_posts; posts = fetch_reddit_hot_posts(subreddits=['technology'], limit=5, min_score=10); print(f'✅ Fetched {len(posts)} posts')"

    # Test Hacker News fetch
    echo "Testing Hacker News..."
    python3 -c "from fetch_hackernews import fetch_hackernews_top_stories; stories = fetch_hackernews_top_stories(limit=10, min_score=10); print(f'✅ Fetched {len(stories)} stories')"

    # Test RSS fetch
    echo "Testing RSS feeds..."
    python3 -c "from fetch_rss import fetch_rss_feeds; articles = fetch_rss_feeds(hours_back=48); print(f'✅ Fetched {len(articles)} articles')"

    echo ""
    echo "============================================"
    echo "✨ All tests passed!"
    echo ""
    echo "To run the full aggregator:"
    echo "  cd src && python3 main.py"
    echo ""
    echo "Make sure to set environment variables:"
    echo "  export GEMINI_API_KEY='your-key'"
    echo "  export YOUTUBE_API_KEY='your-key'  # optional"
else
    echo "❌ Tests failed. Please install dependencies first."
fi
