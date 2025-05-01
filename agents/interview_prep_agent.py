from textwrap import dedent

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.crawl4ai import Crawl4aiTools
from agno.tools.duckduckgo import DuckDuckGoTools
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv

load_dotenv()


def read_file(path: str) -> str:
    """Read any file, convert it to markdown and return the content."""
    converter = DocumentConverter()
    result = converter.convert(path)
    return result.document.export_to_markdown()


agent = Agent(
    model=Gemini(id="gemini-2.5-flash-preview-04-17"),
    tools=[DuckDuckGoTools(), Crawl4aiTools(), read_file],
    instructions=dedent("""\
        1. CV Analysis
            - Read the requested file as Markdown
            - Summarize the CV and generate search terms to find the best matching vacancies

        2. Find a matching vacancy
            - Use DuckDuckGo to find vacancies
            - Crawl the full content of the best looking vacancies until you find a good match
            - If you are not sure about match, ALWAYS CONTINUE CRAWLING AND FOLLOWING LINKS TO VACANCIES UNTIL YOU FIND AN ADEQUATE MATCH

        3. Interview Preparation
            - Crawl information about the company of the best match you found
            - Compare the CV to the best matching vacancy
            - Explain why the CV is a good match for the vacancy
            - Write a cheat sheet to prepare for an interview for that job.
    """),
    markdown=True,
    show_tool_calls=True,
)

agent.print_response(
    "Please find me a good vacancy and prepare me for an interview, my CV is in data_cvs/Profile.pdf",
    stream=True,
)
