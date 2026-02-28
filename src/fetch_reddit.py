"""
Fetch hot posts from Reddit
"""
import requests
from datetime import datetime, timedelta

def fetch_reddit_hot_posts(subreddits=None, limit=10, min_score=50):
    """
    Fetch hot posts from specified subreddits

    Args:
        subreddits: List of subreddit names (without r/)
        limit: Number of posts to fetch per subreddit
        min_score: Minimum upvotes to include a post

    Returns:
        List of post dictionaries
    """
    if subreddits is None:
        # Default subreddits focused on tech and AI
        subreddits = ['artificial', 'machinelearning', 'technology', 'programming', 'ChatGPT']

    all_posts = []
    headers = {'User-Agent': 'HotTopicsAggregator/1.0'}

    for subreddit in subreddits:
        try:
            url = f'https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}'
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            posts = data.get('data', {}).get('children', [])

            # Filter by score and within 24 hours
            cutoff_time = datetime.utcnow() - timedelta(hours=24)

            for post_data in posts:
                post = post_data.get('data', {})
                created_utc = datetime.utcfromtimestamp(post.get('created_utc', 0))
                score = post.get('score', 0)

                if score >= min_score and created_utc >= cutoff_time:
                    all_posts.append({
                        'source': 'Reddit',
                        'subreddit': subreddit,
                        'title': post.get('title', ''),
                        'url': f"https://reddit.com{post.get('permalink', '')}",
                        'score': score,
                        'num_comments': post.get('num_comments', 0),
                        'created_at': created_utc.isoformat(),
                        'author': post.get('author', ''),
                        'selftext': post.get('selftext', '')[:500]  # First 500 chars
                    })

        except Exception as e:
            print(f"Error fetching from r/{subreddit}: {str(e)}")
            continue

    # Sort by score descending
    all_posts.sort(key=lambda x: x['score'], reverse=True)
    return all_posts

if __name__ == '__main__':
    posts = fetch_reddit_hot_posts()
    print(f"Fetched {len(posts)} Reddit posts")
    for post in posts[:3]:
        print(f"  - {post['title']} ({post['score']} upvotes)")
