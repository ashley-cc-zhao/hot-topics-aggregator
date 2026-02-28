# 🔥 Tech Hot Topics Aggregator

An automated tool that aggregates hot topics from multiple sources (Reddit, Hacker News, YouTube, RSS feeds), analyzes them with Google Gemini AI, and publishes beautiful HTML reports to GitHub Pages.

## ✨ Features

- **Multi-Source Data Collection**
  - Reddit hot posts from tech/AI subreddits
  - Hacker News top stories
  - YouTube trending tech videos
  - RSS feeds from major tech news sites (The Verge, TechCrunch, etc.)

- **AI-Powered Analysis**
  - Uses Google Gemini to analyze trends
  - Generates executive summaries
  - Identifies top trending topics
  - Categorizes content automatically

- **Automated Updates**
  - Runs automatically every 12 hours via GitHub Actions
  - Deploys to GitHub Pages automatically
  - Zero maintenance required after setup

- **Beautiful Reports**
  - Responsive HTML design
  - Clean, modern UI
  - Easy to read and share

## 🚀 Quick Start

### Prerequisites

1. GitHub account (you'll use: **ashley-cc-zhao**)
2. Google Gemini API key (free tier available)
3. YouTube API key (optional, but recommended)

### Step 1: Get API Keys

#### Gemini API Key (Required)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

#### YouTube API Key (Optional)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "YouTube Data API v3"
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy the API key

### Step 2: Set Up GitHub Repository

1. **Create a new repository on GitHub**
   - Go to GitHub and sign in as **ashley-cc-zhao**
   - Click "New Repository"
   - Name: `hot-topics-aggregator`
   - Description: "Automated tech hot topics aggregator with AI analysis"
   - Public repository
   - DO NOT initialize with README (we already have one)
   - Click "Create repository"

2. **Push this code to GitHub**
   ```bash
   cd hot-topics-aggregator
   git init
   git add .
   git commit -m "Initial commit: Hot Topics Aggregator"
   git branch -M main
   git remote add origin https://github.com/ashley-cc-zhao/hot-topics-aggregator.git
   git push -u origin main
   ```

### Step 3: Configure GitHub Secrets

1. Go to your repository on GitHub
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Add the following secrets:

   **GEMINI_API_KEY** (Required)
   - Name: `GEMINI_API_KEY`
   - Value: Your Gemini API key from Step 1

   **YOUTUBE_API_KEY** (Optional)
   - Name: `YOUTUBE_API_KEY`
   - Value: Your YouTube API key from Step 1

### Step 4: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click "Settings" → "Pages"
3. Under "Source", select "Deploy from a branch"
4. Under "Branch", select `gh-pages` and `/ (root)`
5. Click "Save"

### Step 5: Run First Aggregation

1. Go to "Actions" tab in your repository
2. Click on "Aggregate Hot Topics" workflow
3. Click "Run workflow" → "Run workflow"
4. Wait for the workflow to complete (takes 2-5 minutes)

### Step 6: View Your Report

After the workflow completes successfully, your report will be available at:

**https://ashley-cc-zhao.github.io/hot-topics-aggregator/**

## 📅 Automatic Updates

The workflow runs automatically every 12 hours:
- 12:00 AM UTC (Daily midnight)
- 12:00 PM UTC (Daily noon)

You can also manually trigger it anytime from the Actions tab.

## 🛠️ Customization

### Change Data Sources

Edit the subreddit list in [src/main.py:42](src/main.py#L42):

```python
all_data['reddit'] = fetch_reddit_hot_posts(
    subreddits=['artificial', 'MachineLearning', 'technology', 'programming',
               'ChatGPT', 'LocalLLaMA', 'stablediffusion', 'singularity'],
    limit=15,
    min_score=50
)
```

### Change Update Frequency

Edit the cron schedule in [.github/workflows/aggregate.yml:6](.github/workflows/aggregate.yml#L6):

```yaml
schedule:
  - cron: '0 */12 * * *'  # Every 12 hours
  # - cron: '0 */6 * * *'   # Every 6 hours
  # - cron: '0 9 * * *'     # Daily at 9 AM UTC
```

### Modify RSS Feeds

Edit the feed URLs in [src/fetch_rss.py:13](src/fetch_rss.py#L13):

```python
feed_urls = {
    'The Verge AI': 'https://www.theverge.com/rss/ai-artificial-intelligence/index.xml',
    'TechCrunch AI': 'https://techcrunch.com/category/artificial-intelligence/feed/',
    # Add your own feeds here
}
```

## 📁 Project Structure

```
hot-topics-aggregator/
├── .github/
│   └── workflows/
│       └── aggregate.yml       # GitHub Actions workflow
├── src/
│   ├── main.py                # Main orchestration script
│   ├── fetch_reddit.py        # Reddit data fetcher
│   ├── fetch_hackernews.py    # Hacker News fetcher
│   ├── fetch_youtube.py       # YouTube fetcher
│   ├── fetch_rss.py           # RSS feed fetcher
│   ├── analyze_with_gemini.py # AI analysis
│   └── generate_html.py       # HTML report generator
├── data/                      # Generated data (auto-created)
├── index.html                 # Generated report (auto-created)
├── requirements.txt           # Python dependencies
├── .gitignore
└── README.md
```

## 🐛 Troubleshooting

### Workflow fails with "API key not found"
- Make sure you've added the API keys to GitHub Secrets (Step 3)
- Check the secret names are exactly: `GEMINI_API_KEY` and `YOUTUBE_API_KEY`

### GitHub Pages shows 404
- Make sure you've enabled GitHub Pages (Step 4)
- Check that the `gh-pages` branch exists
- Wait a few minutes after the first workflow run

### No YouTube videos appearing
- YouTube API key is optional - the tool works without it
- If you want YouTube data, make sure you've added `YOUTUBE_API_KEY` secret
- Check your YouTube API quota (free tier: 10,000 units/day)

### RSS feeds not updating
- Some RSS feeds may be temporarily unavailable
- Check the feed URLs are still valid
- The tool will continue working even if some feeds fail

## 🔧 Local Testing

To test locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY="your-key-here"
export YOUTUBE_API_KEY="your-key-here"  # optional

# Run the aggregator
cd src
python main.py

# Open the generated index.html in your browser
open ../index.html
```

## 📊 Data Sources

### Default Sources:
- **Reddit**: r/artificial, r/MachineLearning, r/technology, r/programming, r/ChatGPT, r/LocalLLaMA, r/stablediffusion, r/singularity
- **Hacker News**: Top 50 stories (filtered by score > 50)
- **YouTube**: Trending AI/tech videos from last 24 hours
- **RSS Feeds**: The Verge, TechCrunch, MIT Tech Review, Ars Technica, Wired

### Filtering Criteria:
- **Reddit**: Posts with 50+ upvotes from last 24 hours
- **Hacker News**: Stories with 50+ points from last 24 hours
- **YouTube**: Videos sorted by view count from last 24 hours
- **RSS**: Articles published in last 24 hours

## 🤖 AI Analysis

The Gemini AI analyzes all collected data to provide:
- Executive summary of main trends
- Top 5 trending topics
- Content categorization (AI/ML, Software, Hardware, Business, Other)

## 🌟 Credits

- Inspired by the n8n workflow from Xuan酱's tutorial
- Powered by Google Gemini AI
- Deployed with GitHub Actions & Pages

## 📝 License

MIT License - feel free to use and modify!

## 🙋‍♀️ Support

If you encounter any issues:
1. Check the "Actions" tab for workflow logs
2. Review the troubleshooting section above
3. Create an issue on GitHub

---

**Happy aggregating! 🚀**

Last updated: 2026-02-28
