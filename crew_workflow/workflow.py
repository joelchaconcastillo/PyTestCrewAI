from crewai import Agent, Task, Crew
from utils.llm_factory import create_llm
from utils.test_runner import run_pytest
from utils.lint_checker import check_code_style


class CrewWorkflow:
    """
    CrewAI 1.2.1 workflow:
    AnalyzerAgent -> TestWriterAgent -> ExecutorAgent -> ReviewerAgent
    Tasks are executed via Crew.kickoff() orchestration.
    """

    def __init__(self, config: dict):
        self.config = config
        self.llm = create_llm(config)

        # --- Define Agents ---
        self.analyzer_agent = Agent(
            name="Code Analyzer",
            role="Software Code Analyst",
            goal="Analyze Python source code and extract its structure, functions, classes, and docstrings.",
            backstory="Understands Python syntax, semantic patterns, and code organization.",
            instructions=(
                "You will receive Python source code and must analyze it to identify "
                "all classes, functions, and docstrings, returning a structured JSON summary."
            ),
            verbose=True,
            llm=self.llm,
        )

        self.writer_agent = Agent(
            name="Test Writer",
            role="Unit Test Generator",
            goal="Generate pytest-style unit tests for the provided Python code.",
            backstory="Writes clean, maintainable, and effective pytest tests covering key behaviors.",
            instructions=(
                "Using the analysis of the source code, generate pytest-compatible test cases "
                "that thoroughly cover the discovered functions and classes."
            ),
            verbose=True,
            llm=self.llm,
        )

        self.executor_agent = Agent(
            name="Executor",
            role="Test Executor",
            goal="Run pytest-based tests and report the results.",
            backstory="Executes test suites and gathers pass/fail results and exceptions.",
            instructions=(
                "Execute the provided pytest test code and report back the results as JSON. "
                "Include pass/fail counts and any errors encountered."
            ),
            verbose=True,
            llm=self.llm,
        )

        self.reviewer_agent = Agent(
            name="Reviewer",
            role="Test Coverage Reviewer",
            goal="Review the test execution results and provide improvement recommendations.",
            backstory="Evaluates test quality, coverage, and identifies missing edge cases.",
            instructions=(
                "Review the test execution results and analysis output. "
                "Provide feedback on coverage, missing tests, and suggestions for improvement."
            ),
            verbose=True,
            llm=self.llm,
        )

        # --- Define Tasks with prompt templates ---
        # 1️⃣ Analyze Code
        self.analyze_task = Task(
            name="Analyze Source Code",
            description="Analyze the given source code and extract its functions, classes, and docstrings. This is the code {source_code}",
            expected_output="Structured JSON of all identified code elements.",
            agent=self.analyzer_agent,
            input_mapping={"source_code": "source_code"},
        )

        # 2️⃣ Generate Tests
        self.generate_task = Task(
            name="Generate Unit Tests",
            description="Generate pytest-compatible unit tests based on the analysis output.",
            expected_output="Python code string containing pytest test cases.",
            agent=self.writer_agent,
            context=[self.analyze_task],
        )

        # 3️⃣ Execute Tests
        self.execute_task = Task(
            name="Execute Unit Tests",
            description="Run generated pytest tests and collect their results.",
            expected_output="Dictionary of test outcomes (passed, failed, errors).",
            agent=self.executor_agent,
            context=[self.generate_task],
        )

        # 4️⃣ Review Results
        self.review_task = Task(
            name="Review Test Results",
            description="Review execution results and suggest improvements to test coverage.",
            expected_output="Detailed feedback report with actionable recommendations.",
            agent=self.reviewer_agent,
            context=[self.execute_task, self.analyze_task],
        )

        # --- Create Crew ---
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

    def run(self, source_code: str):
        """Run the full multi-agent workflow."""
        if not source_code or not source_code.strip():
            raise ValueError("❌ Source code input is empty!")

        print("🚀 Starting CrewAI Workflow (v1.2.1)...")
        print(source_code)
        inputs = {"source_code": source_code}
        result = self.crew.kickoff(inputs=inputs)

        # Retrieve generated test code
        test_code = getattr(result, "Generate_Unit_Tests", None)
        if test_code:
            lint_ok, lint_issues = check_code_style(test_code)
            if not lint_ok:
                print(f"⚠️ Lint issues found:\n{lint_issues}")

        print("✅ Workflow completed.")
        return result