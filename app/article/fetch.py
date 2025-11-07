import requests
from datetime import datetime
from django.conf import settings
from core.models import Article


def fetch_articles():
    """Fetch technology articles from NewsAPI"""
    print("fetching articles...")
    api_key = settings.NEWSAPI_KEY
    url = "https://newsapi.org/v2/top-headlines"

    params = {
        'sources': 'techcrunch',
        'apiKey': api_key,
        'pageSize': 100
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        articles_created = 0
        for article_data in data.get('articles', []):
            Article.objects.create(
                title=article_data.get('title', 'No title')[:200],
                content=(
                    article_data.get('content') or
                    article_data.get('description', '')
                ),
                url=article_data.get('url', ''),
                published_date=(
                    datetime.strptime(
                        article_data.get('publishedAt'), "%Y-%m-%dT%H:%M:%SZ"
                    ) or
                    datetime.now().date()
                ),
                source=(
                    article_data
                    .get('source', {})
                    .get('name', 'Unknown')
                )
            )
            articles_created += 1

        print(f"Successfully created {articles_created} articles")

    except Exception as e:
        print(f"Error fetching articles: {str(e)}")
