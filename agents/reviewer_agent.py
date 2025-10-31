from crewai import Agent

class ReviewerAgent(Agent):
    async def run(self, input_data: dict):
        """
        input_data: {"analysis": dict, "tests": list, "results": list}
        Returns a summarized review of the workflow.
        """
        analysis = input_data.get("analysis", {})
        tests = input_data.get("tests", [])
        results = input_data.get("results", [])

        review_text = f"Functions analyzed: {analysis.get('functions', [])}\n"
        review_text += f"Generated {len(tests)} tests.\n"
        review_text += f"Test results:\n"
        for res in results:
            review_text += f" - Test: {res['test']}, Success: {res['success']}, Attempts: {res['attempts']}\n"

        return {"review": review_text.strip()}
