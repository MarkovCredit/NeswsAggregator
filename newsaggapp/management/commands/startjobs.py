#standard libraries
import logging 

#Django
from django.conf import settings
from django.core.management.base import BaseCommand

#Third party 
import feedparser
import re
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

#Models
from newsaggapp.models import Article

logger = logging.getLogger(__name__)

def parse_desc(desc):
    # sometimes the description is an html object so we need to find the tag and parse it
        parsed_desc = re.findall('(?<=<p>)(.*)(?=</p>)',desc)
        return parsed_desc[0] if parsed_desc else desc 

def save_new_articles(feed):
    """Saves new articles to the database.

    Checks the article GUID against the articles currently stored in the
    database. If not found, then a new `Article` is added to the database.

    Args:
        feed: requires a feedparser object
    """
    article_title = feed.channel.title
    try:
        article_image = feed.channel.image["href"]
    except:
        article_image = '' 

    for item in feed.entries:
        if not Article.objects.filter(guid=item.guid).exists():
            article = Article(
                news_publisher = article_title,
                title=item.title,
                description=parse_desc(item.description),                
                pub_date=parser.parse(item.published),
                link=item.link,
                image=article_image,
                # article_name=article_title,
                guid=item.guid
            )
            article.save()

def fetch_bitcoin_articles():
    """Fetches new articles from RSS for bitcoin."""
    _feed = feedparser.parse("https://cointelegraph.com/rss/tag/bitcoin")
    save_new_articles(_feed)
    return 'Saved the article'

def fetch_fox_articles():
    """Fetches new articles from RSS for Fox News."""
    _feed = feedparser.parse("https://moxie.foxnews.com/feedburner/latest.xml")
    save_new_articles(_feed)
    return 'Saved the article'
    

def fetch_hackernews_articles():
    """Fetches new articles from RSS for Hacker News."""
    _feed = feedparser.parse("https://feeds.feedburner.com/TheHackersNews")
    save_new_articles(_feed)
    return 'Saved the article'
    
    # 

def delete_old_job_executions(max_age=604_800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)




class Command(BaseCommand):
    
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
        fetch_bitcoin_articles,
        trigger="interval",
        minutes=60,
        id="Bitcoin_Articles_CoinTelegraph",
        max_instances=1,
        replace_existing=True,
                    )
        logger.info("Added job: Bitcoin_Articles_CoinTelegraph")

        scheduler.add_job(
        fetch_fox_articles,
        trigger="interval",
        minutes=2,
        id="FoxNews_Articles",
        max_instances=1,
        replace_existing=True,
                    )


        scheduler.add_job(
        fetch_hackernews_articles,
        trigger="interval",
        minutes=2,
        id="HackerNews_Articles",
        max_instances=1,
        replace_existing=True,
                    )
        logger.info("Added job: Hacker News Articles")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

        