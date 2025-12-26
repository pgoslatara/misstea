import json
import logging
import os
from typing import Any

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

from misstea.constants import AGENT_MODEL

logger = logging.getLogger(__name__)


async def scrape_generic_webpage_to_json(url: str) -> dict[str, Any] | None:
    """Scrapes a generic webpage using an LLM to extract its main content into a JSON object based on broad instructions.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        dict: A dictionary representing the JSON object with the main content.

    Raises:
        ValueError: If unable to decode JSON from LLM output.

    """
    logger.info(f"Scraping webpage: {url}")
    api_token = os.environ["GOOGLE_API_KEY"]
    llm_config = LLMConfig(provider=AGENT_MODEL, api_token=api_token)
    extraction_strategy = LLMExtractionStrategy(
        llm_config=llm_config,
        instruction="""
            Extract the comprehensive and detailed content of the entire webpage.
            Identify and include all major headings, paragraphs, lists, URL references, images URLs and key information.
            Structure the output as a single JSON object with a key named 'main_content'
            whose value is a string containing all the extracted textual content.
            Do not include navigation, footers, sidebars, or advertisements.
            Ensure the output is valid JSON.
        """,
        extraction_type="free_form",
    )
    config = CrawlerRunConfig(extraction_strategy=extraction_strategy)
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=config)
        if result.success:
            try:
                parsed_json = json.loads(result.extracted_content)
                logger.info(f"Webpage {url} scraped and parsed successfully.")
                return parsed_json
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Error decoding JSON from LLM output: {e}\nRaw LLM output:\n{result.extracted_content}"
                ) from e
        else:
            if result.error_details:
                logger.warning(f"Details: {result.error_details}")
