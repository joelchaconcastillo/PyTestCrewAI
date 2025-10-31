import ast

def check_code_style(code: str):
    """
    Minimal Python syntax / lint check using ast.parse.
    Returns:
        - passed: bool
        - issues: list[str]
    """
    try:
        ast.parse(code)
        return True, []
    except SyntaxError as e:
        return False, [f"SyntaxError: {e}"]
    except Exception as e:
        return False, [f"Error: {e}"]
