import os
from dotenv import load_dotenv
from crew_workflow.workflow import CrewWorkflow

# Load environment variables
load_dotenv()

def main():
    # Read environment variables (with sane defaults)
    config = {
        "gemini_api_key": os.getenv("GEMINI_API_KEY"),
        "gemini_model": os.getenv("GEMINI_MODEL", "gemini/gemini-2.5-flash"),
        "temperature": float(os.getenv("LLM_TEMPERATURE", 0.3)),
        "max_attempts": int(os.getenv("MAX_ATTEMPTS", 3)),
        "test_file_prefix": os.getenv("TEST_FILE_PREFIX", "generated_tests/unit_test"),
    }

    # Example source code input
    source_code = """
    def divide(a, b):
        return a / b
    """

    # Initialize workflow with config
    workflow = CrewWorkflow(config)
    result, _ = workflow.run(source_code)

    print("\n=== FINAL RESULT ===")

    # Convert CrewOutput to dict first
    result_dict = result.dict()  # <-- this is the key fix

    for task_name, output in result_dict.items():
        print(f"\nTask: {task_name}")
        print(output)



if __name__ == "__main__":
    main()
