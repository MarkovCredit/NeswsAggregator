# Generated by Django 3.2.6 on 2022-07-22 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsaggapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.URLField(default='../static/imgs/news.jpg'),
        ),
    ]
