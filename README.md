# Agentic AI

## Setup

1. Clone the repository `git clone https://github.com/data-mastery-courses/agents.git`
2. Make sure you have uv installed: https://docs.astral.sh/uv/getting-started/installation/
3. Install the dependencies: `uv sync`
4. Set up playwright: `uv run playwright install chromium`
5. Get a Gemini API key from AI Studio: https://aistudio.google.com/apikey
6. Copy .env.example to .env and fill in your new API key
7. Run `uv run agents/example_agent.py`, if everything is fine, you should see the output in the terminal.

# User Story: Interview Prep Agent

As a contractor, I want to be matched automatically to a new assignment based on my CV, so that I can save time and focus on work.

**Solution design:**
* Create an agent that:
  * Takes the user's CV as input (hint: write a tool that can read a PDF file as markdown using `docling`)
  * Uses the internet to find matching job vacancies (hint: DuckDuckGo)
  * Analyzes the best matching vacancy (hint: Crawl4ai)
  * Researches the company (hint: Crawl4ai)
  * Writes an interview preparation plan:
    * Explain why the user is a good fit for the vacancy
    * Generate personalized talking points for the interview
    * Suggest questions to ask the interviewer
* Use `agno` to build the agent
* Use Gemini Flash 2.5 as the LLM

Start from this repo: [github.com/data-mastery-courses/agents](https://github.com/data-mastery-courses/agents)
