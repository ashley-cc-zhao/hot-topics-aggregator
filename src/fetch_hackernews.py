"""
Fetch top stories from Hacker News
"""
import requests
from datetime import datetime, timedelta

def fetch_hackernews_top_stories(limit=30, min_score=50):
    """
    Fetch top stories from Hacker News

    Args:
        limit: Number of stories to fetch
        min_score: Minimum points to include a story

    Returns:
        List of story dictionaries
    """
    stories = []
    base_url = 'https://hacker-news.firebaseio.com/v0'

    try:
        # Get top story IDs
        response = requests.get(f'{base_url}/topstories.json', timeout=10)
        response.raise_for_status()
        story_ids = response.json()[:limit]

        cutoff_time = datetime.utcnow() - timedelta(hours=24)

        for story_id in story_ids:
            try:
                # Fetch individual story
                story_response = requests.get(f'{base_url}/item/{story_id}.json', timeout=10)
                story_response.raise_for_status()
                story = story_response.json()

                if not story:
                    continue

                created_time = datetime.utcfromtimestamp(story.get('time', 0))
                score = story.get('score', 0)

                # Filter by score and time
                if score >= min_score and created_time >= cutoff_time:
                    stories.append({
                        'source': 'Hacker News',
                        'title': story.get('title', ''),
                        'url': story.get('url', f'https://news.ycombinator.com/item?id={story_id}'),
                        'score': score,
                        'num_comments': story.get('descendants', 0),
                        'created_at': created_time.isoformat(),
                        'author': story.get('by', ''),
                        'hn_url': f'https://news.ycombinator.com/item?id={story_id}'
                    })

            except Exception as e:
                print(f"Error fetching HN story {story_id}: {str(e)}")
                continue

    except Exception as e:
        print(f"Error fetching HN top stories: {str(e)}")

    # Sort by score descending
    stories.sort(key=lambda x: x['score'], reverse=True)
    return stories

if __name__ == '__main__':
    stories = fetch_hackernews_top_stories()
    print(f"Fetched {len(stories)} HN stories")
    for story in stories[:3]:
        print(f"  - {story['title']} ({story['score']} points)")
