from crewai import Agent
import ast

class TestWriterAgent(Agent):
    async def run(self, input_data: dict):
        code_snippet = input_data["code_snippet"]
        # Parse functions from code
        tree = ast.parse(code_snippet)
        functions = [f for f in tree.body if isinstance(f, ast.FunctionDef)]
        
        test_snippets = []

        for func in functions:
            func_name = func.name

            # Example: simple real test generation
            # For demonstration, we'll assume simple inputs
            if func_name == "divide":
                test_code = f"""import pytest

def {func_name}(a, b):
{ast.unparse(func).splitlines()[1]}  # body from original snippet

def test_{func_name}():
    assert {func_name}(6, 2) == 3
    assert {func_name}(10, 5) == 2
    with pytest.raises(ZeroDivisionError):
        {func_name}(1, 0)
"""
            else:
                test_code = f"""import pytest

def {func_name}(*args, **kwargs):
    # Original function body placeholder
    pass

def test_{func_name}():
    # TODO: write meaningful tests
    assert True
"""
            test_snippets.append(test_code)

        return test_snippets
