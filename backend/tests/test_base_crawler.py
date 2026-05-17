from unittest.mock import MagicMock, patch
from app.crawlers.base_crawler import BaseCrawler


class DummyCrawler(BaseCrawler):
    URL = "https://example.com"
    LAW_ID = 1
    JURISDICTION_ID = 1
    LAW_NAME = "Test Law"


def test_has_changed_returns_true_when_hashes_differ():
    crawler = DummyCrawler()
    assert crawler.has_changed("abc123", "xyz789") is True


def test_has_changed_returns_false_when_hashes_same():
    crawler = DummyCrawler()
    assert crawler.has_changed("abc123", "abc123") is False


def test_generate_hash_is_consistent():
    crawler = DummyCrawler()
    text = "some regulatory content"
    assert crawler.generate_hash(text) == crawler.generate_hash(text)


def test_generate_hash_differs_for_different_content():
    crawler = DummyCrawler()
    assert crawler.generate_hash("content A") != crawler.generate_hash("content B")


@patch("app.crawlers.base_crawler.get_latest_snapshot", return_value=None)
@patch("app.crawlers.base_crawler.create_snapshot")
def test_first_snapshot_is_stored(mock_create_snapshot, mock_get_snapshot):
    crawler = DummyCrawler()
    db = MagicMock()
    page_data = {
        "url": "https://example.com",
        "hash": "abc123",
        "raw_content": "some content",
    }
    crawler.process_change_detection(db, page_data)
    mock_create_snapshot.assert_called_once()