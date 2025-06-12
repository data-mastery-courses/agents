import asyncio
from typing import Literal

import dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent

dotenv.load_dotenv()


class CvFitInputs(BaseModel):
    """Inputs for CV fit classification."""

    cv_text: str = Field(description="The text of the candidate's CV.")
    job_vacancy_text: str = Field(description="The text of the job vacancy.")


class JobFitClassification(BaseModel):
    explanation: str = Field(description="A short explanation of the classification.")
    classification: Literal["Very Bad", "Bad", "Mediocre", "Good", "Very Good"] = Field(
        description="How well the CV fits the job vacancy."
    )


async def classify_cv_fit(inputs: CvFitInputs) -> JobFitClassification:
    """
    Classifies the fit of a CV to a job vacancy using a Pydantic AI agent.

    Args:
        inputs: The inputs for the CV fit classification.

    Returns:
        The classification of the fit, as one of "Very Bad", "Bad",
        "Mediocre", "Good", or "Very Good".
    """
    agent = Agent(
        model="google-gla:gemini-2.0-flash-lite",
        output_type=JobFitClassification,
        instructions=[
            "You are an expert HR assistant.",
            "Your task is to classify the fit of a candidate's CV to a job vacancy.",
            "The classification must be one of: 'Very Bad', 'Bad', 'Mediocre', 'Good', 'Very Good'.",
        ],
    )

    prompt = f"""
    Here is the CV:
    ---
    {inputs.cv_text}
    ---

    Here is the job vacancy:
    ---
    {inputs.job_vacancy_text}
    ---

    Please classify the fit of the CV to the job vacancy based on the requirements and the candidate's experience.
    """

    result = await agent.run(prompt)
    return result.output


if __name__ == "__main__":
    cv = """
    John Doe
    Software Engineer

    Experience:
    - 5 years of experience with Python.
    - 3 years of experience with Django and Flask.
    - Built and maintained several web applications.
    - Proficient in SQL and NoSQL databases.
    """

    job_vacancy = """
    Senior Python Developer

    Requirements:
    - 8+ years of experience in Python development.
    - Strong experience with Django.
    - Experience with cloud platforms like AWS.
    - Excellent problem-solving skills.
    """
    fit_classification = asyncio.run(classify_cv_fit(CvFitInputs(cv_text=cv, job_vacancy_text=job_vacancy)))
    print(f"Explanations: {fit_classification.explanation}\n")
    print(f"Classification: {fit_classification.classification}")
