import os
from crewai import Agent, Task, Crew
from utils.llm_factory import create_llm
#from utils.test_runner import run_pytest
from utils.lint_checker import check_code_style


class CrewWorkflow:
    """
    CrewAI 1.2.1 workflow:
    AnalyzerAgent -> TestWriterAgent -> ExecutorAgent -> ReviewerAgent
    Tasks executed via Crew.kickoff()
    """

    def __init__(self, config: dict, test_file_prefix: str = "test_"):
        self.config = config
        self.llm = create_llm(config)
        self.test_file_prefix = test_file_prefix

        # --- Define Agents ---
        self.analyzer_agent = Agent(
            name="Code Analyzer",
            role="Software Code Analyst",
            goal="Analyze Python source code and extract its structure, functions, classes, and docstrings.",
            backstory="Understands Python syntax, semantics, and structure.",
            instructions=(
                "Analyze the Python source code to identify all classes, functions, and docstrings, "
                "and return them in structured JSON format."
            ),
            verbose=True,
            llm=self.llm,
        )

        self.writer_agent = Agent(
            name="Test Writer",
            role="Unit Test Generator",
            goal="Generate pytest-style unit tests for the provided code.",
            backstory="Writes clean, maintainable pytest tests with broad coverage.",
            instructions=(
                "Generate pytest-compatible test cases covering functions, classes, and edge cases "
                "identified in the analysis."
            ),
            verbose=True,
            llm=self.llm,
        )

        self.executor_agent = Agent(
            name="Executor",
            role="Test Executor",
            goal="Run pytest-based tests and summarize results.",
            backstory="Executes pytest and captures pass/fail/error results.",
            instructions="Execute the provided pytest test code and report structured JSON results.",
            verbose=True,
            llm=self.llm,
        )

        self.reviewer_agent = Agent(
            name="Reviewer",
            role="Test Coverage Reviewer",
            goal="Review test execution results and suggest improvements.",
            backstory="Expert in identifying gaps and improving test coverage.",
            instructions=(
                "Analyze test results and the analyzed code. Suggest missing tests, edge cases, "
                "and robustness improvements."
            ),
            verbose=True,
            llm=self.llm,
        )

        # --- Define Tasks ---
        self.analyze_task = Task(
            name="Analyze Source Code",
            description=(
                "Analyze the given Python source code: {source_code}. "
                "Extract its functions, classes, and docstrings as structured JSON."
            ),
            expected_output="Structured JSON of all identified code elements.",
            agent=self.analyzer_agent,
            input_mapping={"source_code": "source_code"},
        )

        self.generate_task = Task(
            name="Generate Unit Tests",
            description="Generate pytest-compatible unit tests based on the analysis output.",
            expected_output="Python code string containing pytest test cases.",
            agent=self.writer_agent,
            context=[self.analyze_task],
        )

        self.execute_task = Task(
            name="Execute Unit Tests",
            description="Run the generated pytest tests and collect results in JSON.",
            expected_output="Dictionary with passed, failed, and error test lists.",
            agent=self.executor_agent,
            context=[self.generate_task],
        )

        self.review_task = Task(
            name="Review Test Results",
            description="Review test results and suggest ways to improve coverage and quality.",
            expected_output="Feedback report with actionable recommendations.",
            agent=self.reviewer_agent,
            context=[self.execute_task, self.analyze_task],
        )

        # --- Assemble Crew ---
        self.crew = Crew(
            name="Code Testing Crew",
            agents=[
                self.analyzer_agent,
                self.writer_agent,
                self.executor_agent,
                self.reviewer_agent,
            ],
            tasks=[
                self.analyze_task,
                self.generate_task,
                self.execute_task,
                self.review_task,
            ],
            verbose=True,
        )

    def run(self, source_code: str, output_dir: str = "./tests"):
        """Run the entire CrewAI workflow and save the generated unit tests."""
        if not source_code or not source_code.strip():
            raise ValueError("❌ Source code input is empty!")

        os.makedirs(output_dir, exist_ok=True)
        print("🚀 Starting CrewAI Workflow (v1.2.1)...")

        # Run Crew
        inputs = {"source_code": source_code}
        result = self.crew.kickoff(inputs=inputs)

        if not self.generate_task.output.raw:
            print("❌ No test code generated.")
            return result

        test_code = self.generate_task.output.raw

        # --- Lint & Save ---
        lint_ok, lint_issues = check_code_style(test_code)
        if not lint_ok:
            print(f"⚠️ Lint issues found:\n{lint_issues}")

        file_path = os.path.join(output_dir, f"{self.test_file_prefix}generated.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(test_code)
        print(f"💾 Unit tests saved to {file_path}")

        print("✅ Workflow completed.")
        return result, file_path
