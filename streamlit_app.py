import os
import streamlit as st
from dotenv import load_dotenv
from crew_workflow.workflow import CrewWorkflow
from utils.examples import example_dijkstra
load_dotenv()

st.title("🧪 PyTestCrew_AI — AI-Powered Python Test Generator")
st.caption("Automatically create, run, and validate Python tests using AI-driven workflows")


config = {
    "gemini_api_key": os.getenv("GEMINI_API_KEY"),
    "gemini_model": os.getenv("GEMINI_MODEL", "gemini/gemini-2.5-flash"),
    "temperature": float(os.getenv("LLM_TEMPERATURE", 0.3)),
    "max_attempts": int(os.getenv("MAX_ATTEMPTS", 3)),
    "test_file_prefix": os.getenv("TEST_FILE_PREFIX", "generated_tests/unit_test"),
}

st.header("Source Code Input")
source_code = st.text_area(
    "Paste your Python code here:", 
    height=200, 
    value=f"{example_dijkstra}"
)

if st.button("Run Workflow"):
    if not source_code.strip():
        st.error("Please provide source code to run the workflow.")
    else:
        workflow = CrewWorkflow(config)

        with st.spinner("Running CrewAI workflow..."):
            result, file_path = workflow.run(source_code)

        st.success("Workflow completed!")

    result_dict  = result.dict()

    if file_path and os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            st.download_button(
                label=f"Download {os.path.basename(file_path)}",
                data=f.read(),
                file_name=os.path.basename(file_path),
                mime="text/plain"
            )

    for task_name, output in result_dict.items():
        st.subheader(f"Task: {task_name}")
        st.code(output)
