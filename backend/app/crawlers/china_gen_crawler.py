from app.crawlers.base_crawler import (
    BaseCrawler
)


class ChinaGenCrawler(BaseCrawler):

    URL = (
        "https://english.www.gov.cn/news/202307/13/content_WS64aff5b3c6d0868f4e8ddc01.html"
    )

    LAW_ID = 6

    JURISDICTION_ID = 6

    LAW_NAME = "China Generative AI Measures"