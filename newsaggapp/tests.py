# Create your tests here.
from django.test import TestCase
from django.utils import timezone
from .models import Article
from django.urls.base import reverse
from datetime import datetime


class ArticleTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            news_publisher="Python News 4 U",
            title="My Awesome News Article",
            description="Behold, the Article!",
            pub_date=timezone.now(),
            link="https://myawesomeshow.com",
            # image="https://image.myawesomeshow.com",
            guid="de194720-7b4c-49e2-a05f-432436d3fetr",
        )

    def test_article_content(self):
        self.assertEqual(self.article.description, "Behold, the Article!")
        self.assertEqual(self.article.link, "https://myawesomeshow.com")
        self.assertEqual(
            self.article.guid, "de194720-7b4c-49e2-a05f-432436d3fetr"
        )

    def test_article_str_representation(self):
        self.assertEqual(
            str(self.article), "Python News 4 U: My Awesome News Article"
        )

    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse("homepage"))
        self.assertTemplateUsed(response, "homepage.html")

    def test_homepage_list_contents(self):
        response = self.client.get(reverse("homepage"))
        self.assertContains(response, "My Awesome News Article")