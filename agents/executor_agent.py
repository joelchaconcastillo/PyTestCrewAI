from crewai import Agent
from pydantic import Field

class ExecutorAgent(Agent):
    max_attempts: int = Field(default=3, description="Number of retries for failing tests")

    async def run(self, input_data: dict):
        """
        input_data: {"tests": list, "code_snippet": str}
        Executes tests up to max_attempts retries.
        """
        tests = input_data.get("tests", [])
        code_snippet = input_data.get("code_snippet", "")
        if not isinstance(code_snippet, str):
            raise TypeError(f"Expected code_snippet to be str, got {type(code_snippet)}")

        results = []
        for test in tests:
            attempt = 0
            success = False
            while attempt < self.max_attempts and not success:
                attempt += 1
                # Placeholder: here you could integrate real pytest execution
                success = True  # Simulate success
                results.append({"test": test, "success": success, "attempts": attempt})
        return results
