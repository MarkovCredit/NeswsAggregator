from django.db import models

# Create your models here.
from django.db import models

class Article(models.Model):
    news_publisher = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField(default = "static/imgs/news.jpg")
    guid = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.news_publisher}: {self.title}"