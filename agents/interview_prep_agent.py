import asyncio

from crawl4ai import AsyncWebCrawler
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool

load_dotenv()


def read_file_as_markdown(path: str) -> str:
    """Reads any file, converts it to markdown, and returns the content."""
    try:
        converter = DocumentConverter()
        result = converter.convert(path)
        return result.document.export_to_markdown()
    except Exception as e:
        print(e)
        return f"Error: {e}"


class InterviewPrep(BaseModel):
    """The final output of the agent, containing all the information to prepare for the interview."""

    job_title: str = Field(description="The title of the job vacancy.")
    company: str = Field(description="The name of the company.")
    job_description_summary: str = Field(description="A summary of the job description.")
    cv_match_analysis: str = Field(description="An analysis of why the CV is a good match for the vacancy.")
    interview_cheat_sheet: str = Field(
        description="A cheat sheet with key points to mention during the interview."
    )


def create_prep_agent(cv_content: str) -> Agent:
    """Creates the Interview Prep Agent."""
    system_prompt = f"""
    You are an expert in hiring. Your goal is to find the best matching vacancy for the given CV and prepare the candidate for the interview.

    You will perform the following steps:
    1.  **Analyze the CV**: Understand the candidate's skills and experience from the CV provided below.
    2.  **Find a matching vacancy**: Use your web search tool to find job vacancies. Use the CV analysis to generate the search term. Crawl the most promising links to get the full job description. Ensure you don't crawl the same link twice.
    3.  **Prepare for the interview**: Once you have found a suitable vacancy, analyze it against the CV. Create a summary of why the candidate is a good fit and a cheat sheet for the interview.

    You must be autonomous and not ask for confirmation. When you have found a good match and prepared the materials, provide the final `InterviewPrep` object.

    --- CANDIDATE CV ---
    {cv_content}
    --- END OF CANDIDATE CV ---
    """
    agent = Agent(
        model="google-gla:gemini-2.0-flash-lite",
        output_type=InterviewPrep,
        system_prompt=system_prompt,
        tools=[duckduckgo_search_tool()],
        retries=2,
    )

    @agent.tool_plain
    async def crawl_webpage(url: str) -> str:
        """Crawls a webpage to extract its text content. Use this to get the full content of a job posting from a URL found via search."""
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url)
            return result.markdown

    return agent


async def main():
    """Main function to run the interview preparation agent."""
    print("# 🤖 AI Interview Prep Agent")

    cv_path = "data_cvs/Profile.pdf"
    cv_text = read_file_as_markdown(cv_path)

    agent = create_prep_agent(cv_text)

    prompt = "Please find me a good vacancy and prepare me for an interview."

    result = await agent.run(prompt)
    prep_data = result.output

    print("\n--- ✅ Interview Preparation Complete ---")
    print(f"\n### Job Title: {prep_data.job_title}")
    print(f"### Company: {prep_data.company}")
    print(f"\n**Job Description Summary:**\n{prep_data.job_description_summary}")
    print(f"\n**CV Match Analysis:**\n{prep_data.cv_match_analysis}")
    print(f"\n**Interview Cheat Sheet:**\n{prep_data.interview_cheat_sheet}")


if __name__ == "__main__":
    asyncio.run(main())
