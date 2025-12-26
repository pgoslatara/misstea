import asyncio
import logging
from typing import Any

import nest_asyncio

from misstea.sub_agents.web_scraper.tools_async import scrape_generic_webpage_to_json

logger = logging.getLogger(__name__)

nest_asyncio.apply()


def fetch_web_page_contents(url: str) -> dict[str, str | dict[str, Any] | None] | None:
    """Fetch detailed content of a web page given its URL.

    Args:
        url (str): The URL of the web page to fetch.

    Returns:
        Union[None, str]: The detailed content of the web page, or None if unable to fetch.

    """
    logger.info(f"Fetching content from {url}...")
    try:
        content = asyncio.run(scrape_generic_webpage_to_json(url))
        return {"status": "success", "content": content}
    except Exception as e:
        logger.warning(f"Error fetching content from {url} using LLM: {e}")
        return {"status": "success", "content": None}
