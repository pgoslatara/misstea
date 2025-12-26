import asyncio
import logging
from typing import Any

import nest_asyncio
import newspaper
import requests
import trafilatura

from misstea.sub_agents.web_scraper.tools_async import scrape_generic_webpage_to_json

logger = logging.getLogger(__name__)

nest_asyncio.apply()


def fetch_web_page_contents(url: str) -> dict[str, str | dict[str, Any] | None] | None:
    """Fetch detailed content of a web page given its URL.

    Args:
        url (str): The URL of the web page to fetch.

    Returns:
        Union[None, str]: The detailed content of the web page, or None if unable to fetch.

    Raises:
        ValueError: If unable to decode JSON from LLM output.

    """
    logger.debug(f"Fetching content from {url}...")
    try:
        content = trafilatura.extract(trafilatura.fetch_url(url))
        if not content:
            try:
                article = newspaper.Article(url, language="en")
                article.download()
                article.parse()
                content = article.text
                if not content:
                    raise ValueError("No content found using newspaper3k.")
                return {"status": "success", "content": content}
            except Exception:
                response = requests.get(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                    },
                    timeout=10,
                )
                content = response.text
                if not content:
                    try:
                        content = asyncio.run(scrape_generic_webpage_to_json(url))
                        return {"status": "success", "content": content}
                    except Exception as e:
                        logger.warning(
                            f"Error fetching content from {url} using LLM: {e}"
                        )
                else:
                    return {"status": "success", "content": content}
        else:
            return {"status": "success", "content": content}
    except Exception as e:
        logger.warning(f"Error fetching content from {url}: {e}")
        logger.warning(f"Unable to fetch content for {url}.")
        return {"status": "success", "content": None}
