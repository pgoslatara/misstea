import datetime
import logging
import os
from io import BytesIO
from typing import Dict

from google import genai
from google.adk.agents import Agent
from google.genai.types import GenerateContentConfig, Modality
from PIL import Image  # ty: ignore[unresolved-import]

from misstea.constants import AGENT_MODEL

logger = logging.getLogger(__name__)


def generate_image(prompt: str) -> Dict[str, str]:
    """Generate an image based on a prompt and save it directly without external image processing packages.

    Args:
        prompt (str): The text description for the image to be generated.

    Returns:
        Dict: Status of the image generation and location of the output file.

    """
    extensions = ["jpeg", "png"]
    output_filename = f"{os.environ['IMAGE_GENERATION_DIR']}/generated_image_{datetime.datetime.now(datetime.timezone.utc).timestamp()}"
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=(prompt),
        config=GenerateContentConfig(
            response_modalities=[Modality.IMAGE],
        ),
    )
    for part in response.candidates[  # ty: ignore[not-iterable, non-subscriptable, possibly-missing-attribute]
        0
    ].content.parts:
        if part.inline_data:
            image = Image.open(BytesIO((part.inline_data.data)))  # ty: ignore[invalid-argument-type]
            for ext in extensions:
                image.save(f"{output_filename}.{ext}")

    logger.info(f"Image saved to {output_filename} ({', '.join(extensions)}).")
    return {"status": "success", "report": f"Saved to {output_filename}"}


def get_image_generator_agent() -> Agent:
    """Return an Image Generator agent.

    Returns:
        Agent: The Image Generator agent.

    """
    return Agent(
        model=AGENT_MODEL,
        name="image_generator_agent",
        instruction=""""
            Generate an image.
        """,
        tools=[generate_image],
    )


root_agent = get_image_generator_agent()
