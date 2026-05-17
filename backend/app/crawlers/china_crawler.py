from app.crawlers.base_crawler import (
    BaseCrawler
)


class ChinaCrawler(BaseCrawler):

    URL = (
        "https://www.cac.gov.cn/"
    )

    LAW_ID = 5

    JURISDICTION_ID = 5

    LAW_NAME = "China AI Regulation"