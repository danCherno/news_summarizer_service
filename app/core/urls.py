from django.urls import path
from .views import ArticleListView, ArticleSummaryView

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path(
        'articles/<int:article_id>/summary/',
        ArticleSummaryView.as_view(),
        name='article-summary'
    ),
]
