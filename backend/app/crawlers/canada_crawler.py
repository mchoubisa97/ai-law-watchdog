from app.crawlers.base_crawler import (
    BaseCrawler
)


class CanadaCrawler(BaseCrawler):

    URL = (
        "https://ised-isde.canada.ca/site/innovation-better-canada/en/artificial-intelligence-and-data-act-aida-companion-document"
    )

    LAW_ID = 7

    JURISDICTION_ID = 7

    LAW_NAME = "Canada AIDA"