from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Article
from .serializers import ArticleSerializer, ArticleSummarySerializer
from app.article.summariser import SummaryService


class ArticlePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ArticleListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Article.objects.all().order_by('-published_date')
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination


class ArticleDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'pk'


class ArticleSummaryView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ArticleSummarySerializer

    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)

        summary_service = SummaryService()

        try:
            summary = summary_service.get_or_create_summary(article)
            serializer = self.get_serializer(summary)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
