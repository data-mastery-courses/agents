
# User Story: Multi-Agent Interview Simulation

As a contractor, I want to simulate a job interview so that I can prepare for the actual interview in the most optimal way.

* **Solution design:**  
  * Read the user's CV from a PDF file and convert it to markdown using `docling`.
  * Fetch the job description from a web page using `crawl4ai`.
  * Create a **Candidate Agent** with the CV as its context. The agent only answers questions based on the CV.
  * Create an **Interviewer Agent** with the job description and the CV. The interviewer uses the candidate agent as a tool to ask questions and get answers.
  * The interviewer agent conducts a structured interview:
    * Greets the candidate.
    * Asks a series of relevant questions (including: fit for the role, relevant project, strengths/weaknesses).
    * Follows up based on answers.
    * Concludes with feedback and a hire/do-not-hire recommendation.
  * Use `pydantic_ai` for agent orchestration.
  * Use Gemini Flash 2.5 as the LLM for the candidate, and Gemini Flash Lite 2.0 for the interviewer.
  * Run the interview loop until the interviewer concludes.
