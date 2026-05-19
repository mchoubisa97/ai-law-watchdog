from app.crawlers.base_crawler import (
    BaseCrawler
)


class ChinaCrawler(BaseCrawler):

    URL = (
        "https://www.whitecase.com/insight-our-thinking/ai-watch-global-regulatory-tracker-china"
    )

    LAW_ID = 5

    JURISDICTION_ID = 5

    LAW_NAME = "China AI Regulation"