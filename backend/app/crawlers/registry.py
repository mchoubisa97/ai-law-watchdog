from app.crawlers.eu_crawler import EUCrawler
from app.crawlers.uk_crawler import UKCrawler
from app.crawlers.us_crawler import USCrawler
from app.crawlers.nist_crawler import NISTCrawler
from app.crawlers.china_crawler import ChinaCrawler
from app.crawlers.china_gen_crawler import ChinaGenCrawler
from app.crawlers.canada_crawler import CanadaCrawler
from app.crawlers.singapore_crawler import SingaporeCrawler
from app.crawlers.india_crawler import IndiaCrawler

CRAWLER_REGISTRY = [
    EUCrawler,
    UKCrawler,
    USCrawler,
    NISTCrawler,
    ChinaCrawler,
    ChinaGenCrawler,
    CanadaCrawler,
    SingaporeCrawler,
    IndiaCrawler,
]