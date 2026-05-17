from app.crawlers.base_crawler import (
    BaseCrawler
)


class ChinaGenCrawler(BaseCrawler):

    URL = (
        "https://www.cac.gov.cn/2023-04/11/c_1682854275475410.htm"
    )

    LAW_ID = 6

    JURISDICTION_ID = 6

    LAW_NAME = "China Generative AI Measures"