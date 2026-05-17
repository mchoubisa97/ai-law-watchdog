from threading import Lock
from app.core.logger import logger
from app.crawlers.registry import CRAWLER_REGISTRY

crawler_lock = Lock()


def run_all_crawlers():
    if not crawler_lock.acquire(blocking=False):
        logger.warning("Crawler cycle already running — skipping.")
        return

    try:
        logger.info(f"Starting crawler cycle — {len(CRAWLER_REGISTRY)} crawlers registered.")

        for crawler_class in CRAWLER_REGISTRY:
            crawler_name = crawler_class.__name__
            try:
                logger.info(f"Running {crawler_name}...")
                crawler_class().run()
                logger.info(f"{crawler_name} completed.")
            except Exception as e:
                logger.exception(f"{crawler_name} failed: {e}")

        logger.info("Crawler cycle completed.")

    finally:
        crawler_lock.release()
