class ReviewerAgent:
    """
    ReviewerAgent:
    Evaluates test quality using LLM reasoning and pytest results.
    """

    def __init__(self, config, llm):
        self.config = config
        self.llm = llm
        self.temperature = config.get("llm_temperature", 0.3)

    def __call__(self, test_report, analysis=None):
        analysis = analysis or {}
        test_output = test_report.get("test_results", {})
        test_code = test_report.get("test_code", "")
        stdout = test_output.get("stdout", "")
        stderr = test_output.get("stderr", "")
        passed = test_output.get("passed", False)

        func_names = [f["name"] for f in analysis.get("functions", [])] if analysis else []
        func_summary = ", ".join(func_names) if func_names else "unknown functions"

        prompt = f"""
        You are a senior QA engineer reviewing automated test generation.
        Analyze the following pytest output and generated test code.

        === FUNCTIONS UNDER TEST ===
        {func_summary}

        === GENERATED TEST CODE ===
        {test_code[:1200]}

        === PYTEST OUTPUT ===
        STDOUT:
        {stdout[:1000]}
        STDERR:
        {stderr[:500]}

        Provide:
        1. A short summary of test performance
        2. A score (0.0–1.0)
        3. Clear, actionable recommendations for improvement
        """

        try:
            response = self.llm.generate_content(prompt)
            review_text = response.text.strip()
        except Exception as e:
            review_text = f"⚠️ Review generation failed: {e}"

        score = 0.9 if passed else 0.6

        return {
            "summary": review_text,
            "score": score,
            "passed": passed,
            "stdout_excerpt": stdout[:500],
            "stderr_excerpt": stderr[:300],
        }
