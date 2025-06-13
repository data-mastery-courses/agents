import asyncio
from pathlib import Path

from pydantic_evals import Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext

from agents.cv_classifier_agent import CvFitInputs, JobFitClassification, classify_cv_fit


class ClassificationEvaluator(Evaluator):
    """
    Custom evaluator that only checks the 'classification' field of the
    JobFitClassification output.
    """

    def evaluate(self, ctx: EvaluatorContext[JobFitClassification, JobFitClassification]) -> float:
        """
        Returns 1.0 if classifications match, 0.0 otherwise.
        """
        if ctx.output.classification == ctx.expected_output.classification:
            return 1.0  # Success
        return 0.0  # Failure


async def main():
    """Runs the evaluation for the CV fit classification agent."""
    cases_file = Path("agents/cases.yaml")
    if not cases_file.exists():
        print(f"Error: Cases file not found at {cases_file}")
        return

    print(f"Loading dataset from {cases_file}...")
    dataset = Dataset[CvFitInputs, JobFitClassification].from_file(cases_file)

    print("Running evaluation...")
    dataset.evaluators = [ClassificationEvaluator()]
    report = await dataset.evaluate(classify_cv_fit, max_concurrency=1)

    print("\nEvaluation Report:")
    report.print()
    report_file = Path("report.json")
    report_file.write_text(report.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
