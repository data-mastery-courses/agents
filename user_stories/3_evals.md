# User Story: Evaluation of LLM Agents

As a contractor, I want to evaluate the quality of the job interview so that I can systematically judge the insights from the interview process.

* **Solution design:** Evaluate a CV/job-fit classification agent using PydanticAI:
  * The agent to be evaluated is in `cv_classifier_agent.py`
  * There is a test dataset in `agents/cases.yaml`
  * Implement a custom evaluator that checks if the agent's classification matches the expected output
  * Use the PydanticAI evaluation framework to:
    * Load the dataset
    * Run the agent on each case
    * Apply your evaluator to measure accuracy
