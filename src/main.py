#!/usr/bin/env python3
"""
Main script to orchestrate the hot topics aggregation
"""
import os
import sys
import json
from datetime import datetime

# Import our custom modules
from fetch_reddit import fetch_reddit_hot_posts
from fetch_hackernews import fetch_hackernews_top_stories
from fetch_youtube import fetch_youtube_trending
from fetch_rss import fetch_rss_feeds
from analyze_with_gemini import analyze_topics_with_gemini
from generate_html import generate_html_report

def main():
    """
    Main execution flow
    """
    print("=" * 60)
    print("🔥 Hot Topics Aggregator")
    print("=" * 60)
    print(f"Started at: {datetime.utcnow().isoformat()} UTC\n")

    # Initialize data storage
    all_data = {
        'reddit': [],
        'hackernews': [],
        'youtube': [],
        'rss': []
    }

    # Fetch from all sources
    print("📥 Fetching data from sources...")
    print("-" * 60)

    # 1. Fetch Reddit posts
    print("1️⃣  Fetching Reddit hot posts...")
    try:
        all_data['reddit'] = fetch_reddit_hot_posts(
            subreddits=['artificial', 'MachineLearning', 'technology', 'programming',
                       'ChatGPT', 'LocalLLaMA', 'stablediffusion', 'singularity'],
            limit=15,
            min_score=50
        )
        print(f"   ✅ Fetched {len(all_data['reddit'])} Reddit posts")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # 2. Fetch Hacker News stories
    print("2️⃣  Fetching Hacker News stories...")
    try:
        all_data['hackernews'] = fetch_hackernews_top_stories(
            limit=50,
            min_score=50
        )
        print(f"   ✅ Fetched {len(all_data['hackernews'])} HN stories")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # 3. Fetch YouTube videos
    print("3️⃣  Fetching YouTube trending videos...")
    try:
        all_data['youtube'] = fetch_youtube_trending(
            max_results=20,
            query='AI OR "artificial intelligence" OR "machine learning" OR technology OR programming'
        )
        print(f"   ✅ Fetched {len(all_data['youtube'])} YouTube videos")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # 4. Fetch RSS feeds
    print("4️⃣  Fetching RSS feeds...")
    try:
        all_data['rss'] = fetch_rss_feeds(
            hours_back=24
        )
        print(f"   ✅ Fetched {len(all_data['rss'])} RSS articles")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Calculate totals
    total_items = sum(len(items) for items in all_data.values())
    print(f"\n📊 Total items collected: {total_items}")
    print("-" * 60)

    # Save raw data to JSON
    print("\n💾 Saving raw data...")
    try:
        # Create data directory in parent (root) if it doesn't exist
        os.makedirs('../data', exist_ok=True)
        with open('../data/latest_data.json', 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.utcnow().isoformat(),
                'data': all_data
            }, f, indent=2, ensure_ascii=False)
        print("   ✅ Raw data saved to ../data/latest_data.json")
    except Exception as e:
        print(f"   ⚠️  Could not save raw data: {str(e)}")

    # Analyze with Gemini
    print("\n🤖 Analyzing with Gemini AI...")
    try:
        analysis = analyze_topics_with_gemini(all_data)
        print("   ✅ AI analysis completed")
        print(f"   📝 Summary: {analysis.get('summary', 'N/A')[:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        analysis = {
            'summary': 'AI analysis failed',
            'top_trends': [],
            'categories': {}
        }

    # Generate HTML report
    print("\n📄 Generating HTML report...")
    try:
        # Output to parent directory (root) for GitHub Pages
        output_file = '../index.html'
        generate_html_report(all_data, analysis, output_file)
        print(f"   ✅ HTML report generated: {output_file}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("✨ All done!")
    print(f"Completed at: {datetime.utcnow().isoformat()} UTC")
    print("=" * 60)

if __name__ == '__main__':
    # Create data directory in parent (root) if it doesn't exist
    os.makedirs('../data', exist_ok=True)

    # Run main function
    main()
