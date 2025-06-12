# User Story: n8n AI CV Chat Agent

As a contractor, I want to build an n8n AI CV chat agent so that I can prepare for the actual interview.

* **Solution design:** Create an agent in n8n:
  * Use Gemini Flash 2.5 (`gemini-2.5-flash-preview-05-20`) as the LLM
  * Take the user's CV (PDF) as input
  * Create a chat interface where the user can ask questions about their CV
  * Update the prompt for the LLM to function as interview preparation coach and use the CV as context
