from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, Mock
from datetime import date
from core.models import Article, ArticleSummary


class ArticleSummaryTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Authenticate the client
        self.client.force_authenticate(user=self.user)

        self.article = Article.objects.create(
            title='Test AI Article',
            content='This is a test article about AI technology.',
            url='https://example.com/ai-article',
            published_date=date(2025, 1, 1),
            source='Tech News'
        )

    @patch('article.summariser.OpenAI')
    def test_create_summary_on_first_request(self, mock_openai):
        # Mock OpenAI response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [
            Mock(message=Mock(content='This is a test summary.'))
        ]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        url = reverse('article-summary', kwargs={'article_id': self.article.id})  # noqa: E501
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('summary_text', response.data)
        self.assertEqual(
            response.data['summary_text'],
            'This is a test summary.'
        )

        # Verify summary was created in database
        self.assertEqual(ArticleSummary.objects.count(), 1)
        summary = ArticleSummary.objects.first()
        self.assertEqual(summary.article, self.article)

    def test_return_existing_summary(self):
        # Create existing summary
        ArticleSummary.objects.create(
            article=self.article,
            summary_text='Existing summary text'
        )

        url = reverse('article-summary', kwargs={'article_id': self.article.id})  # noqa: E501
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['summary_text'],
            'Existing summary text'
        )

        # Verify only one summary exists
        self.assertEqual(ArticleSummary.objects.count(), 1)

    def test_summary_nonexistent_article(self):
        url = reverse('article-summary', kwargs={'article_id': 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('article.summariser.OpenAI')
    def test_summary_api_error(self, mock_openai):
        # Mock OpenAI error
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception('API Error')  # noqa: E501
        mock_openai.return_value = mock_client

        url = reverse('article-summary', kwargs={'article_id': self.article.id})  # noqa: E501
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.assertIn('error', response.data)

    def test_unauthenticated_user_denied(self):
        # Create unauthenticated client
        unauthenticated_client = APIClient()

        url = reverse('article-summary', kwargs={'article_id': self.article.id})  # noqa: E501
        response = unauthenticated_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
