from apscheduler.schedulers.background import BackgroundScheduler
from app.crawlers.crawler_manager import run_all_crawlers
from app.core.logger import logger

scheduler = BackgroundScheduler()


def start_scheduler():

    scheduler.add_job(
        run_all_crawlers,
        "interval",
        hours=6,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=3600
    )

    scheduler.start()

    logger.info("Scheduler started.")