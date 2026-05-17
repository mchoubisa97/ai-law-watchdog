from app.crawlers.base_crawler import (
    BaseCrawler
)


class EUCrawler(BaseCrawler):

    URL = (
        "https://artificialintelligenceact.eu/"
    )

    LAW_ID = 1

    JURISDICTION_ID = 1

    LAW_NAME = "EU AI Act"