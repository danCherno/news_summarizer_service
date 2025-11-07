from django.db import models  # noqa


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    url = models.URLField()
    published_date = models.DateField()
    source = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title