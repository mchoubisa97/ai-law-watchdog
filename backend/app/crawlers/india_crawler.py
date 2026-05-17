from app.crawlers.base_crawler import (
    BaseCrawler
)


class IndiaCrawler(BaseCrawler):

    URL = (
        "https://www.meity.gov.in/"
    )

    LAW_ID = 9

    JURISDICTION_ID = 9

    LAW_NAME = "India AI Governance"    