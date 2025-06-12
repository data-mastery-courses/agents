import dotenv
from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool

dotenv.load_dotenv()

agent = Agent(
    model="google-gla:gemini-2.0-flash-lite",
    tools=[duckduckgo_search_tool()],
)

result = agent.run_sync(
    "What kind of training modules does the company Data Mastery provide? Search the web for the information.",
)

print("Response:")
print(result.output)
