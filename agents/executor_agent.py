import os
from utils.test_runner import run_pytest


class ExecutorAgent:
    """
    ExecutorAgent:
    Executes generated pytest code and captures structured results.
    """

    def __init__(self, config, llm):
        self.config = config
        self.llm = llm
        self.test_prefix = config.get("test_file_prefix", "generated_tests/unit_test")

    def __call__(self, test_code: str):
        os.makedirs(os.path.dirname(self.test_prefix), exist_ok=True)
        test_file = f"{self.test_prefix}.py"

        with open(test_file, "w") as f:
            f.write(test_code)

        result = run_pytest(test_file)

        return {
            "test_file": test_file,
            "test_results": result,
            "test_code": test_code,
        }
