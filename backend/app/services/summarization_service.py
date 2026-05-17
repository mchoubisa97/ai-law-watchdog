import os
from google import genai
from app.core.logger import logger

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def summarize_legal_change(law_name: str, diff: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=(
                f"You are a legal analyst specializing in AI regulation.\n\n"
                f"The following diff shows what changed on the official page for: {law_name}\n\n"
                f"DIFF:\n{diff[:3000]}\n\n"
                f"In 2-3 sentences, summarize what changed in plain English. "
                f"Focus on regulatory impact. If the change seems trivial or non-legal, say so."
            ),
        )
        return response.text

    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        return "Summary unavailable."