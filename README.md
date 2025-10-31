# PyTestCrew AI

**Autonomous CrewAI System for Intelligent Unit Test Generation and Self-Correction**

---

## **Overview**

**PyTestCrew AI** is an AI-driven system that automatically generates, executes, and self-corrects **Python unit tests** for code snippets using **CrewAI** and **GraphChain (LangGraph)**.
It demonstrates advanced **multi-agent orchestration**, **LLM reasoning**, and **developer workflow automation**, making it perfect for a portfolio project in AI engineering or DevOps tooling.

---

## **Features**

* **Automatic test generation**: Generates pytest unit tests for Python functions using LLM reasoning.
* **Edge-case coverage**: Creates tests for normal, boundary, and invalid input scenarios.
* **Self-correcting execution**: Runs tests and fixes failing ones autonomously up to `k` attempts.
* **Modular multi-agent architecture**:

  * `AnalyzerAgent`: Extracts functions and arguments.
  * `TestWriterAgent`: Generates and fixes tests intelligently.
  * `ExecutorAgent`: Runs tests using pytest and retries failures.
  * `ReviewerAgent`: Summarizes results and coverage.
* **GraphChain workflow**: Orchestrates agent interactions seamlessly.
* **Extensible**: Can be extended to multiple languages, frameworks, and CI/CD pipelines.

---

## **Tech Stack**

* Python 3.10+
* **CrewAI**: Multi-agent orchestration
* **LangGraph**: GraphChain workflow engine
* **OpenAI GPT-4 / LLM**: Intelligent test generation and self-correction
* **pytest**: Unit test execution
* Optional: Streamlit / FastAPI for UI demos

---

## **Installation**

1. Clone the repo:

```bash
git clone https://github.com/yourusername/pytestcrew_ai.git
cd pytestcrew_ai
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

---

## **Usage**

```bash
python main.py
```

* The script will:

  1. Analyze the code snippet.
  2. Generate pytest unit tests.
  3. Execute tests, retrying failing ones up to `max_attempts`.
  4. Print a final review summarizing results.

### Example Python snippet:

```python
def divide(a, b):
    return a / b
```

### Example Output:

```
=== FINAL REVIEW ===
4 test(s) generated for 1 function(s).

Test divide_basic: PASSED
Test divide_zero: FAILED -> fixed on attempt 2
Test divide_negative: PASSED
Test divide_float: PASSED

All tests passed after 2 attempts.
```

---

## **Project Architecture**

```
+-------------------+
|   AnalyzerAgent   | ---> Extract functions
+-------------------+
          |
          v
+-------------------+
|  TestWriterAgent  | ---> Generate initial tests
+-------------------+
          |
          v
+-------------------+
|   ExecutorAgent   | ---> Run tests, fix failures (k attempts)
+-------------------+
          |
          v
+-------------------+
|   ReviewerAgent   | ---> Summarize results and coverage
+-------------------+
```

* **GraphChain (LangGraph)** orchestrates data flow between agents.
* **CrewAI** enables asynchronous agent reasoning and LLM calls.

---

## **Configuration**

* `max_attempts` (int): Maximum retries for fixing failing tests. Default = 3.
* LLM configuration: Use **CrewAI LLM agent** or **OpenAI GPT-4 API** for intelligent test generation.