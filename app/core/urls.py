from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleSummaryView

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),  # noqa: E501
    path(
        'articles/<int:article_id>/summary/',
        ArticleSummaryView.as_view(),
        name='article-summary'
    ),
]
