import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.logger import logger


def send_alert(law_name: str, summary: str, source_url: str, event_date) -> None:
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    alert_email = os.getenv("ALERT_EMAIL")

    if not all([smtp_host, smtp_user, smtp_password, alert_email]):
        logger.warning("Email notifications not configured — skipping.")
        return

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🚨 AI Law Change Detected: {law_name}"
        msg["From"] = smtp_user
        msg["To"] = alert_email

        body = f"""
AI Law Watchdog detected a regulatory change.

Law: {law_name}
Date: {event_date}
Source: {source_url}

Summary:
{summary}

---
AI Law Watchdog
        """.strip()

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, alert_email, msg.as_string())

        logger.info(f"Alert email sent for {law_name}.")

    except Exception as e:
        logger.error(f"Failed to send alert email: {e}")