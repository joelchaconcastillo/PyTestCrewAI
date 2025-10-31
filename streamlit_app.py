import streamlit as st
import asyncio
from pathlib import Path
from dotenv import dotenv_values
from crewai.llm import LLM
from workflow import run_workflow  # Your workflow function

# Load .env config
config = dotenv_values(".env")
gemini_api_key = config.get("GEMINI_API_KEY")
gemini_model = config.get("GEMINI_MODEL", "gemini-2.5-flash")

st.title("PyTestCrew AI")

st.write("Generate Pytest unit tests and reviews automatically from a Python snippet!")

# User inputs
code_snippet = st.text_area("Enter Python code snippet", height=200)
max_attempts = st.number_input("Max retry attempts", min_value=1, max_value=10, value=3)

if st.button("Run Workflow"):
    if not code_snippet.strip():
        st.error("Please enter a Python code snippet!")
    else:
        with st.spinner("Running workflow..."):
            # Initialize Gemini LLM
            gemini_llm = LLM(
                model=gemini_model,
                api_key=gemini_api_key,
                temperature=0
            )

            # Run workflow
            workflow_result = asyncio.run(
                run_workflow(
                    code_snippet=code_snippet,
                    llm=gemini_llm,
                    max_attempts=max_attempts,
                    dotfile=".env"
                )
            )

            st.success("Workflow completed!")

            # Display final review
            st.subheader("Final Review")
            st.text(workflow_result["review"])

            # Retrieve generated test file(s) and review.json from workflow folder
            test_file_prefix = config.get("TEST_FILE_PREFIX", "tests/test")
            prefix_path = Path(test_file_prefix)
            folder = prefix_path.parent

            # Show and offer downloads
            st.subheader("Generated Files")
            for file_path in folder.glob(f"{prefix_path.name}_*.py"):
                st.write(f"**{file_path.name}**")
                st.download_button(
                    label="Download Test File",
                    data=file_path.read_text(),
                    file_name=file_path.name,
                    mime="text/plain"
                )

            review_file = folder / "review.json"
            if review_file.exists():
                st.write(f"**{review_file.name}**")
                st.download_button(
                    label="Download Review JSON",
                    data=review_file.read_text(),
                    file_name=review_file.name,
                    mime="application/json"
                )
