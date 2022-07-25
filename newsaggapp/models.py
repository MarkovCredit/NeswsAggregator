from django.db import models

# Create your models here.
from django.db import models

class Article(models.Model):
    news_publisher = models.TextField()
    title = models.TextField()
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField(default = "static/imgs/news.jpg")
    guid = models.TextField()

    def __str__(self) -> str:
        return f"{self.news_publisher}: {self.title}"