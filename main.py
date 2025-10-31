import os
import asyncio
from dotenv import load_dotenv

from workflow import run_workflow
from crewai import LLM

# Load environment variables
load_dotenv()

async def main():
    code_snippet = """
def divide(a, b):
    return a / b
"""

    max_attempts = int(os.getenv("MAX_ATTEMPTS", 3))
    temperature = float(os.getenv("LLM_TEMPERATURE", 0.3))
    model = os.getenv("GEMINI_MODEL", "gemini/gemini-2.5-flash")
    api_key = os.getenv("GEMINI_API_KEY")

    # Configure Gemini 2.5 Flash LLM
    gemini_llm = LLM(
        model=model,
        api_key=api_key,
        temperature=temperature
    )

    # Run the workflow
    review = await run_workflow(code_snippet, gemini_llm, max_attempts=max_attempts)

    print("=== FINAL REVIEW ===")
    print(review)

if __name__ == "__main__":
    asyncio.run(main())
