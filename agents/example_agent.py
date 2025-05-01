from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model=Gemini(id="gemini-2.5-flash-preview-04-17"),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)
agent.print_response(
    "What kind of training modules does the company Data Mastery provide?",
    stream=True,
)
