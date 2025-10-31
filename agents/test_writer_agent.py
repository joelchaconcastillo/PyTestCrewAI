from langgraph.graph import StateGraph, END
from utils.lint_checker import check_code_style
from utils.test_runner import run_pytest


class TestWriterAgent:
    """
    TestWriterAgent:
    Uses an LLM to generate pytest tests.
    Automatically re-generates if lint/style checks fail.
    """

    def __init__(self, config, llm):
        self.config = config
        self.llm = llm
        self.max_attempts = int(config.get("max_attempts", 3))

    def build_graph(self):
        g = StateGraph()
        g.add_node("generate", self.generate_tests)
        g.add_node("check", self.check_tests)
        g.add_node("run", self.run_tests)

        g.add_edge("generate", "check")
        g.add_edge("check", "generate", condition=lambda res: not res["passed"])
        g.add_edge("check", "run", condition=lambda res: res["passed"])
        g.add_edge("run", END)
        return g

    def __call__(self, source_code, analysis):
        """
        Orchestrates the generation-check-run flow.
        """
        graph = self.build_graph()
        state = {"source_code": source_code, "analysis": analysis}
        result = graph.run(state)
        return result.get("test_code")

    # === LangGraph nodes ===
    def generate_tests(self, state):
        source_code = state["source_code"]
        analysis = state["analysis"]

        prompt = f"""
        You are a Python testing assistant.
        Generate clean, minimal pytest tests for the following code.
        Use only pytest (no unittest), and focus on key behaviors.

        === SOURCE ANALYSIS ===
        {analysis['summary']}

        === SOURCE CODE ===
        {source_code[:2000]}

        === OUTPUT FORMAT ===
        Only provide valid Python test code using pytest.
        """

        try:
            response = self.llm.generate_content(prompt)
            generated_code = response.text.strip()
        except Exception as e:
            generated_code = f"# Error generating tests: {e}"

        return {"test_code": generated_code}

    def check_tests(self, state):
        ok, issues = check_code_style(state["test_code"])
        return {"passed": ok, "issues": issues, "test_code": state["test_code"]}

    def run_tests(self, state):
        result = run_pytest(state["test_code"])
        return {"test_code": state["test_code"], "test_results": result}
