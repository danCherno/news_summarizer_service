from django.db import models  # noqa


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    url = models.URLField()
    published_date = models.DateField()
    source = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.title


class ArticleSummary(models.Model):
    article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        related_name='summary'
    )
    summary_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Article Summaries"

    def __str__(self) -> str:
        return f"Summary for: {self.article.title}"
