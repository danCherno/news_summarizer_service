from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date
from core.models import Article


class ArticleAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test articles
        for i in range(15):
            Article.objects.create(
                title=f'Article {i}',
                content=f'Content {i}',
                url=f'https://example.com/article{i}',
                published_date=date(2025, 1, i + 1),
                source='Test Source'
            )

    def test_get_articles_list(self):
        url = reverse('article-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertEqual(len(response.data['results']), 10)
        self.assertEqual(response.data['count'], 15)

    def test_get_articles_pagination(self):
        url = reverse('article-list')
        response = self.client.get(url, {'page': 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)

    def test_get_articles_custom_page_size(self):
        url = reverse('article-list')
        response = self.client.get(url, {'page_size': 5})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)

    def test_articles_ordered_by_date(self):
        url = reverse('article-list')
        response = self.client.get(url)

        first_article = response.data['results'][0]
        self.assertEqual(first_article['title'], 'Article 14')

    def test_get_article_detail(self):
        article = Article.objects.first()
        url = reverse('article-detail', kwargs={'pk': article.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], article.id)
        self.assertEqual(response.data['title'], article.title)
        self.assertEqual(response.data['content'], article.content)
        self.assertEqual(response.data['url'], article.url)
        self.assertEqual(response.data['source'], article.source)

    def test_get_article_detail_not_found(self):
        url = reverse('article-detail', kwargs={'pk': 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
