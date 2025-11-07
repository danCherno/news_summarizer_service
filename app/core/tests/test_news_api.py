from django.test import TestCase, override_settings
from unittest.mock import patch, Mock
from article.fetch import fetch_articles
from core.models import Article


@override_settings(NEWSAPI_KEY='test_key')
@patch('article.fetch.requests.get')
class NewsAPITaskTests(TestCase):

    def _setup_mock_and_fetch(self, mock_get):
        self.mock_data = {
            'status': 'ok',
            'articles': [
                {
                    "source": {"id": "techcrunch", "name": "TechCrunch"},
                    "author": "John Doe",
                    "title": "AI Title",
                    "description": "AI article desc.",
                    "url": "https://example.com/article",
                    "urlToImage": "https://exampleImage.com/img.jpg",
                    "publishedAt": "2024-05-08T13:02:12Z",
                    "content": "AI article Content"
                }
            ]
        }

        mock_response = Mock()
        mock_response.json.return_value = self.mock_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        fetch_articles()

    def test_correct_api_called(self, mock_get):
        self._setup_mock_and_fetch(mock_get)

        mock_get.assert_called_once()
        call_args = mock_get.call_args
        self.assertIn('sources', call_args[1]['params'])
        self.assertEqual(
            call_args[1]['params']['sources'],
            'techcrunch'
        )

    def test_article_created(self, mock_get):
        self._setup_mock_and_fetch(mock_get)

        self.assertEqual(Article.objects.count(), 1)
        article = Article.objects.first()
        self.assertEqual(article.title, 'AI Title')
        self.assertEqual(article.source, 'TechCrunch')
