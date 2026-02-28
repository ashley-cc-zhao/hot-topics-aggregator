"""
Fetch trending videos from YouTube
"""
import requests
import os
from datetime import datetime, timedelta

def fetch_youtube_trending(api_key=None, max_results=20, query='AI OR artificial intelligence OR technology'):
    """
    Fetch trending YouTube videos

    Args:
        api_key: YouTube Data API v3 key
        max_results: Number of videos to fetch
        query: Search query for videos

    Returns:
        List of video dictionaries
    """
    if api_key is None:
        api_key = os.environ.get('YOUTUBE_API_KEY')

    if not api_key:
        print("Warning: No YouTube API key provided. Skipping YouTube fetch.")
        return []

    videos = []
    base_url = 'https://www.googleapis.com/youtube/v3'

    try:
        # Calculate time range (last 24 hours)
        published_after = (datetime.utcnow() - timedelta(hours=24)).isoformat() + 'Z'

        # Search for videos
        search_params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'order': 'viewCount',
            'publishedAfter': published_after,
            'maxResults': max_results,
            'key': api_key
        }

        response = requests.get(f'{base_url}/search', params=search_params, timeout=10)
        response.raise_for_status()
        search_data = response.json()

        video_ids = [item['id']['videoId'] for item in search_data.get('items', [])]

        if not video_ids:
            return []

        # Get video statistics
        stats_params = {
            'part': 'statistics,snippet',
            'id': ','.join(video_ids),
            'key': api_key
        }

        stats_response = requests.get(f'{base_url}/videos', params=stats_params, timeout=10)
        stats_response.raise_for_status()
        stats_data = stats_response.json()

        for item in stats_data.get('items', []):
            snippet = item.get('snippet', {})
            stats = item.get('statistics', {})

            videos.append({
                'source': 'YouTube',
                'title': snippet.get('title', ''),
                'url': f"https://www.youtube.com/watch?v={item['id']}",
                'channel': snippet.get('channelTitle', ''),
                'views': int(stats.get('viewCount', 0)),
                'likes': int(stats.get('likeCount', 0)),
                'comments': int(stats.get('commentCount', 0)),
                'published_at': snippet.get('publishedAt', ''),
                'description': snippet.get('description', '')[:300],
                'thumbnail': snippet.get('thumbnails', {}).get('medium', {}).get('url', '')
            })

    except Exception as e:
        print(f"Error fetching YouTube videos: {str(e)}")

    # Sort by views descending
    videos.sort(key=lambda x: x['views'], reverse=True)
    return videos

if __name__ == '__main__':
    videos = fetch_youtube_trending()
    print(f"Fetched {len(videos)} YouTube videos")
    for video in videos[:3]:
        print(f"  - {video['title']} ({video['views']:,} views)")
