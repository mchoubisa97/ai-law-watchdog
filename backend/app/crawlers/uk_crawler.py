from app.crawlers.base_crawler import (
    BaseCrawler
)


class UKCrawler(BaseCrawler):

    URL = (
        "https://www.gov.uk/government/publications/a-pro-innovation-approach-to-ai-regulation"
    )

    LAW_ID = 2

    JURISDICTION_ID = 2

    LAW_NAME = "UK AI Regulation"