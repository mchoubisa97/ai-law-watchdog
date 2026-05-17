from app.crawlers.base_crawler import (
    BaseCrawler
)


class NISTCrawler(BaseCrawler):

    URL = (
        "https://www.nist.gov/itl/ai-risk-management-framework"
    )

    LAW_ID = 4

    JURISDICTION_ID = 4

    LAW_NAME = "NIST AI RMF"