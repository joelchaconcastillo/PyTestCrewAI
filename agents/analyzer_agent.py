import ast
from crewai import Agent

class AnalyzerAgent(Agent):
    async def run(self, input_data: dict):
        """
        input_data: {"code_snippet": str}
        Returns a dictionary with analysis results (e.g., function names)
        """
        code_snippet = input_data.get("code_snippet", "")
        if not isinstance(code_snippet, str):
            raise TypeError(f"Expected code_snippet to be str, got {type(code_snippet)}")

        tree = ast.parse(code_snippet)
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        return {"functions": functions}
