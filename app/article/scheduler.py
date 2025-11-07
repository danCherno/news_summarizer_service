from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from article.fetch import fetch_articles


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        fetch_articles,
        trigger=IntervalTrigger(hours=6),
        id='fetch_articles_job',
        name='Fetch articles every 6 hours',
        replace_existing=True
    )
    scheduler.start()
