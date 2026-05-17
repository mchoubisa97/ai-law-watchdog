import hashlib
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from datetime import date, datetime
from bs4 import BeautifulSoup

from app.core.logger import logger
from app.db.database import SessionLocal

from app.services.notification_service import send_alert
from app.services.summarization_service import summarize_legal_change
from app.services.snapshot_service import get_latest_snapshot, create_snapshot
from app.services.law_event_service import create_law_event
from app.services.diff_service import generate_diff, is_meaningful_change
from app.services.crawler_run_service import create_crawler_run


class BaseCrawler:

    URL = None
    LAW_ID = None
    JURISDICTION_ID = None
    LAW_NAME = "Unknown Law"
    EVENT_TYPE = "Regulatory Update Detected"

    # ----------------------------
    # SESSION
    # ----------------------------

    def create_session(self):
        session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    # ----------------------------
    # CORE UTILITIES
    # ----------------------------

    def generate_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def fetch_page(self):
        session = self.create_session()
        response = session.get(self.URL, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # Remove noise elements
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
            tag.decompose()

        title = soup.title.get_text(strip=True) if soup.title else "No Title"

        clean_text = "\n".join(
            line.strip()
            for line in soup.get_text(separator="\n").splitlines()
            if line.strip()
        )

        content_hash = self.generate_hash(clean_text)

        return {
            "url": self.URL,
            "title": title,
            "hash": content_hash,
            "raw_content": clean_text,
        }

    # ----------------------------
    # PIPELINE HELPERS
    # ----------------------------

    def has_changed(self, previous_hash: str, current_hash: str) -> bool:
        return previous_hash != current_hash

    def is_meaningful(self, old_content: str, new_content: str) -> bool:
        return is_meaningful_change(old_content, new_content)

    def build_diff(self, old_content: str, new_content: str) -> str:
        return generate_diff(old_content, new_content)

    # ----------------------------
    # MAIN PIPELINE
    # ----------------------------

    def process_change_detection(self, db, page_data: dict):
        latest_snapshot = get_latest_snapshot(db, page_data["url"])

        # CASE 1: First time snapshot
        if latest_snapshot is None:
            logger.info(f"[{self.LAW_NAME}] First snapshot — storing baseline.")
            create_snapshot(
                db=db,
                law_id=self.LAW_ID,
                jurisdiction_id=self.JURISDICTION_ID,
                source_url=page_data["url"],
                content_hash=page_data["hash"],
                raw_content=page_data["raw_content"],
            )
            return

        # STEP 1: Hash check
        if not self.has_changed(latest_snapshot.content_hash, page_data["hash"]):
            logger.info(f"[{self.LAW_NAME}] No changes detected.")
            return

        logger.warning(f"[{self.LAW_NAME}] CHANGE DETECTED!")

        # STEP 2: Meaningful filter
        if not self.is_meaningful(latest_snapshot.raw_content, page_data["raw_content"]):
            logger.info(f"[{self.LAW_NAME}] Ignoring minor/non-meaningful change.")
            return

        # STEP 3: Diff generation
        diff_result = self.build_diff(latest_snapshot.raw_content, page_data["raw_content"])

        # STEP 4: Event creation
        summary = summarize_legal_change(self.LAW_NAME, diff_result)

        create_law_event(
            db=db,
            law_id=self.LAW_ID,
            event_type=self.EVENT_TYPE,
            description=(
                f"SUMMARY:\n{summary}\n\n"
                f"DIFF:\n{diff_result[:5000]}"
            ),
            source_url=page_data["url"],
            event_date=date.today(),
        )

        send_alert(
            law_name=self.LAW_NAME,
            summary=summary,
            source_url=page_data["url"],
            event_date=date.today(),
        )

        # STEP 5: Snapshot update
        create_snapshot(
            db=db,
            law_id=self.LAW_ID,
            jurisdiction_id=self.JURISDICTION_ID,
            source_url=page_data["url"],
            content_hash=page_data["hash"],
            raw_content=page_data["raw_content"],
        )

        logger.info(f"[{self.LAW_NAME}] New snapshot saved.")

    # ----------------------------
    # RUNNER (with full CrawlerRun tracking)
    # ----------------------------

    def run(self):
        if not self.URL:
            raise ValueError(f"[{self.LAW_NAME}] Crawler URL not configured.")

        db = SessionLocal()
        started_at = datetime.utcnow()

        try:
            logger.info(f"[{self.LAW_NAME}] Crawler started.")
            page_data = self.fetch_page()
            self.process_change_detection(db, page_data)

            finished_at = datetime.utcnow()
            duration = (finished_at - started_at).total_seconds()

            create_crawler_run(
                db=db,
                crawler_name=self.__class__.__name__,
                status="success",
                message=f"Completed in {duration:.1f}s",
                started_at=started_at,
                finished_at=finished_at,
            )

            logger.info(f"[{self.LAW_NAME}] Completed in {duration:.1f}s")

        except Exception as e:
            finished_at = datetime.utcnow()
            create_crawler_run(
                db=db,
                crawler_name=self.__class__.__name__,
                status="failed",
                message=str(e),
                started_at=started_at,
                finished_at=finished_at,
            )
            logger.error(f"[{self.LAW_NAME}] Error: {e}")

        finally:
            db.close()
