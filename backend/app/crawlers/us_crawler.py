from app.crawlers.base_crawler import (
    BaseCrawler
)


class USCrawler(BaseCrawler):

    URL = (
        "https://www.whitehouse.gov/presidential-actions/"
    )

    LAW_ID = 3

    JURISDICTION_ID = 3

    LAW_NAME = "US AI Executive Order"