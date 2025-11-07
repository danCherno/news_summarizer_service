from django.test import TestCase
from datetime import date
from core.models import Article


class ModelTests(TestCase):
    def test_create_article_successful(self):
        context = {
            "title": "an article",
            "content": """
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                Quisque nec convallis turpis.
                Quisque sollicitudin quam nunc, eget eleifend erat euismod vel.
            """,
            "url": "example.com",
            "published_date": date(2025, 1, 1),
            "source": "Dr. John Doe"
        }

        article = Article.objects.create(**context)

        self.assertIsNotNone(article)
        self.assertIsNotNone(article.id)
        self.assertEqual(article.title, "an article")
        self.assertIn("Lorem ipsum", article.content)
        self.assertEqual(article.url, "example.com")
        self.assertEqual(article.published_date, date(2025, 1, 1))
        self.assertEqual(article.source, "Dr. John Doe")
