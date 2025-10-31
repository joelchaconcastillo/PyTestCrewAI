import os
from dotenv import load_dotenv
import streamlit as st
from crew_workflow.workflow import CrewWorkflow

# Load environment variables
load_dotenv()

# --- Streamlit UI ---
st.set_page_config(page_title="CrewWorkflow Runner", layout="wide")
st.title("CrewWorkflow Runner 🌟")

# Sidebar for workflow configuration
st.sidebar.header("Workflow Configuration")

max_attempts = st.sidebar.number_input(
    "Max Attempts", min_value=1, max_value=10, value=int(os.getenv("MAX_ATTEMPTS", 3))
)
test_file_prefix = st.sidebar.text_input(
    "Test File Prefix", value=os.getenv("TEST_FILE_PREFIX", "generated_tests/unit_test")
)

st.header("Source Code Input")
source_code = st.text_area(
    "Paste your Python source code here:",
    value="""
def divide(a, b):
    return a / b
""",
    height=200
)

if st.button("Run CrewWorkflow"):
    # Build full config, including hidden keys/models from environment
    config = {
        "gemini_api_key": os.getenv("GEMINI_API_KEY"),
        "gemini_model": os.getenv("GEMINI_MODEL", "gemini/gemini-2.5-flash"),
        "temperature": float(os.getenv("LLM_TEMPERATURE", 0.3)),
        "max_attempts": max_attempts,
        "test_file_prefix": test_file_prefix,
    }

    workflow = CrewWorkflow(config)
    with st.spinner("Running workflow..."):
        result = workflow.run(source_code)

    st.success("✅ Workflow completed")

    # Convert CrewOutput to dict
    result_dict = result.dict()  # <- this fixes the AttributeError
    for task_name, output in result_dict.items():
        st.subheader(f"Task: {task_name}")
        st.code(output)
