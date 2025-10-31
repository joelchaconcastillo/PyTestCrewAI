import asyncio
from pathlib import Path
import uuid
import json
import textwrap
from agents.analyzer_agent import AnalyzerAgent
from agents.testwriter_agent import TestWriterAgent
from agents.executor_agent import ExecutorAgent
from agents.reviewer_agent import ReviewerAgent
from dotenv import dotenv_values

async def run_workflow(code_snippet: str, llm, max_attempts: int = 3, dotfile: str = ".env"):
    """
    Run the full PyTestCrew AI workflow, export tests to a single file with prefix+UUID, and print a formatted review.
    """

    # Load configuration from dotfile
    config = dotenv_values(dotfile)
    test_file_prefix = config.get("TEST_FILE_PREFIX", "tests/test")
    
    # Resolve folder + create if needed
    prefix_path = Path(test_file_prefix)
    folder = prefix_path.parent
    folder.mkdir(parents=True, exist_ok=True)
    
    # Generate full test file path with UUID
    test_file = folder / f"{prefix_path.name}_{uuid.uuid4().hex}.py"

    # Initialize agents
    analyzer = AnalyzerAgent(
        name="Analyzer",
        role="Code Analyzer",
        goal="Analyze a Python code snippet and extract functions.",
        backstory="I am an AI agent that inspects code to prepare it for unit testing.",
        llm=llm
    )

    testwriter = TestWriterAgent(
        name="TestWriter",
        role="Test Generator",
        goal="Generate pytest unit tests for the given code snippet.",
        backstory="I am an AI agent that writes unit tests intelligently.",
        llm=llm
    )

    executor = ExecutorAgent(
        name="Executor",
        role="Test Executor",
        goal=f"Run pytest tests and retry failing tests up to {max_attempts} attempts.",
        backstory="I am an AI agent that executes tests and ensures they pass or request fixes.",
        llm=llm,
        max_attempts=max_attempts
    )

    reviewer = ReviewerAgent(
        name="Reviewer",
        role="Review Summarizer",
        goal="Summarize the analysis, generated tests, and test results for the user.",
        backstory="I am an AI agent that creates a clear report of code testing and coverage.",
        llm=llm
    )

    # Step 1: Analyze code
    analysis = await analyzer.run({"code_snippet": code_snippet})

    # Step 2: Generate tests
    tests = await testwriter.run({"analysis": analysis, "code_snippet": code_snippet})

    # Step 3: Save all tests to single file
    test_file.write_text("\n\n".join(tests))
    print(f"\n✅ Generated tests saved to: {test_file.resolve()}\n")

    # Step 4: Execute tests
    results = await executor.run({"tests": tests, "code_snippet": code_snippet})

    # Step 5: Summarize review
    review = await reviewer.run({"analysis": analysis, "tests": tests, "results": results})

    # Pretty print final review
    print("\n=== FINAL REVIEW ===\n")
    print(textwrap.indent(review["review"], prefix="  "))

    # Save review JSON in the same folder
    review_file = folder / "review.json"
    with open(review_file, "w") as f:
        json.dump(review, f, indent=2)
    print(f"\n✅ Review saved to: {review_file.resolve()}\n")

    return review
