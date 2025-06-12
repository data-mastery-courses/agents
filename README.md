# Agentic AI

## Setup python environment

1. Clone the repository `git clone https://github.com/data-mastery-courses/agents.git`
2. Make sure you have uv installed: https://docs.astral.sh/uv/getting-started/installation/
3. Install the dependencies: `uv sync`
4. Set up playwright: `uv run playwright install chromium`
5. Get a Gemini API key from AI Studio: https://aistudio.google.com/apikey
6. Copy .env.example to .env and fill in your new API key
7. Run `uv run agents/example_agent.py`, if everything is fine, you should see the output in the terminal.

## Setup n8n

Running n8n is easiest using Node.js or using Docker. If you have neither of those, consider installing Node.js: https://nodejs.org/en/download

### In case you have Node.js installed

Run:
```bash
npx n8n
```

### In case you have docker installed
To run a lightweight n8n docker container run the following command:

```bash
docker run -it --rm --name n8n -p 5678:5678 -v ./data_cvs:/data_cvs docker.n8n.io/n8nio/n8n
```

Note that the `./data_cvs` directory is mounted to the container's `/data_cvs` directory, which is where n8n will read the CV PDFs from.
