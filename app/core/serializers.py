from rest_framework import serializers
from .models import Article
from app.article.summariser import ArticleSummary


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'url', 'published_date', 'source']


class ArticleSummarySerializer(serializers.ModelSerializer):
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = ArticleSummary
        fields = ['id', 'article', 'summary_text', 'created_at']
        read_only_fields = ['id', 'created_at']
