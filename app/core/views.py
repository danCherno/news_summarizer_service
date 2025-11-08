from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import Article
from .serializers import ArticleSerializer


class ArticlePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all().order_by('-published_date')
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
