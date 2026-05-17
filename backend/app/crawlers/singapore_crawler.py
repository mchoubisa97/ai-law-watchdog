from app.crawlers.base_crawler import (
    BaseCrawler
)


class SingaporeCrawler(BaseCrawler):

    URL = (
        "https://www.imda.gov.sg/resources/press-releases-factsheets-and-speeches/factsheets/2020/model-ai-governance-framework"
    )

    LAW_ID = 8

    JURISDICTION_ID = 8

    LAW_NAME = "Singapore AI Governance Framework"