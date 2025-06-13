import asyncio
import time
from typing import Literal

from crawl4ai import AsyncWebCrawler
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent

load_dotenv()


def read_file_as_markdown(path: str) -> str:
    """Reads any file, converts it to markdown, and returns the content."""
    converter = DocumentConverter()
    result = converter.convert(path)
    return result.document.export_to_markdown()


async def extract_webpage_text(url: str) -> str:
    """Fetches a URL and extracts the main text content."""
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url)
        return result.markdown


def create_candidate_agent(cv_content: str) -> Agent:
    """Creates the Candidate Agent with the CV baked into its system prompt."""
    system_prompt = f"""
    You are a job candidate. Your personality is professional, concise, and positive.
    You MUST answer all questions based *only* on the information contained in the CV provided below.
    Do not invent experience, skills, or details not present in the CV.
    Keep your answers direct and to the point.

    --- YOUR CV ---
    {cv_content}
    --- END OF CV ---
    """
    return Agent(
        model="google-gla:gemini-2.5-flash-preview-05-20",
        system_prompt=system_prompt,
    )


class EndInterview(BaseModel):
    """The action to conclude the interview with a summary and recommendation."""

    feedback: str = Field(description="Feedback on the candidate's performance.")
    recommendation: Literal["Hire", "Do Not Hire"] = Field(description="Final hiring recommendation.")


def create_interviewer_agent(job_description: str, candidate_agent: Agent, cv_content: str) -> Agent:
    """Creates the Interviewer Agent, which uses the Candidate Agent as a tool."""
    system_prompt = f"""
    You are a professional and insightful Hiring Manager.
    Your goal is to assess if the candidate is a good fit for the role described below by conducting a structured interview.
    You must start with a brief greeting, then ask a series of relevant questions. You can create follow-up questions based on the candidate's answers.
    When you have enough information, end the interview by providing a final summary and recommendation.

    Questions that should always be asked:
    - Why do you think you are a good fit for this role?
    - Walk through an example of a project you have worked on relevant to this role
    - What are your biggest strengths and weaknesses?

    --- JOB DESCRIPTION ---
    {job_description}
    --- END OF JOB DESCRIPTION ---

    --- CANDIDATE CV ---
    {cv_content}
    --- END OF CANDIDATE CV ---
    """
    interviewer = Agent(
        model="google-gla:gemini-2.0-flash-lite",
        output_type=Literal["AskQuestion"] | EndInterview,
        system_prompt=system_prompt,
        retries=2,
    )

    @interviewer.tool_plain
    async def ask_candidate(question_to_candidate: str) -> str:
        """Asks the candidate a specific question and returns their answer."""
        print(f"\n## Interviewer:\n{question_to_candidate}")

        result = await candidate_agent.run(question_to_candidate)
        answer = result.output

        print(f"\n## Candidate:\n{answer}")
        return answer

    return interviewer


async def main():
    """Main function to run the interview simulation."""
    print("# 🤖 AI Job Interview Simulation")

    cv_path = "data_cvs/Profile.pdf"
    job_url = "https://www.circle8.nl/opdracht/azure-data-engineer_VNR-73585"

    cv_text = read_file_as_markdown(cv_path)
    job_text = await extract_webpage_text(job_url)

    print("\n--- Starting Simulation ---")

    candidate = create_candidate_agent(cv_text)
    interviewer = create_interviewer_agent(job_text, candidate, cv_text)

    prompt = "Start the interview. Greet the candidate and ask your first question."

    while True:
        result = await interviewer.run(prompt)
        action = result.output

        if isinstance(action, EndInterview):
            print("\n--- 🎤 Interview Concluded ---")
            print(f"\n### Interview Feedback\n{action.feedback}")
            print(f"\n**Final Recommendation:** `{action.recommendation}`")
            break

        prompt = "Continue the interview. Ask the next logical question or conclude if you are finished."
        time.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
