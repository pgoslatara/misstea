import datetime

from google.adk.agents import Agent, LoopAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import FunctionTool, google_search

from misstea.constants import AGENT_MODEL
from misstea.sub_agents.interactive_blogger.validation_checkers import (
    BlogPostValidationChecker,
    OutlineValidationChecker,
)

from .tools import analyze_codebase, save_blog_post_to_file


def suppress_output_callback(callback_context: CallbackContext) -> None:  # noqa: ARG001
    """Suppresses the output of the agent by returning an empty Content object.

    Returns:
        None

    """
    return None


blog_editor = Agent(
    model=AGENT_MODEL,
    name="blog_editor",
    description="Edits a technical blog post based on user feedback.",
    instruction="""
    You are a professional technical editor. You will be given a blog post and user feedback.
    Your task is to edit the blog post based on the provided feedback.
    The final output should be a revised blog post in Markdown format.
    """,
    output_key="blog_post",
    after_agent_callback=suppress_output_callback,
)

blog_planner = Agent(
    model=AGENT_MODEL,
    name="blog_planner",
    description="Generates a blog post outline.",
    instruction="""
    You are a technical content strategist. Your job is to create a blog post outline.
    The outline should be well-structured and easy to follow.
    It should include a title, an introduction, a main body with several sections, and a conclusion.
    If a codebase is provided, the outline should include sections for code snippets and technical deep dives.
    The codebase context will be available in the `codebase_context` state key.
    Use the information in the `codebase_context` to generate a specific and accurate outline.
    Use Google Search to find relevant information and examples to support your writing.
    Your final output should be a blog post outline in Markdown format.
    """,
    tools=[google_search],
    output_key="blog_outline",
    after_agent_callback=suppress_output_callback,
)

robust_blog_planner = LoopAgent(
    name="robust_blog_planner",
    description="A robust blog planner that retries if it fails.",
    sub_agents=[
        blog_planner,
        OutlineValidationChecker(name="outline_validation_checker"),
    ],
    max_iterations=3,
    after_agent_callback=suppress_output_callback,
)


blog_writer = Agent(
    model=AGENT_MODEL,
    name="blog_writer",
    description="Writes a technical blog post.",
    instruction="""
    You are an expert technical writer, crafting articles for a sophisticated audience similar to that of 'Towards Data Science' and 'freeCodeCamp'.
    Your task is to write a high-quality, in-depth technical blog post based on the provided outline and codebase summary.
    The article must be well-written, authoritative, and engaging for a technical audience.
    - Assume your readers are familiar with programming concepts and software development.
    - Dive deep into the technical details. Explain the 'how' and 'why' behind the code.
    - Use code snippets extensively to illustrate your points.
    - Use Google Search to find relevant information and examples to support your writing.
    - The codebase context will be available in the `codebase_context` state key.
    The final output must be a complete blog post in Markdown format. Do not wrap the output in a code block.
    """,
    tools=[google_search],
    output_key="blog_post",
    after_agent_callback=suppress_output_callback,
)

robust_blog_writer = LoopAgent(
    name="robust_blog_writer",
    description="A robust blog writer that retries if it fails.",
    sub_agents=[
        blog_writer,
        BlogPostValidationChecker(name="blog_post_validation_checker"),
    ],
    max_iterations=3,
)


interactive_blogger_agent = Agent(
    name="interactive_blogger_agent",
    model=AGENT_MODEL,
    description="The primary technical blogging assistant. It collaborates with the user to create a blog post.",
    instruction=f"""
    You are a technical blogging assistant. Your primary function is to help users create technical blog posts.

    Your workflow is as follows:

    1. **Analyze Codebase (Optional):** If the user provides a directory, you will analyze the codebase to understand its structure and content. To do this, use the `analyze_codebase` tool.

    2. **Plan:** You will generate a blog post outline and present it to the user. To do this, use the `robust_blog_planner` tool.

    3. **Refine:** The user can provide feedback to refine the outline. You will continue to refine the outline until it is approved by the user.

    4. **Visuals:** You will ask the user to choose their preferred method for including visual content. You have two options for including visual content in your blog post:
        1. **Upload:** I will add placeholders in the blog post for you to upload your own images and videos.
        2. **None:** I will not include any images or videos in the blog post.
        Please respond with "1" or "2" to indicate your choice.

    5. **Write:** Once the user approves the outline, you will write the blog post. To do this, use the `robust_blog_writer` tool. Be then open for feedback.

    6. **Edit:** After the first draft is written, you will present it to the user and ask for feedback. You will then revise the blog post based on the feedback. This process will be repeated until the user is satisfied with the result.

    7. **Export:** When the user approves the final version, you will ask for a filename and save the blog post as a markdown file. If the user agrees, use the `save_blog_post_to_file` tool to save the blog post.

    Current date: {datetime.datetime.now().strftime("%Y-%m-%d")}
    """,
    sub_agents=[
        robust_blog_writer,
        robust_blog_planner,
        blog_editor,
    ],
    tools=[
        FunctionTool(analyze_codebase),
        FunctionTool(save_blog_post_to_file),
    ],
    output_key="blog_outline",
)

root_agent = interactive_blogger_agent
