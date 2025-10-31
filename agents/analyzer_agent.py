import ast

class AnalyzerAgent:
    """
    AnalyzerAgent:
    Parses source code to extract functions, classes, and docstrings.
    This output guides the TestWriterAgent to generate meaningful tests.
    """

    def __init__(self, config, llm):
        self.config = config
        self.llm = llm

    def __call__(self, source_code: str):
        """
        Analyze Python code and return structured data.
        """
        tree = ast.parse(source_code)
        functions = []
        classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    "name": node.name,
                    "args": [a.arg for a in node.args.args],
                    "docstring": ast.get_docstring(node),
                })
            elif isinstance(node, ast.ClassDef):
                classes.append({
                    "name": node.name,
                    "docstring": ast.get_docstring(node),
                })

        summary_prompt = f"""
You are a code summarizer.
Provide a concise description of what this code does, 
focusing on the purpose of each function and class.

=== SOURCE CODE ===
{source_code[:1500]}
"""

        try:
            response = self.llm.generate_content(summary_prompt)
            summary = response.text.strip()
        except Exception as e:
            # Fixed: no unterminated f-string
            summary = f"Summary generation failed: {e}"

        return {
            "functions": functions,
            "classes": classes,
            "summary": summary
        }
