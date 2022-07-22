from django.db import models


class naver_news(models.Model):
    NEWS_TITLE = models.CharField(max_length=150)
    NEWS_URL = models.URLField(unique=True)
    def __str__(self):
        return self.NEWS_TITLE
# Create your models here.
